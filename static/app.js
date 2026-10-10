// ============================================================
//  app.js  —  ตรรกะหน้าเว็บ (ทำให้เสร็จแล้ว ★ นิสิตไม่ต้องแก้)
//  ปรับช่องค้นหา/ฟอร์มได้ที่ตัวแปร ENTITIES ด้านล่าง
// ============================================================
// value = ค่าที่เก็บใน database (ต้องตรงกับ ENUM), label = ข้อความที่แสดงบนหน้าจอ
const GENDERS = [{ "value": "female"        , "label": "หญิง" },
                 { "value": "male"          , "label": "ชาย" },
                 { "value": "non_binary"    , "label": "นอนไบนารี" }, 
                 { "value": "not_specified" , "label": "ไม่ระบุ" }];

const ENTITIES = {
  "members": {
    "label": "สมาชิก",
    "api": "/api/members",
    "idKey": "member_id",
    "search": [
      { "key": "name"   , "label": "ชื่อ"   , "type": "text" },
      { "key": "gender" , "label": "เพศ"  , "type": "select", 
        "options": [ "", "male", "female", "non_binary", "not_specified" ] },
      { "key": "package_type", "label": "แพ็กเกจ", "type": "select",
        "options": [ "", "Regular", "Vip" ] } ],
      "form": [
      { "key": "name", "label": "ชื่อ", "type": "text" },
      { "key": "gender", "label": "เพศ", "type": "select",
        "options": [ "male", "female", "non_binary", "not_specified" ] },
      { "key": "join_date", "label": "วันที่สมัคร", "type": "date"},
      { "key": "package_type", "label": "แพ็กเกจ", "type": "select",
        "options": [ "Regular", "Vip" ] } ] },
  "classes": {
    "label": "คลาสเรียน",
    "api": "/api/classes",
    "idKey": "class_id",
    "search": [
      { "key": "name", "label": "ชื่อคลาส", "type": "text"},
      { "key": "room", "label": "ห้อง", "type": "text" } ],
    "form": [
      { "key": "name", "label": "ชื่อคลาส", "type": "text" },
      { "key": "trainer_id", "label": "เทรนเนอร์", "type": "select", "options": []},
      { "key": "room", "label": "ห้อง", "type": "text"},
      { "key": "capacity", "label": "จำนวนรับ", "type": "number" },
      { "key": "schedule_time", "label": "เวลา", "type": "datetime-local" } ] },
  "bookings": {
    "label": "การจอง",
    "api": "/api/bookings",
    "idKey": "booking_id",
    "search": [
      { "key": "name", "label": "ชื่อสมาชิก", "type": "text" },
      { "key": "class_id", "label": "รหัสคลาส", "type": "text" },
      { "key": "status", "label": "สถานะ", "type": "select",
        "options": [ "", "CONFIRMED", "CANCELLED" ] } ],
    "form": [
      { "key": "member_id", "label": "รหัสสมาชิก", "type": "text"},
      { "key": "class_id", "label": "รหัสคลาส", "type": "text"},
      { "key": "book_date", "label": "วันที่จอง", "type": "datetime-local" },
      { "key": "status", "label": "สถานะ", "type": "select",
        "options": [ "CONFIRMED", "CANCELLED" ] } ] }
  
};

let current = Object.keys(ENTITIES)[0];
let editingId = null;
const $ = (s) => document.querySelector(s);
function setStatus(el, msg, cls = "") { el.className = "status " + cls; el.textContent = msg; }
async function api(url, opts) { const res = await fetch(url, opts); return res.json(); }

async function refreshTrainerOptions() {
  const response = await api("/api/trainers");
  if (!response.ok) return;
  const trainerField = ENTITIES.classes.form.find(f => f.key === "trainer_id");
  trainerField.options = (response.data || []).map(trainer => ({
    value: trainer.trainer_id,
    label: trainer.name
  }));
}

async function refreshBookingOptions() {
  const [membersResponse, classesResponse] = await Promise.all([
    api(ENTITIES.members.api),
    api(ENTITIES.classes.api)
  ]);
  if (!membersResponse.ok || !classesResponse.ok) return;

  const memberOptions = (membersResponse.data || []).map(member => ({
    value: member.member_id,
    label: member.name
  }));
  const classOptions = (classesResponse.data || []).map(cls => ({
    value: cls.class_id,
    label: cls.name
  }));
  ENTITIES.bookings.search.find(f => f.key === "class_id").options = ["", ...classOptions];
  ENTITIES.bookings.form.find(f => f.key === "member_id").options = [
    { value: "", label: "เลือกสมาชิก" }, ...memberOptions
  ];
  ENTITIES.bookings.form.find(f => f.key === "class_id").options = [
    { value: "", label: "เลือกคลาส" }, ...classOptions
  ];
}

function fieldHtml(f, prefix, value = "") {
  let input;
  if (f.type === "select") {
    input = '<select id="' + prefix + f.key + '">' +
      f.options.map(o => {
        const option = typeof o === "object" ? o : { value: o, label: o || "ทั้งหมด" };
        return '<option value="' + option.value + '"' + (String(option.value) === String(value ?? "") ? " selected" : "") + '>' + option.label + '</option>';
      }).join("") + '</select>';
  } else { input = '<input id="' + prefix + f.key + '" type="' + f.type + '" value="' + (value ?? "") + '">'; }
  return '<div class="field"><label>' + f.label + '</label>' + input + '</div>';
}
async function buildSearch() {
  const cfg = ENTITIES[current];
  if (current === "bookings") await refreshBookingOptions();
  $("#searchTitle").textContent = cfg.label;
  $("#searchFields").innerHTML = cfg.search.map(f => fieldHtml(f, "s_")).join("");
}
async function doSearch() {
  const cfg = ENTITIES[current];
  const params = new URLSearchParams();
  cfg.search.forEach(f => { const v = $("#s_" + f.key).value; if (v) params.append(f.key, v); });
  setStatus($("#status"), "กำลังค้นหา...");
  renderTable(await api(cfg.api + "?" + params.toString()));
}
function renderTable(r) {
  const head = $("#tableHead"), body = $("#tableBody"), st = $("#status");
  head.innerHTML = ""; body.innerHTML = "";
  if (!r.ok) { setStatus(st, (r.todo ? "🚧 " : "⚠️ ") + r.error, r.todo ? "todo" : "err"); return; }
  const rows = r.data || [];
  if (rows.length === 0) { setStatus(st, "ไม่พบข้อมูล"); return; }
  setStatus(st, "พบ " + rows.length + " รายการ");
  const cols = Object.keys(rows[0]);
  head.innerHTML = cols.map(c => "<th>" + c + "</th>").join("") + "<th>จัดการ</th>";
  body.innerHTML = rows.map(row => {
    const id = row[ENTITIES[current].idKey];
    return "<tr>" + cols.map(c => "<td>" + (row[c] ?? "—") + "</td>").join("") +
      '<td><button class="btn sm" onclick="editRow(' + id + ')">แก้ไข</button> ' +
      '<button class="btn sm del" onclick="deleteRow(' + id + ')">ลบ</button></td></tr>';
  }).join("");
}
async function openForm(title, data = {}) {
  const cfg = ENTITIES[current];
  if (current === "classes") await refreshTrainerOptions();
  if (current === "bookings") await refreshBookingOptions();
  $("#modalTitle").textContent = title;
  $("#formFields").innerHTML = cfg.form.map(f => fieldHtml(f, "f_", data[f.key])).join("");
  $("#modal").classList.remove("hidden");
}
function collectForm() { const cfg = ENTITIES[current], d = {}; cfg.form.forEach(f => d[f.key] = $("#f_" + f.key).value); return d; }
async function editRow(id) {
  const cfg = ENTITIES[current];
  const r = await api(cfg.api + "/" + id);
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  editingId = id; openForm("แก้ไขข้อมูล", r.data);
}
async function deleteRow(id) {
  if (!confirm("ยืนยันการลบ?")) return;
  const r = await api(ENTITIES[current].api + "/" + id, { method: "DELETE" });
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  doSearch();
}
async function save() {
  const cfg = ENTITIES[current], data = collectForm();
  const opts = { method: editingId ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) };
  const r = await api(editingId ? cfg.api + "/" + editingId : cfg.api, opts);
  if (!r.ok) { alert((r.todo ? "🚧 " : "⚠️ ") + r.error); return; }
  $("#modal").classList.add("hidden"); doSearch();
}
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
  t.classList.add("active"); current = t.dataset.entity;
  buildSearch(); $("#tableHead").innerHTML = ""; $("#tableBody").innerHTML = "";
  setStatus($("#status"), 'กด "ค้นหา" เพื่อแสดงข้อมูล');
}));
$("#btnSearch").onclick = doSearch;
$("#btnClear").onclick = () => buildSearch();
$("#btnAdd").onclick = () => { editingId = null; openForm("เพิ่มข้อมูลใหม่"); };
$("#btnSave").onclick = save;
$("#btnCancel").onclick = () => $("#modal").classList.add("hidden");
buildSearch();
setStatus($("#status"), 'กด "ค้นหา" เพื่อแสดงข้อมูล');
