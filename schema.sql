-- ============================================================
--  schema.sql — ระบบฟิตเนส (นิสิตออกแบบและเขียนเอง)
--  กติกา: การจอง = m:n (member × gym_class), อุปกรณ์ต่อคลาส = m:n (gym_class × equipment),
--         แต่ละคลาสมีเทรนเนอร์ (1:m จาก trainer)
-- ============================================================

-- 1. ตารางสมาชิก (member)
create table member (
    member_id    int auto_increment primary key,
    name         varchar(100) not null,
    gender       enum('female','male','non_binary','not_specified')
    			 not null default 'not_specified',
    join_date    date not null,
    package_type varchar(50),
    referred_id  int default null,

    foreign key (referred_id)
        references member(member_id)
);

-- 2. ตารางผู้ฝึกสอน (trainer)
create table trainer (
    trainer_id   int auto_increment primary key,
    name         varchar(100) not null,
    specialty    varchar(100),
    phone        varchar(20)
    
);

-- 3. ตารางคลาสออกกำลังกาย (gym_class) - 1:m จาก trainer
create table gym_class (
    class_id      int auto_increment primary key,
    trainer_id    int not null,
    name          varchar(100) not null,
    room          varchar(20),
    capacity      int not null,
    schedule_time datetime not null,
    
    foreign key (trainer_id) 
    	references trainer(trainer_id)
);

-- 4. ตารางการจอง (booking) - m:n ระหว่าง member และ gym_class
create table booking (
    booking_id int auto_increment primary key,
    member_id  int not null,
    class_id   int not null,
    book_date  datetime not null,
    status     varchar(50) not null default 'CONFIRMED',
    
    foreign key (member_id)
    	references member(member_id),
    foreign key (class_id)
    	references gym_class(class_id)
);

-- 5. ตารางอุปกรณ์ (equipment)
create table equipment (
    equip_id       int auto_increment primary key,
    name           varchar(100) not null,
    zone           varchar(50),
    status         varchar(50) not null default 'Available',
    total_quantity int not null default 0
);

-- 6. ตารางอุปกรณ์ที่ใช้ในแต่ละคลาส (class_equipment) - m:n ระหว่าง gym_class และ equipment
create table class_equipment (
    class_id int not null,
    equip_id int not null,
    quantity int not null,
    primary key (class_id, equip_id),
    
    foreign key (class_id) 
    	references gym_class(class_id),
    foreign key (equip_id) 
    	references equipment(equip_id)
);

-- ============================================================
--  insert ข้อมูลตัวอย่างสำหรับทดสอบ
-- ============================================================

-- เพิ่มข้อมูลสมาชิก (member)
insert into member (
	name,
	gender,
	join_date,
	package_type,
	referred_id
)
values 
	('itadori yuji'		, 'male'			,'2026-01-15', 'regular'	,null),
	('fushiguro megumi'	, 'male'			,'2026-02-01', 'regular'	,1),
	('kugisaki nobara'	, 'female'			,'2026-02-10', 'vip'		,1),
	
	('okkotsu yuta'		, 'male'			,'2026-02-01', 'regular'	,null),
	('zenin maki'		, 'female'			,'2026-02-01', 'vip'		,4),
	('inumaki toge'		, 'male'			,'2026-02-01', 'regular'	,4),
	('panda'			, 'not_specified'	,'2026-02-01', 'regular'	,4);

-- เพิ่มข้อมูลผู้ฝึกสอน (trainer)
insert into trainer (
	name,
	specialty,
	phone
)
values 
	('gojo satoru'		, 'bodybuilding & powerlifting'		, '0811112222' ),
	('nanami kento'		, 'cardio & endurance'				, '0822223333' ),
	('yagai masamichi'	, 'crossfit & functional training'	, '0833334444' ),
	('ieiri shoko'		, 'yoga & pilates'					, '0855556666' ),
	('ryomen sukuna'	, 'extreme conditioning'			, '0877778888' );

-- เพิ่มข้อมูลคลาส (gym_class)
insert into gym_class (
	trainer_id,
	name, 
	room,
	capacity,
	schedule_time
) 
values 
	(1, 'power weightlifting'	, 'room a'		, 15, '2026-10-10 09:00:00'),
	(2, 'cardio burn'			, 'studio 1'	, 20, '2026-10-10 10:30:00'),
	(3, 'crossfit challenge'	, 'room b'		, 12, '2026-10-11 14:00:00'),
	(4, 'morning yoga'			, 'studio 2'	, 15, '2026-10-12 08:00:00'),
	(1, 'advanced bodybuilding'	, 'room a'		, 10, '2026-10-13 16:00:00'),
	(5, 'hiit cardio extreme'	, 'studio 3'	, 20, '2026-10-14 17:00:00');

-- เพิ่มข้อมูลการจอง (booking)
insert into booking (
	member_id,
	class_id, 
	book_date, 
	status
) 
values
	(1, 1, '2026-10-01 08:30:00', 'CONFIRMED'),
	(2, 2, '2026-10-01 09:15:00', 'CONFIRMED'),
	(3, 1, '2026-10-02 10:00:00', 'CONFIRMED'),
	(4, 4, '2026-10-03 11:20:00', 'CONFIRMED'),
	(5, 3, '2026-10-04 14:00:00', 'CANCELLED');

-- เพิ่มข้อมูลอุปกรณ์ (equipment)
insert into equipment (
	name, 
	zone, 
	status, 
	total_quantity
) 
values 
	('dumbbell set 10kg'	, 'Free weight', 'Available', 20),
	('yoga mat'				, 'studio zone', 'Available', 30),
	('kettlebell 16kg'		, 'Free weight', 'Available', 12),
	('jump rope'			, 'cardio zone', 'Available', 25),
	('barbell 20kg'			, 'Free weight', 'Available', 15),
	('resistance band'		, 'studio zone', 'Available', 40);

-- เพิ่มข้อมูลการใช้อุปกรณ์ในคลาส (class_equipment)
insert into class_equipment (
	class_id, 
	equip_id, 
	quantity
) 
values 
	(1, 1, 15), -- class 1 (power weightlifting) ใช้ dumbbell 15 ชุด
	(1, 3, 10), -- class 1 ใช้ kettlebell 10 อัน
	(2, 4, 20), -- class 2 (cardio burn) ใช้ jump rope 20 เส้น
	(3, 3, 12), -- class 3 (crossfit) ใช้ kettlebell 12 อัน
	(4, 2, 15), -- class 4 (yoga) ใช้ yoga mat 15 ผืน
	(5, 5, 10),	-- class 5 (advanced bodybuilding) ใช้ barbell 20kg 15
	(6, 6, 18);	-- class 6 (hiit cardio extreme) ใช้ resistance band 18