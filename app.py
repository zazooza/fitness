# ============================================================
#  app.py — เว็บแอป Flask (ทำให้เสร็จแล้ว ★ ไม่ต้องแก้)
#  รัน:  python app.py  แล้วเปิด http://127.0.0.1:5000
# ============================================================
from flask import Flask, request, jsonify, render_template
from datetime import date, datetime
import db

app = Flask(__name__)


def json_safe(value):
    """แปลงวันที่เป็น YYYY-MM-DD ก่อนส่ง JSON เพื่อไม่ให้ Flask เติมเวลา/GMT"""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def safe(fn, *args, **kwargs):
    try:
        return jsonify({"ok": True, "data": json_safe(fn(*args, **kwargs))})
    except NotImplementedError as e:
        return jsonify({"ok": False, "todo": True, "error": str(e)}), 501
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500


@app.route("/")
def page_home():
    return render_template("index.html")

@app.route("/report")
def page_report():
    return render_template("report.html")


# ---- สมาชิก ----
@app.route("/api/members", methods=["GET"])
def members_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_members, filters)

@app.route("/api/members/<int:_id>", methods=["GET"])
def member_get(_id):
    return safe(db.get_member, _id)

@app.route("/api/members", methods=["POST"])
def member_create():
    return safe(db.create_member, request.json)

@app.route("/api/members/<int:_id>", methods=["PUT"])
def member_update(_id):
    return safe(db.update_member, _id, request.json)

@app.route("/api/members/<int:_id>", methods=["DELETE"])
def member_delete(_id):
    return safe(db.delete_member, _id)

# ---- คลาสเรียน ----
@app.route("/api/trainers", methods=["GET"])
def trainers_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_trainers, filters)

@app.route("/api/trainers", methods=["POST"])
def trainer_create():
    return safe(db.create_trainer, request.json)

@app.route("/api/trainers/<int:_id>", methods=["GET"])
def trainer_get(_id):
    return safe(db.get_trainer, _id)

@app.route("/api/trainers/<int:_id>", methods=["PUT"])
def trainer_update(_id):
    return safe(db.update_trainer, _id, request.json)

@app.route("/api/trainers/<int:_id>", methods=["DELETE"])
def trainer_delete(_id):
    return safe(db.delete_trainer, _id)

@app.route("/api/classes", methods=["GET"])
def classes_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_classes, filters)

@app.route("/api/classes/<int:_id>", methods=["GET"])
def class_get(_id):
    return safe(db.get_class, _id)

@app.route("/api/classes", methods=["POST"])
def class_create():
    return safe(db.create_class, request.json)

@app.route("/api/classes/<int:_id>", methods=["PUT"])
def class_update(_id):
    return safe(db.update_class, _id, request.json)

@app.route("/api/classes/<int:_id>", methods=["DELETE"])
def class_delete(_id):
    return safe(db.delete_class, _id)

# ---- อุปกรณ์ ----
@app.route("/api/equipment", methods=["GET"])
def equipment_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_equipment, filters)

@app.route("/api/equipment/<int:_id>", methods=["GET"])
def equipment_get(_id):
    return safe(db.get_equipment, _id)

@app.route("/api/equipment", methods=["POST"])
def equipment_create():
    return safe(db.create_equipment, request.json)

@app.route("/api/equipment/<int:_id>", methods=["PUT"])
def equipment_update(_id):
    return safe(db.update_equipment, _id, request.json)

@app.route("/api/equipment/<int:_id>", methods=["DELETE"])
def equipment_delete(_id):
    return safe(db.delete_equipment, _id)

# ---- อุปกรณ์ที่ใช้ในแต่ละคลาส ----
@app.route("/api/class-equipment", methods=["GET"])
def class_equipment_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_class_equipment, filters)

def parse_class_equipment_id(link_id):
    try:
        class_id, equip_id = link_id.split("-", 1)
        return int(class_id), int(equip_id)
    except (ValueError, AttributeError):
        raise ValueError("รหัสรายการอุปกรณ์ประจำคลาสไม่ถูกต้อง")

@app.route("/api/class-equipment", methods=["POST"])
def class_equipment_create():
    return safe(db.create_class_equipment, request.get_json(silent=True) or {})

@app.route("/api/class-equipment/<link_id>", methods=["GET"])
def class_equipment_get(link_id):
    try:
        class_id, equip_id = parse_class_equipment_id(link_id)
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    return safe(db.get_class_equipment, class_id, equip_id)

@app.route("/api/class-equipment/<link_id>", methods=["PUT"])
def class_equipment_update(link_id):
    try:
        class_id, equip_id = parse_class_equipment_id(link_id)
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    return safe(db.update_class_equipment, class_id, equip_id, request.get_json(silent=True) or {})

@app.route("/api/class-equipment/<link_id>", methods=["DELETE"])
def class_equipment_delete(link_id):
    try:
        class_id, equip_id = parse_class_equipment_id(link_id)
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    return safe(db.delete_class_equipment, class_id, equip_id)

# ---- การจอง ----
@app.route("/api/bookings", methods=["GET"])
def bookings_list():
    filters = {k: v for k, v in request.args.items() if v}
    return safe(db.search_bookings, filters)

@app.route("/api/bookings/<int:_id>", methods=["GET"])
def booking_get(_id):
    return safe(db.get_booking, _id)

@app.route("/api/bookings", methods=["POST"])
def booking_create():
    return safe(db.create_booking, request.json)

@app.route("/api/bookings/<int:_id>", methods=["PUT"])
def booking_update(_id):
    return safe(db.update_booking, _id, request.json)

@app.route("/api/bookings/<int:_id>", methods=["DELETE"])
def booking_delete(_id):
    return safe(db.delete_booking, _id)


@app.route("/api/reports/summary")
def report_summary():
    return safe(db.report_summary)

@app.route("/api/reports/popular-classes")
def route_report_popular_classes():
    return safe(db.report_popular_classes)

@app.route("/api/reports/top-trainers")
def route_report_trainers_above_avg():
    return safe(db.report_trainers_above_avg)

@app.route("/api/reports/class-equipment")
def route_report_class_equipment():
    return safe(db.report_class_equipment)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
