// ============================================================
//  report.js  —  ตรรกะหน้ารายงาน (ทำให้เสร็จแล้ว ★)
// ============================================================
const $ = (s) => document.querySelector(s);
async function api(url) { return (await fetch(url)).json(); }
function fillTable(tableSel, statusSel, r) {
  const t = $(tableSel), st = $(statusSel);
  const thead = t.querySelector("thead"), tbody = t.querySelector("tbody");
  thead.innerHTML = ""; tbody.innerHTML = "";
  if (!r.ok) { st.className = "status " + (r.todo ? "todo" : "err"); st.textContent = (r.todo ? "🚧 " : "⚠️ ") + r.error; return; }
  const rows = r.data || [];
  if (!rows.length) { st.className = "status"; st.textContent = "ไม่มีข้อมูล"; return; }
  st.textContent = "";
  const cols = Object.keys(rows[0]);
  thead.innerHTML = "<tr>" + cols.map(c => "<th>" + c + "</th>").join("") + "</tr>";
  tbody.innerHTML = rows.map(row => "<tr>" + cols.map(c => "<td>" + (row[c] ?? "—") + "</td>").join("") + "</tr>").join("");
}
async function loadSummary() {
  const r = await api("/api/reports/summary");
  if (!r.ok) return;
  const d = r.data || {};
  if (d.members !== undefined) $("#m_mem").textContent = d.members;
  if (d.classes !== undefined) $("#m_cls").textContent = d.classes;
  if (d.trainers !== undefined) $("#m_trn").textContent = d.trainers;
  if (d.bookings !== undefined) $("#m_bok").textContent = d.bookings;
}
async function loadAll() {
  loadSummary();
  fillTable("#popularTable", "#popularStatus", await api("/api/reports/popular-classes"));
  fillTable("#trainersTable", "#trainersStatus", await api("/api/reports/top-trainers"));
  fillTable("#equipTable", "#equipStatus", await api("/api/reports/class-equipment"));
}
loadAll();
