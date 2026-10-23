# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#  มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# ============================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


def blank_to_none(value):
    return value if value != "" else None


def require_integer(value, label, minimum):
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label}ต้องเป็นจำนวนเต็มตั้งแต่ {minimum} ขึ้นไป")
    if str(value).strip() != str(number) and not isinstance(value, int):
        raise ValueError(f"{label}ต้องเป็นจำนวนเต็มตั้งแต่ {minimum} ขึ้นไป")
    if number < minimum:
        raise ValueError(f"{label}ต้องมีค่าอย่างน้อย {minimum}")
    return number


def _todo(name):
    raise NotImplementedError(f"TODO: ยังไม่ได้เขียนฟังก์ชัน {name} ใน db.py")

def list_trainers():
    sql = "SELECT * FROM trainer ORDER BY trainer_id"
    return run_query(sql)



# ---------- สมาชิก (member) ----------
def search_members(filters):
    """ค้นหา สมาชิก ตามเงื่อนไข (name, gender, package_type)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM member WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    sql = "SELECT * FROM member WHERE 1=1"
    params = []

    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("gender"):
        sql += " AND gender = %s"
        params.append(filters["gender"])

    if filters.get("package_type"):
        sql += " AND package_type = %s"
        params.append(filters["package_type"])

    sql += " ORDER BY member_id"
    return run_query(sql, params)


def get_member(member_id):
    """ดึง สมาชิก 1 รายการตาม member_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    rows = run_query("SELECT * FROM member WHERE member_id = %s", (member_id,))
    return rows[0] if rows else None


def create_member(data):
    """เพิ่ม สมาชิก ใหม่ — data มีคีย์: name, gender, join_date, package_type,referred_id"""
    sql = """INSERT INTO member (name, gender, join_date, package_type, referred_id)
                 VALUES (%s, %s, %s, %s, %s)"""
    return run_command(
    sql,
    (
        data["name"],
        data["gender"],
        data["join_date"],
        blank_to_none(data["package_type"]),
        blank_to_none(data["referred_id"])
    )
)


def update_member(member_id, data):
    """แก้ไข สมาชิก ตาม member_id"""
    sql = """UPDATE member
                 SET name = %s, gender = %s, join_date = %s, package_type = %s, referred_id = %s
                 WHERE member_id = %s"""
    return run_command(sql, (data["name"], data["gender"], (data["join_date"]),
                             blank_to_none(data["package_type"]), blank_to_none(data["referred_id"]), member_id))


def delete_member(member_id):
    """ลบ สมาชิก ตาม member_id"""
    return run_command("DELETE FROM member WHERE member_id = %s", (member_id,))

# ---------- คลาสเรียน (gym_class) ----------
def search_classes(filters):
    """ค้นหา คลาสเรียน ตามเงื่อนไข (name, room)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM gym_class WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    sql = """
        SELECT c.class_id, c.name, c.room, t.name AS trainer_name,
               c.schedule_time, c.capacity,
               GREATEST(c.capacity - (
                   SELECT COUNT(*)
                   FROM booking b
                   WHERE b.class_id = c.class_id AND b.status = 'CONFIRMED'
               ), 0) AS remain
        FROM gym_class c
        INNER JOIN trainer t ON c.trainer_id = t.trainer_id
        WHERE 1=1
    """
    params = []
    
    if filters.get("name"):
            sql += " AND c.name LIKE %s"
            params.append("%" + filters["name"] + "%")
    
    if filters.get("room"):
            sql += " AND LOWER(REPLACE(c.room, ' ', '')) LIKE %s"
            normalized_room = filters["room"].replace(" ", "").lower()
            params.append("%" + normalized_room + "%")
    
    sql += " ORDER BY c.class_id"
    return run_query(sql, params)


def get_class(class_id):
    """ดึง คลาสเรียน 1 รายการตาม class_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    sql = """SELECT class_id, trainer_id, name, room, capacity,
                    schedule_time
             FROM gym_class WHERE class_id = %s"""
    rows = run_query(sql, (class_id,))
    return rows[0] if rows else None


def create_class(data):
    """เพิ่ม คลาสเรียน ใหม่ — data มีคีย์: name, trainer_id, room, capacity, schedule_time"""
    sql = """
        INSERT INTO gym_class
            (name, trainer_id, room, capacity, schedule_time)
        VALUES (%s, %s, %s, %s, %s)
    """
    capacity = require_integer(data.get("capacity"), "จำนวนรับ", 1)
    return run_command(
        sql,
        (
            data["name"],
            data["trainer_id"],
            blank_to_none(data["room"]),
            capacity,
            data["schedule_time"]
        )
    )

def update_class(class_id, data):
    """แก้ไข คลาสเรียน ตาม class_id"""
    capacity = require_integer(data.get("capacity"), "จำนวนรับ", 1)
    sql = """UPDATE gym_class
                 SET name = %s, trainer_id = %s, room = %s, capacity = %s, schedule_time = %s
                 WHERE class_id = %s"""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        cur.execute("SELECT class_id FROM gym_class WHERE class_id = %s FOR UPDATE", (class_id,))
        if not cur.fetchone():
            raise ValueError("ไม่พบคลาสที่ต้องการแก้ไข")
        cur.execute(
            "SELECT COUNT(*) AS total FROM booking WHERE class_id = %s AND status = 'CONFIRMED'",
            (class_id,)
        )
        confirmed_count = cur.fetchone()["total"]
        if capacity < confirmed_count:
            raise ValueError(f"จำนวนรับลดไม่ได้ต่ำกว่าจำนวนที่จองยืนยันแล้ว ({confirmed_count} คน)")
        cur.execute(sql, (data["name"], data["trainer_id"], blank_to_none(data["room"]), capacity, data["schedule_time"], class_id))
        conn.commit()
        return {"new_id": cur.lastrowid, "affected": cur.rowcount}
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def delete_class(class_id):
    """ลบ คลาสเรียน ตาม class_id"""
    return run_command("DELETE FROM gym_class WHERE class_id = %s", (class_id,))

# ---------- การจอง (booking) ----------
def search_bookings(filters):
    """ค้นหาการจองด้วยชื่อสมาชิก ชื่อคลาส และสถานะ"""
    sql = """
        SELECT b.booking_id, m.name AS member_name, c.name AS class_name,
               b.book_date, b.status
        FROM booking b
        INNER JOIN member m ON b.member_id = m.member_id
        INNER JOIN gym_class c ON b.class_id = c.class_id
        WHERE 1=1
    """
    params = []

    if filters.get("name"):
        sql += " AND m.name LIKE %s"
        params.append("%" + filters["name"] + "%")

    if filters.get("class_name"):
        sql += " AND c.name LIKE %s"
        params.append("%" + filters["class_name"] + "%")

    if filters.get("status"):
        sql += " AND b.status = %s"
        params.append(filters["status"])
    sql += " ORDER BY b.booking_id"
    return run_query(sql, params)


def get_booking(booking_id):
    """ดึง การจอง 1 รายการตาม booking_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    sql = """SELECT booking_id, member_id, class_id,
                    book_date, status
             FROM booking WHERE booking_id = %s"""
    rows = run_query(sql, (booking_id,))
    return rows[0] if rows else None


def save_booking_with_capacity(sql, params, class_id, status, exclude_booking_id=None):
    """Serialize confirmed bookings per class so capacity cannot be exceeded."""
    class_id = require_integer(class_id, "คลาส", 1)
    status = (status or "CONFIRMED").strip().upper()
    if status not in {"CONFIRMED", "CANCELLED"}:
        raise ValueError("สถานะการจองต้องเป็น CONFIRMED หรือ CANCELLED")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        cur.execute("SELECT capacity FROM gym_class WHERE class_id = %s FOR UPDATE", (class_id,))
        class_row = cur.fetchone()
        if not class_row:
            raise ValueError("ไม่พบคลาสที่เลือก")

        if status == "CONFIRMED":
            count_sql = "SELECT COUNT(*) AS total FROM booking WHERE class_id = %s AND status = 'CONFIRMED'"
            count_params = [class_id]
            if exclude_booking_id is not None:
                count_sql += " AND booking_id <> %s"
                count_params.append(exclude_booking_id)
            cur.execute(count_sql, tuple(count_params))
            confirmed_count = cur.fetchone()["total"]
            if confirmed_count >= class_row["capacity"]:
                raise ValueError("คลาสเต็มแล้ว ไม่สามารถยืนยันการจองเพิ่มได้")

        cur.execute(sql, params)
        conn.commit()
        return {"new_id": cur.lastrowid, "affected": cur.rowcount}
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def create_booking(data):
    """เพิ่ม การจอง ใหม่ — data มีคีย์: member_id, class_id, book_date, status"""
    sql = """
            INSERT INTO booking
                (member_id, class_id, book_date, status)
            VALUES (%s, %s, %s, %s)
        """
    member_id = require_integer(data.get("member_id"), "สมาชิก", 1)
    class_id = require_integer(data.get("class_id"), "คลาส", 1)
    status = (data.get("status") or "CONFIRMED").strip().upper()
    params = (member_id, class_id, data.get("book_date"), status)
    return save_booking_with_capacity(sql, params, class_id, status)

def update_booking(booking_id, data):
    """แก้ไข การจอง ตาม booking_id"""
    sql = """UPDATE booking
                     SET member_id = %s, class_id = %s, book_date = %s, status = %s
                     WHERE booking_id = %s"""
    member_id = require_integer(data.get("member_id"), "สมาชิก", 1)
    class_id = require_integer(data.get("class_id"), "คลาส", 1)
    status = (data.get("status") or "CONFIRMED").strip().upper()
    params = (member_id, class_id, data.get("book_date"), status, booking_id)
    return save_booking_with_capacity(sql, params, class_id, status, booking_id)


def delete_booking(booking_id):
    """ลบ การจอง ตาม booking_id"""
    return run_command("DELETE FROM booking WHERE booking_id = %s", (booking_id,))


# ============================================================
# Trainer (เทรนเนอร์)
# ============================================================
def search_trainers(filters):
    sql = "SELECT trainer_id, name, specialty, phone FROM trainer WHERE 1=1"
    params = []
    if filters.get("name"):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("specialty"):
        sql += " AND specialty LIKE %s"
        params.append(f"%{filters['specialty']}%")
    return run_query(sql, params)

def get_trainer(_id):
    sql = "SELECT trainer_id, name, specialty, phone FROM trainer WHERE trainer_id = %s"
    res = run_query(sql, (_id,))
    return res[0] if res else None

def create_trainer(data):
    sql = "INSERT INTO trainer (name, specialty, phone) VALUES (%s, %s, %s)"
    return run_command(sql, (data.get("name"), data.get("specialty"), data.get("phone")))

def update_trainer(_id, data):
    sql = "UPDATE trainer SET name = %s, specialty = %s, phone = %s WHERE trainer_id = %s"
    return run_command(sql, (data.get("name"), data.get("specialty"), data.get("phone"), _id))

def delete_trainer(_id):
    sql = "DELETE FROM trainer WHERE trainer_id = %s"
    return run_command(sql, (_id,))


# ============================================================
# Equipment (อุปกรณ์)
# ============================================================
def search_equipment(filters):
    sql = """SELECT e.equip_id, e.name, e.zone, e.total_quantity,
                    GREATEST(e.total_quantity - COALESCE(assigned.quantity, 0), 0) AS remain,
                    CASE WHEN LOWER(e.status) = 'maintenance' THEN 'unavailable' ELSE LOWER(e.status) END AS status
             FROM equipment e
             LEFT JOIN (
                 SELECT equip_id, SUM(quantity) AS quantity
                 FROM class_equipment
                 GROUP BY equip_id
             ) assigned ON assigned.equip_id = e.equip_id
             WHERE 1=1"""
    params = []
    if filters.get("name"):
        sql += " AND e.name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get("zone"):
        sql += " AND e.zone LIKE %s"
        params.append(f"%{filters['zone']}%")
    if filters.get("status"):
        sql += " AND CASE WHEN LOWER(e.status) = 'maintenance' THEN 'unavailable' ELSE LOWER(e.status) END = %s"
        params.append(filters["status"])
    return run_query(sql, params)

def get_equipment(_id):
    sql = """SELECT e.equip_id, e.name, e.zone, e.total_quantity,
                    GREATEST(e.total_quantity - COALESCE(assigned.quantity, 0), 0) AS remain,
                    CASE WHEN LOWER(e.status) = 'maintenance' THEN 'unavailable' ELSE LOWER(e.status) END AS status
             FROM equipment e
             LEFT JOIN (
                 SELECT equip_id, SUM(quantity) AS quantity
                 FROM class_equipment
                 GROUP BY equip_id
             ) assigned ON assigned.equip_id = e.equip_id
             WHERE e.equip_id = %s"""
    res = run_query(sql, (_id,))
    return res[0] if res else None

def create_equipment(data):
    sql = "INSERT INTO equipment (name, zone, status, total_quantity) VALUES (%s, %s, %s, %s)"
    qty = require_integer(data.get("total_quantity", 0) or 0, "จำนวนอุปกรณ์", 0)
    status = normalize_equipment_status(data.get("status"))
    return run_command(sql, (data.get("name"), data.get("zone"), status, qty))

def update_equipment(_id, data):
    sql = "UPDATE equipment SET name = %s, zone = %s, status = %s, total_quantity = %s WHERE equip_id = %s"
    qty = require_integer(data.get("total_quantity", 0) or 0, "จำนวนอุปกรณ์", 0)
    status = normalize_equipment_status(data.get("status"))
    return run_command(sql, (data.get("name"), data.get("zone"), status, qty, _id))

def delete_equipment(_id):
    sql = "DELETE FROM equipment WHERE equip_id = %s"
    return run_command(sql, (_id,))


def normalize_equipment_status(value):
    status = (value or "available").strip().lower()
    if status == "maintenance":
        status = "unavailable"
    if status not in {"available", "unavailable"}:
        raise ValueError("สถานะอุปกรณ์ต้องเป็น available หรือ unavailable")
    return status


# ---------- อุปกรณ์ที่ใช้ในแต่ละคลาส (class_equipment) ----------
def search_class_equipment(filters):
    sql = """SELECT CONCAT(ce.class_id, '-', ce.equip_id) AS link_id,
                    ce.class_id, ce.equip_id, c.name AS class_name,
                    e.name AS equipment_name, ce.quantity
             FROM class_equipment ce
             INNER JOIN gym_class c ON c.class_id = ce.class_id
             INNER JOIN equipment e ON e.equip_id = ce.equip_id
             WHERE 1=1"""
    params = []
    if filters.get("class_name"):
        sql += " AND c.name LIKE %s"
        params.append("%" + filters["class_name"] + "%")
    if filters.get("equipment_name"):
        sql += " AND e.name LIKE %s"
        params.append("%" + filters["equipment_name"] + "%")
    sql += " ORDER BY ce.class_id, ce.equip_id"
    return run_query(sql, params)


def get_class_equipment(class_id, equip_id):
    rows = run_query(
        "SELECT class_id, equip_id, quantity FROM class_equipment WHERE class_id = %s AND equip_id = %s",
        (class_id, equip_id)
    )
    return rows[0] if rows else None


def _validate_class_equipment(data):
    class_id = require_integer(data.get("class_id"), "คลาส", 1)
    equip_id = require_integer(data.get("equip_id"), "อุปกรณ์", 1)
    quantity = require_integer(data.get("quantity"), "จำนวนที่ใช้", 1)
    rows = run_query("SELECT total_quantity FROM equipment WHERE equip_id = %s", (equip_id,))
    if not rows:
        raise ValueError("ไม่พบอุปกรณ์ที่เลือก")
    if not run_query("SELECT class_id FROM gym_class WHERE class_id = %s", (class_id,)):
        raise ValueError("ไม่พบคลาสที่เลือก")
    if quantity > rows[0]["total_quantity"]:
        raise ValueError(f"จำนวนที่ใช้เกินจำนวนอุปกรณ์ทั้งหมด ({rows[0]['total_quantity']})")
    return class_id, equip_id, quantity


def create_class_equipment(data):
    class_id, equip_id, quantity = _validate_class_equipment(data)
    if get_class_equipment(class_id, equip_id):
        raise ValueError("คลาสนี้มีรายการอุปกรณ์ดังกล่าวแล้ว กรุณาแก้ไขรายการเดิม")
    return run_command(
        "INSERT INTO class_equipment (class_id, equip_id, quantity) VALUES (%s, %s, %s)",
        (class_id, equip_id, quantity)
    )


def update_class_equipment(old_class_id, old_equip_id, data):
    class_id, equip_id, quantity = _validate_class_equipment(data)
    if not get_class_equipment(old_class_id, old_equip_id):
        raise ValueError("ไม่พบรายการอุปกรณ์ประจำคลาสที่ต้องการแก้ไข")
    if (class_id, equip_id) != (int(old_class_id), int(old_equip_id)) and get_class_equipment(class_id, equip_id):
        raise ValueError("คลาสนี้มีรายการอุปกรณ์ดังกล่าวแล้ว")
    return run_command(
        "UPDATE class_equipment SET class_id = %s, equip_id = %s, quantity = %s WHERE class_id = %s AND equip_id = %s",
        (class_id, equip_id, quantity, old_class_id, old_equip_id)
    )


def delete_class_equipment(class_id, equip_id):
    return run_command(
        "DELETE FROM class_equipment WHERE class_id = %s AND equip_id = %s",
        (class_id, equip_id)
    )



# ============================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
# ============================================================
def report_summary():
    """ตัวเลขสรุปบนการ์ด dashboard — คืน dict เช่น {"members": 10, ...}
    คำใบ้: ใช้ COUNT(*) หลายครั้ง"""
    sql = """
            select 
                    (select count(*)    from    `member`    )       as  'members'           ,
                    (select count(*)    from     trainer    )       as  'trainers'          ,
                    (select count(*)    from     gym_class  )       as  'classes'           ,
                    (select count(*)    from booking where status = 'CONFIRMED') as 'bookings',
                    (select count(*)    from     equipment  )       as  'equipment'         ,
                    (select coalesce(sum(total_quantity), 0)
                     from equipment where LOWER(status) = 'available') as 'available_equipment'
    """
    return run_query(sql)[0]

def report_popular_classes():
    """📈 คลาสยอดนิยม (Most Booked)
    คำใบ้: JOIN booking→gym_class, GROUP BY class, COUNT, ORDER BY DESC, LIMIT 5"""
    sql = """
        SELECT 
            c.name AS 'ชื่อคลาส'          ,
            c.room AS 'ห้อง'             ,
            COUNT(b.booking_id)         AS 'จำนวนการจอง'
        FROM booking b
        INNER JOIN gym_class c ON b.class_id = c.class_id
        WHERE b.status = 'CONFIRMED'
        GROUP BY c.class_id, c.name, c.room
        ORDER BY COUNT(b.booking_id) DESC
        LIMIT 5
    """
    return run_query(sql)


def report_trainers_above_avg():
    """🏅 เทรนเนอร์ที่มีผู้จองมากกว่าค่าเฉลี่ย (Above Average)
    คำใบ้: JOIN booking→gym_class→trainer, GROUP BY trainer, HAVING COUNT(*) > (subquery AVG)"""
    sql = """
        SELECT t.name                   AS 'ชื่อเทรนเนอร์',
            COUNT(b.booking_id)         AS 'จำนวนการจอง'
        FROM booking b
        INNER JOIN gym_class c  ON b.class_id   = c.class_id
        INNER JOIN trainer t    ON c.trainer_id = t.trainer_id
        WHERE b.status = 'CONFIRMED'
        GROUP BY t.trainer_id, t.name
        HAVING COUNT(b.booking_id) > (
            SELECT AVG(booking_count)
            FROM (
                SELECT COUNT(b2.booking_id) AS booking_count
                FROM trainer t2
                LEFT JOIN gym_class c2 ON t2.trainer_id = c2.trainer_id
                LEFT JOIN booking b2 ON c2.class_id = b2.class_id
                                      AND b2.status = 'CONFIRMED'
                GROUP BY t2.trainer_id
            ) AS avg_table
        )
    """
    return run_query(sql)

def report_class_equipment():
    """🧰 อุปกรณ์ที่ใช้ในแต่ละคลาส (Join 3 Tables)
    คำใบ้: JOIN class_equipment→gym_class, class_equipment→equipment"""
    sql = """
        SELECT 
            gc.name         AS 'ชื่อคลาส',
            e.name          AS 'ชื่ออุปกรณ์',
            ce.quantity     AS 'จำนวนที่ใช้'
        FROM class_equipment ce
        INNER JOIN gym_class gc ON ce.class_id = gc.class_id
        INNER JOIN equipment e ON ce.equip_id = e.equip_id
    """
    return run_query(sql)
