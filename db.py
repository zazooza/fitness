# ============================================================
#   db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#   มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# ============================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT, use_pure=True)


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


# ---------- สมาชิก (member) ----------
def search_members(filters):
    """ค้นหา สมาชิก ตามเงื่อนไข (name, gender, package_type)"""
    sql = "SELECT * FROM member WHERE 1=1"
    params = []
    
    if filters.get('name'):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get('gender'):
        sql += " AND gender = %s"
        params.append(filters['gender'])
    if filters.get('package_type'):
        sql += " AND package_type = %s"
        params.append(filters['package_type'])
    sql += " ORDER BY member_id"
    return run_query(sql, params)


def get_member(member_id):
    rows = run_query("SELECT * FROM member WHERE member_id = %s", (member_id,))
    return rows[0] if rows else None


def create_member(data):
    """เพิ่ม สมาชิก ใหม่ — data มีคีย์: name, gender, join_date, package_type,referred_id"""
    sql = """
        INSERT INTO member (name, gender, join_date, package_type, referred_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    referred_id = data.get('referred_id') or None
    params = (
        data.get('name'),
        data.get('gender'),
        data.get('join_date'),
        data.get('package_type'),
        referred_id
    )
    return run_command(sql, params)


def update_member(member_id, data):
    """แก้ไข สมาชิก ตาม member_id"""
    sql = """
        UPDATE member 
        SET name = %s, gender = %s, join_date = %s, package_type = %s, referred_id = %s
        WHERE member_id = %s
    """
    params = (
        data.get('name'),
        data.get('gender'),
        data.get('join_date'),
        data.get('package_type'),
        data.get('referred_id') or None,
        member_id
    )
    return run_command(sql, params)


def delete_member(member_id):
    """ลบ สมาชิก ตาม member_id"""
    sql = "DELETE FROM member WHERE member_id = %s"
    return run_command(sql, (member_id,))


# ---------- คลาสเรียน (gym_class) ----------
def list_trainers():
    """ดึงรายชื่อเทรนเนอร์สำหรับตัวเลือกในฟอร์มคลาส"""
    return run_query("SELECT trainer_id, name FROM trainer ORDER BY name")


def search_trainers(filters):
    sql = "SELECT trainer_id, name, specialty, phone FROM trainer WHERE 1=1"
    params = []
    if filters.get('name'):
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get('specialty'):
        sql += " AND specialty LIKE %s"
        params.append(f"%{filters['specialty']}%")
    sql += " ORDER BY trainer_id"
    return run_query(sql, params)


def get_trainer(trainer_id):
    rows = run_query("SELECT * FROM trainer WHERE trainer_id = %s", (trainer_id,))
    return rows[0] if rows else None


def create_trainer(data):
    sql = "INSERT INTO trainer (name, specialty, phone) VALUES (%s, %s, %s)"
    return run_command(sql, (data.get('name'), data.get('specialty'), data.get('phone')))


def update_trainer(trainer_id, data):
    sql = "UPDATE trainer SET name = %s, specialty = %s, phone = %s WHERE trainer_id = %s"
    return run_command(sql, (data.get('name'), data.get('specialty'), data.get('phone'), trainer_id))


def delete_trainer(trainer_id):
    return run_command("DELETE FROM trainer WHERE trainer_id = %s", (trainer_id,))


# ---------- อุปกรณ์ (equipment) ----------
def search_equipment(filters):
    sql = "SELECT equip_id, name, zone, status, total_quantity FROM equipment WHERE 1=1"
    params = []
    for key in ('name', 'zone', 'status'):
        if filters.get(key):
            sql += f" AND {key} LIKE %s"
            params.append(f"%{filters[key]}%")
    sql += " ORDER BY equip_id"
    return run_query(sql, params)


def get_equipment(equip_id):
    rows = run_query("SELECT * FROM equipment WHERE equip_id = %s", (equip_id,))
    return rows[0] if rows else None


def create_equipment(data):
    sql = """INSERT INTO equipment (name, zone, status, total_quantity)
             VALUES (%s, %s, %s, %s)"""
    return run_command(sql, (data.get('name'), data.get('zone'), data.get('status', 'Available'), data.get('total_quantity', 0)))


def update_equipment(equip_id, data):
    sql = """UPDATE equipment SET name = %s, zone = %s, status = %s,
             total_quantity = %s WHERE equip_id = %s"""
    return run_command(sql, (data.get('name'), data.get('zone'), data.get('status'), data.get('total_quantity'), equip_id))


def delete_equipment(equip_id):
    return run_command("DELETE FROM equipment WHERE equip_id = %s", (equip_id,))


def search_classes(filters):
    """ค้นหา คลาสเรียน ตามเงื่อนไข (name, room)"""
    sql = """
        SELECT c.class_id, c.name, t.name AS trainer_name, c.room, c.capacity, c.schedule_time
        FROM gym_class c
        JOIN trainer t ON c.trainer_id = t.trainer_id
        WHERE 1=1
    """
    params = []
    
    if filters.get('name'):
        sql += " AND c.name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get('room'):
        sql += " AND c.room LIKE %s"
        params.append(f"%{filters['room']}%")

    sql += " ORDER BY c.class_id"
    return run_query(sql, params)


def get_class(class_id):
    """ดึง คลาสเรียน 1 รายการตาม class_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    sql = "SELECT * FROM gym_class WHERE class_id = %s"
    rows = run_query(sql, (class_id,))
    return rows[0] if rows else None


def create_class(data):
    """เพิ่ม คลาสเรียน ใหม่ — data มีคีย์: name, trainer_id, room, capacity, schedule_time"""
    sql = """
        INSERT INTO gym_class (name, trainer_id, room, capacity, schedule_time)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data.get('name'),
        data.get('trainer_id'),
        data.get('room'),
        data.get('capacity'),
        data.get('schedule_time')
    )
    return run_command(sql, params)


def update_class(class_id, data):
    """แก้ไข คลาสเรียน ตาม class_id"""
    sql = """
        UPDATE gym_class 
        SET name = %s, trainer_id = %s, room = %s, capacity = %s, schedule_time = %s
        WHERE class_id = %s
    """
    params = (
        data.get('name'),
        data.get('trainer_id'),
        data.get('room'),
        data.get('capacity'),
        data.get('schedule_time'),
        class_id
    )
    return run_command(sql, params)


def delete_class(class_id):
    """ลบ คลาสเรียน ตาม class_id"""
    sql = "DELETE FROM gym_class WHERE class_id = %s"
    return run_command(sql, (class_id,))


# ---------- การจอง (booking) ----------
def search_bookings(filters):
    """ค้นหา การจอง ตามเงื่อนไข (member_id, class_id, status)"""
    sql = """
        SELECT b.booking_id, m.name as member_name, c.name as class_name,
               b.book_date, b.status
        FROM booking b
        JOIN member m ON b.member_id = m.member_id
        JOIN gym_class c ON b.class_id = c.class_id
        WHERE 1=1
    """
    params = []
    
    if filters.get('name'):
        sql += " AND m.name LIKE %s"
        params.append(f"%{filters['name']}%")
    if filters.get('class_id'):
        sql += " AND b.class_id = %s"
        params.append(filters['class_id'])
    if filters.get('status'):
        sql += " AND b.status = %s"
        params.append(filters['status'])
        
    return run_query(sql, params)


def get_booking(booking_id):
    """ดึง การจอง 1 รายการตาม booking_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    sql = "SELECT * FROM booking WHERE booking_id = %s"
    rows = run_query(sql, (booking_id,))
    return rows[0] if rows else None


def create_booking(data):
    """เพิ่ม การจอง ใหม่ — data มีคีย์: member_id, class_id, book_date, status"""
    sql = """
        INSERT INTO booking (member_id, class_id, book_date, status)
        VALUES (%s, %s, %s, %s)
    """
    params = (
        data.get('member_id'),
        data.get('class_id'),
        data.get('book_date'),
        data.get('status', 'CONFIRMED')
    )
    return run_command(sql, params)


def update_booking(booking_id, data):
    """แก้ไข การจอง ตาม booking_id"""
    sql = """
        UPDATE booking 
        SET member_id = %s, class_id = %s, book_date = %s, status = %s
        WHERE booking_id = %s
    """
    params = (
        data.get('member_id'),
        data.get('class_id'),
        data.get('book_date'),
        data.get('status'),
        booking_id
    )
    return run_command(sql, params)


def delete_booking(booking_id):
    """ลบ การจอง ตาม booking_id"""
    sql = "DELETE FROM booking WHERE booking_id = %s"
    return run_command(sql, (booking_id,))


# ============================================================
#   REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
# ============================================================
def report_summary():
    """ตัวเลขสรุปบนการ์ด dashboard — คืน dict เช่น {"members": 10, ...}"""
    sql_members = "SELECT COUNT(*) AS total FROM member"
    sql_classes = "SELECT COUNT(*) AS total FROM gym_class"
    sql_bookings = "SELECT COUNT(*) AS total FROM booking"
    sql_trainers = "SELECT COUNT(*) AS total FROM trainer"
    sql_equipment = "SELECT COUNT(*) AS total FROM equipment"
    sql_available_equipment = """SELECT COALESCE(SUM(total_quantity), 0) AS total
                                 FROM equipment WHERE status = 'available'"""
    
    return {
        "members": run_query(sql_members)[0]['total'],
        "classes": run_query(sql_classes)[0]['total'],
        "bookings": run_query(sql_bookings)[0]['total'],
        "trainers": run_query(sql_trainers)[0]['total'],
        "equipment": run_query(sql_equipment)[0]['total'],
        "available_equipment": run_query(sql_available_equipment)[0]['total']
    }


def report_popular_classes():
    """📈 คลาสยอดนิยม (Most Booked)
    JOIN booking -> gym_class, GROUP BY class, COUNT, ORDER BY DESC, LIMIT 5"""
    sql = """
        SELECT 
            c.class_id,
            c.name AS class_name,
            COUNT(b.booking_id) AS total_bookings
        FROM booking b
        INNER JOIN gym_class c ON b.class_id = c.class_id
        GROUP BY c.class_id, c.name
        ORDER BY total_bookings DESC
        LIMIT 5
    """
    return run_query(sql)


def report_trainers_above_avg():
    """🏅 เทรนเนอร์ที่มีผู้จองมากกว่าค่าเฉลี่ย (Above Average)
    JOIN booking -> gym_class -> trainer, GROUP BY trainer, HAVING COUNT(*) > (subquery AVG)"""
    sql = """
        SELECT 
            t.trainer_id,
            t.name AS trainer_name,
            COUNT(b.booking_id) AS total_bookings
        FROM booking b
        INNER JOIN gym_class c ON b.class_id = c.class_id
        INNER JOIN trainer t ON c.trainer_id = t.trainer_id
        GROUP BY t.trainer_id, t.name
        HAVING COUNT(b.booking_id) > (
            SELECT COUNT(b2.booking_id) / COUNT(DISTINCT t2.trainer_id)
            FROM booking b2
            INNER JOIN gym_class c2 ON b2.class_id = c2.class_id
            INNER JOIN trainer t2 ON c2.trainer_id = t2.trainer_id
        )
        ORDER BY total_bookings DESC
    """
    return run_query(sql)


def report_class_equipment():
    """🧰 อุปกรณ์ที่ใช้ในแต่ละคลาส (Join 3 Tables)
    JOIN class_equipment -> gym_class, class_equipment -> equipment"""
    sql = """
        SELECT 
            c.name AS class_name,
            e.name AS equipment_name,
            ce.quantity
        FROM class_equipment ce
        INNER JOIN gym_class c ON ce.class_id = c.class_id
        INNER JOIN equipment e ON ce.equip_id = e.equip_id
        ORDER BY c.name, e.name
    """
    return run_query(sql)
