// ============================================================
//  app.js  —  ตรรกะหน้าเว็บ (ทำให้เสร็จแล้ว ★ นิสิตไม่ต้องแก้)
//  ปรับช่องค้นหา/ฟอร์มได้ที่ตัวแปร ENTITIES ด้านล่าง
// ============================================================
// value = ค่าที่เก็บใน database (ต้องตรงกับ ENUM), label = ข้อความที่แสดงบนหน้าจอ
const GENDERS = [{ "value": "female", "label": "หญิง" },
{ "value": "male", "label": "ชาย" },
{ "value": "non_binary", "label": "นอนไบนารี" },
{ "value": "not_specified", "label": "ไม่ระบุ" }];
const ROOMS = [
  { "value": "room a", "label": "room a" },
  { "value": "room b", "label": "room b" },
  { "value": "studio 1", "label": "studio 1" },
  { "value": "studio 2", "label": "studio 2" },
  { "value": "studio 3", "label": "studio 3" }
];
const EQUIPMENT_ZONES = [
  { "value": "free weight", "label": "free Weight" },
  { "value": "studio  zone", "label": "studio  Zone" },
  { "value": "cardio zone", "label": "cardio Zone" }
];

const ENTITIES = {
  "members": {
    "label": "สมาชิก",
    "api": "/api/members",
    "idKey": "member_id",
    "search": [
      { "key": "name", "label": "ชื่อ", "type": "text" },
      {
        "key": "gender", "label": "เพศ", "type": "select",
        "options": [{ "value": "", "label": "ทั้งหมด" }, ...GENDERS]
      },
      {
        "key": "package_type", "label": "แพ็กเกจ", "type": "select",
        "options": ["", "Regular", "Vip"]
      }],
    "form": [
      { "key": "name", "label": "ชื่อ", "type": "text" },
      {
        "key": "gender", "label": "เพศ", "type": "select",
        "options": ["male", "female", "non_binary", "not_specified"]
      },
      { "key": "join_date", "label": "วันที่สมัคร", "type": "date" },
      {
        "key": "package_type", "label": "แพ็กเกจ", "type": "select",
        "options": ["Regular", "Vip"]
      },
      { "key": "referred_id", "label": "แนะนำโดย", "type": "select",
        "options": [{ "value": "", "label": "ไม่มีผู้แนะนำ" }]
       }]
  },
  "classes": {
    "label": "คลาสเรียน",
    "api": "/api/classes",
    "idKey": "class_id",
    "search": [
      { "key": "name", "label": "ชื่อคลาส", "type": "text" },
      { "key": "room", "label": "ห้อง", "type": "select", "options": [{ "value": "", "label": "ทั้งหมด" }, ...ROOMS] }],
    "form": [
      { "key": "name", "label": "ชื่อคลาส", "type": "text" },
      { "key": "trainer_id", "label": "เทรนเนอร์", "type": "select", "options": [{ "value": "", "label": "เลือกเทรนเนอร์" }] },
      { "key": "room", "label": "ห้อง", "type": "select", "options": [{ "value": "", "label": "เลือกห้อง" }, ...ROOMS] },
      { "key": "capacity", "label": "จำนวนรับ", "type": "number", "min": 1 },
      { "key": "schedule_time", "label": "เวลา", "type": "date" }]
  },
  "bookings": {
    "label": "การจอง",
    "api": "/api/bookings",
    "idKey": "booking_id",
    "search": [
      { "key": "name", "label": "ชื่อสมาชิก", "type": "text" },
      { "key": "class_name", "label": "ชื่อคลาส", "type": "select", "options": [""] },
      {
        "key": "status", "label": "สถานะ", "type": "select",
        "options": ["", "CONFIRMED", "CANCELLED"]
      }],
    "form": [
      { "key": "member_id", "label": "สมาชิก", "type": "select", "options": [{ "value": "", "label": "เลือกสมาชิก" }] },
      { "key": "class_id", "label": "คลาส", "type": "select", "options": [{ "value": "", "label": "เลือกคลาส" }] },
      { "key": "book_date", "label": "วันที่จอง", "type": "date" },
      {
        "key": "status", "label": "สถานะ", "type": "select",
        "options": ["CONFIRMED", "CANCELLED"]
      }]
  },
  "trainers": {
    "label": "เทรนเนอร์", "api": "/api/trainers", "idKey": "trainer_id",
    "search": [
      { "key": "name", "label": "ชื่อเทรนเนอร์", "type": "text" },
      { "key": "specialty", "label": "ความเชี่ยวชาญ", "type": "text" }
    ],
    "form": [
      { "key": "name", "label": "ชื่อเทรนเนอร์", "type": "text" },
      { "key": "specialty", "label": "ความเชี่ยวชาญ", "type": "text" },
      { "key": "phone", "label": "เบอร์โทรศัพท์", "type": "tel" }
    ]
  },
  "equipment": {
    "label": "อุปกรณ์", "api": "/api/equipment", "idKey": "equip_id",
    "search": [
      { "key": "name", "label": "ชื่ออุปกรณ์", "type": "text" },
      { "key": "zone", "label": "พื้นที่", "type": "select", "options": [{ "value": "", "label": "ทั้งหมด" }, ...EQUIPMENT_ZONES] },
      { "key": "status", "label": "สถานะ", "type": "select", "options": ["", "available", "unavailable"] }
    ],
    "form": [
      { "key": "name", "label": "ชื่ออุปกรณ์", "type": "text" },
      { "key": "zone", "label": "พื้นที่", "type": "select", "options": [{ "value": "", "label": "ทั้งหมด" }, ...EQUIPMENT_ZONES] },
      { "key": "status", "label": "สถานะ", "type": "select", "options": ["available", "unavailable"] },
      { "key": "total_quantity", "label": "จำนวนทั้งหมด", "type": "number", "min": 0 }
    ]
  },
  "class_equipment": {
    "label": "อุปกรณ์ประจำคลาส", "api": "/api/class-equipment", "idKey": "link_id", "hideId": true,
    "search": [
      { "key": "class_name", "label": "คลาส", "type": "select", "options": [{ "value": "", "label": "ทุกคลาส" }] },
      { "key": "equipment_name", "label": "อุปกรณ์", "type": "select", "options": [{ "value": "", "label": "ทุกอุปกรณ์" }] }
    ],
    "form": [
      { "key": "class_id", "label": "คลาส", "type": "select", "required": true, "options": [{ "value": "", "label": "เลือกคลาส" }] },
      { "key": "equip_id", "label": "อุปกรณ์", "type": "select", "required": true, "options": [{ "value": "", "label": "เลือกอุปกรณ์" }] },
      { "key": "quantity", "label": "จำนวนที่ใช้", "type": "number", "min": 1, "required": true }
    ]
  }
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

async function refreshClassEquipmentOptions() {
  const [classesResponse, equipmentResponse] = await Promise.all([
    api(ENTITIES.classes.api), api(ENTITIES.equipment.api)
  ]);
  if (!classesResponse.ok || !equipmentResponse.ok) return;
  const classes = (classesResponse.data || []).map(cls => ({ value: cls.class_id, label: cls.name }));
  const equipment = (equipmentResponse.data || []).map(item => ({ value: item.equip_id, label: item.name }));
  ENTITIES.class_equipment.search.find(f => f.key === "class_name").options = [
    { value: "", label: "ทุกคลาส" }, ...classes.map(item => ({ value: item.label, label: item.label }))
  ];
  ENTITIES.class_equipment.search.find(f => f.key === "equipment_name").options = [
    { value: "", label: "ทุกอุปกรณ์" }, ...equipment.map(item => ({ value: item.label, label: item.label }))
  ];
  ENTITIES.class_equipment.form.find(f => f.key === "class_id").options = [
    { value: "", label: "เลือกคลาส" }, ...classes
  ];
  ENTITIES.class_equipment.form.find(f => f.key === "equip_id").options = [
    { value: "", label: "เลือกอุปกรณ์" }, ...equipment
  ];
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
  const classNameOptions = (classesResponse.data || []).map(cls => ({
    value: cls.name,
    label: cls.name
  }));
  ENTITIES.bookings.search.find(f => f.key === "class_name").options = ["", ...classNameOptions];
  ENTITIES.bookings.form.find(f => f.key === "member_id").options = [
    { value: "", label: "เลือกสมาชิก" }, ...memberOptions
  ];
  ENTITIES.bookings.form.find(f => f.key === "class_id").options = [
    { value: "", label: "เลือกคลาส" }, ...classOptions
  ];
}

async function refreshMemberOptions() {
  const response = await api(ENTITIES.members.api);
  if (!response.ok) return;
  const field = ENTITIES.members.form.find(f => f.key === "referred_id");
  field.options = [
    { value: "", label: "ไม่มีผู้แนะนำ" },
    ...(response.data || []).filter(member => String(member.member_id) !== String(editingId)).map(member => ({
      value: member.member_id,
      label: member.name + " (#" + member.member_id + ")"
    }))
  ];
}

function fieldHtml(f, prefix, value = "") {
  let input;
  const required = f.required ? " required" : "";
  if (f.type === "select") {
    input = '<select id="' + prefix + f.key + '"' + required + '>' +
      f.options.map(o => {
        const option = typeof o === "object" ? o : { value: o, label: o || "ทั้งหมด" };
        return '<option value="' + option.value + '"' + (String(option.value) === String(value ?? "") ? " selected" : "") + '>' + option.label + '</option>';
      }).join("") + '</select>';
  } else {
    const min = f.min !== undefined ? ' min="' + f.min + '" step="1"' : "";
    input = '<input id="' + prefix + f.key + '" type="' + f.type + '"' + min + required + ' value="' + (value ?? "") + '">';
  }
  return '<div class="field"><label>' + f.label + '</label>' + input + '</div>';
}
async function buildSearch() {
  const cfg = ENTITIES[current];
  if (current === "bookings") await refreshBookingOptions();
  if (current === "class_equipment") await refreshClassEquipmentOptions();
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
  if (current === "trainers") {
    const idKey = ENTITIES.trainers.idKey;
    cols.splice(cols.indexOf(idKey), 1);
    cols.unshift(idKey);
  }
  if (current === "classes") {
    const classOrder = ["class_id", "name", "room", "trainer_name", "schedule_time", "capacity", "remain"];
    cols.splice(0, cols.length, ...classOrder.filter(column => cols.includes(column)));
  }
  if (current === "members") {
    const memberOrder = ["member_id", "name", "gender", "join_date", "package_type", "referred_id"];
    cols.splice(0, cols.length, ...memberOrder.filter(column => cols.includes(column)));
  }
  if (current === "bookings") {
    const bookingOrder = ["booking_id", "member_name", "class_name", "book_date", "status"];
    cols.splice(0, cols.length, ...bookingOrder.filter(column => cols.includes(column)));
  }
  if (current === "class_equipment") {
    const assignmentOrder = ["class_name", "equipment_name", "quantity"];
    cols.splice(0, cols.length, ...assignmentOrder.filter(column => cols.includes(column)));
  }
  if (current === "equipment") {
    const equipmentOrder = ["equip_id", "name", "zone", "total_quantity", "remain", "status"];
    cols.splice(0, cols.length, ...equipmentOrder.filter(column => cols.includes(column)));
  }
  head.innerHTML = cols.map(c => "<th>" + c + "</th>").join("") + "<th>จัดการ</th>";
  body.innerHTML = rows.map(row => {
    const id = row[ENTITIES[current].idKey];
    const idArg = typeof id === "string" ? "'" + id + "'" : id;
    return "<tr>" + cols.map(c => "<td>" + (row[c] ?? "—") + "</td>").join("") +
      '<td><button class="btn sm" onclick="editRow(' + idArg + ')">แก้ไข</button> ' +
      '<button class="btn sm del" onclick="deleteRow(' + idArg + ')">ลบ</button></td></tr>';
  }).join("");
}
async function openForm(title, data = {}) {
  const cfg = ENTITIES[current];
  if (current === "members") await refreshMemberOptions();
  if (current === "classes") await refreshTrainerOptions();
  if (current === "bookings") await refreshBookingOptions();
  if (current === "class_equipment") await refreshClassEquipmentOptions();
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
  for (const field of cfg.form) {
    const input = $("#f_" + field.key);
    if (!input.checkValidity()) { input.reportValidity(); return; }
  }
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
