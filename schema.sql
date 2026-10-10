-- ============================================================
--  schema.sql — ระบบฟิตเนส (นิสิตออกแบบและเขียนเอง)
--  กติกา: การจอง = M:N (member × gym_class), อุปกรณ์ต่อคลาส = M:N (gym_class × equipment),
--         แต่ละคลาสมีเทรนเนอร์ (1:M จาก trainer)
-- ============================================================

-- 1. ตารางสมาชิก (member)
CREATE TABLE member (
    member_id    INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    gender       ENUM('female','male','non_binary','not_specified')
    			 not null default 'not_specified',
    join_date    DATE NOT NULL,
    package_type VARCHAR(50),
    referred_id  INT DEFAULT NULL,

    FOREIGN KEY (referred_id)
        REFERENCES member(member_id)
);

-- 2. ตารางผู้ฝึกสอน (trainer)
CREATE TABLE trainer (
    trainer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    specialty    VARCHAR(100),
    phone        VARCHAR(20)
    
);

-- 3. ตารางคลาสออกกำลังกาย (gym_class) - 1:M จาก trainer
CREATE TABLE gym_class (
    class_id      INT AUTO_INCREMENT PRIMARY KEY,
    trainer_id    INT NOT NULL,
    name          VARCHAR(100) NOT NULL,
    room          VARCHAR(20),
    capacity      INT NOT NULL,
    schedule_time DATETIME NOT NULL,
    
    FOREIGN KEY (trainer_id) 
    	REFERENCES trainer(trainer_id)
);

-- 4. ตารางการจอง (booking) - M:N ระหว่าง member และ gym_class
CREATE TABLE booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id  INT NOT NULL,
    class_id   INT NOT NULL,
    book_date  DATETIME NOT NULL,
    status     VARCHAR(50) NOT NULL DEFAULT 'CONFIRMED',
    
    FOREIGN KEY (member_id)
    	REFERENCES member(member_id),
    FOREIGN KEY (class_id)
    	REFERENCES gym_class(class_id) 
);

-- 5. ตารางอุปกรณ์ (equipment)
CREATE TABLE equipment (
    equip_id       INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    zone           VARCHAR(50),
    status         VARCHAR(50) NOT NULL DEFAULT 'Available',
    total_quantity INT NOT NULL DEFAULT 0
);

-- 6. ตารางอุปกรณ์ที่ใช้ในแต่ละคลาส (class_equipment) - M:N ระหว่าง gym_class และ equipment
CREATE TABLE class_equipment (
    class_id INT NOT NULL,
    equip_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (class_id, equip_id),
    
    FOREIGN KEY (class_id) 
    	REFERENCES gym_class(class_id),
    FOREIGN KEY (equip_id) 
    	REFERENCES equipment(equip_id) 
);

-- ============================================================
--  INSERT ข้อมูลตัวอย่างสำหรับทดสอบ
-- ============================================================

-- เพิ่มข้อมูลสมาชิก (member)
INSERT INTO member (
	name,
	gender,
	join_date,
	package_type,
	referred_id
)
VALUES 
	('Itadori Yuji'		, 'male'			,'2026-01-15', 'Regular'	,NULL),
	('Fushiguro Megumi'	, 'male'			,'2026-02-01', 'Regular'	,1),
	('Kugisaki Nobara'	, 'female'			,'2026-02-10', 'Vip'		,1),
	
	('Okkotsu Yuta'		, 'male'			,'2026-02-01', 'Regular'	,NULL),
	('Zenin Maki'		, 'female'			,'2026-02-01', 'Vip'		,4),
	('Inumaki Toge'		, 'male'			,'2026-02-01', 'Regular'	,4),
	('Panda'			, 'not_specified'	,'2026-02-01', 'Regular'	,4);

-- เพิ่มข้อมูลผู้ฝึกสอน (trainer)
INSERT INTO trainer (
	name,
	specialty,
	phone
)
VALUES 
	('Gojo Satoru'		, 'Bodybuilding & Powerlifting'		, '0811112222' ),
	('Nanami Kento'		, 'Cardio & Endurance'				, '0822223333' ),
	('Yagai Masamichi'	, 'CrossFit & Functional Training'	, '0833334444' ),
	('Ieiri Shoko'		, 'Yoga & Pilates'					, '0855556666' ),
	('Ryomen Sukuna'	, 'Extreme Conditioning'			, '0877778888' ); 

-- เพิ่มข้อมูลคลาส (gym_class)
INSERT INTO gym_class (
	trainer_id,
	name, 
	room,
	capacity,
	schedule_time
) 
VALUES 
	(1, 'Power Weightlifting'	, 'Room A'		, 15, '2026-10-10 09:00:00'),
	(2, 'Cardio Burn'			, 'Studio 1'	, 20, '2026-10-10 10:30:00'),
	(3, 'CrossFit Challenge'	, 'Room B'		, 12, '2026-10-11 14:00:00'),
	(4, 'Morning Yoga'			, 'Studio 2'	, 15, '2026-10-12 08:00:00'),
	(1, 'Advanced Bodybuilding'	, 'Room A'		, 10, '2026-10-13 16:00:00'),
	(5, 'HIIT Cardio Extreme'	, 'Studio 3'	, 20, '2026-10-14 17:00:00');

-- เพิ่มข้อมูลการจอง (booking)
INSERT INTO booking (
	member_id,
	class_id, 
	book_date, 
	status
) 
VALUES
	(1, 1, '2026-10-01 08:30:00', 'CONFIRMED'),
	(2, 2, '2026-10-01 09:15:00', 'CONFIRMED'),
	(3, 1, '2026-10-02 10:00:00', 'CONFIRMED'),
	(4, 4, '2026-10-03 11:20:00', 'CONFIRMED'),
	(5, 3, '2026-10-04 14:00:00', 'CANCELLED');

-- เพิ่มข้อมูลอุปกรณ์ (equipment)
INSERT INTO equipment (
	name, 
	zone, 
	status, 
	total_quantity
) 
VALUES 
	('Dumbbell Set 10kg'	, 'Free Weight', 'Available', 20),
	('Yoga Mat'				, 'Studio Zone', 'Available', 30),
	('Kettlebell 16kg'		, 'Free Weight', 'Available', 12),
	('Jump Rope'			, 'Cardio Zone', 'Available', 25),
	('Barbell 20kg'			, 'Free Weight', 'Available', 15),
	('Resistance Band'		, 'Studio Zone', 'Available', 40);

-- เพิ่มข้อมูลการใช้อุปกรณ์ในคลาส (class_equipment)
INSERT INTO class_equipment (
	class_id, 
	equip_id, 
	quantity
) 
VALUES 
	(1, 1, 15), -- Class 1 (Power Weightlifting) ใช้ Dumbbell 15 ชุด
	(1, 3, 10), -- Class 1 ใช้ Kettlebell 10 อัน
	(2, 4, 20), -- Class 2 (Cardio Burn) ใช้ Jump Rope 20 เส้น
	(3, 3, 12), -- Class 3 (CrossFit) ใช้ Kettlebell 12 อัน
	(4, 2, 15), -- Class 4 (Yoga) ใช้ Yoga Mat 15 ผืน
	(5, 5, 10),	-- Class 5 (Advanced Bodybuilding) ใช้ Barbell 20kg 15
	(6, 6, 18);	-- Class 6 (HIIT Cardio Extreme) ใช้ Resistance Band 18 