PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(256) NOT NULL, 
	role VARCHAR(7) NOT NULL, 
	full_name VARCHAR(100) NOT NULL, 
	student_id VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email), 
	UNIQUE (student_id)
);
INSERT INTO users VALUES(2,'admin','admin@graduate.utm.my','$2b$12$AoWg5BcxhONNeohDD7cgSentxG2k1HpKwe9yCxcQxPR9TorpEQvk.','ADMIN','admin',NULL,'2025-06-24 14:18:06.746334');
INSERT INTO users VALUES(3,'ada_lovelace','ada_lovelace@graduate.utm.my','$2b$12$OSwVNm5vgAbsuoOwEQOInuZRgvBGrjFgUm3lWL/fK19jOEKpQbeEy','STUDENT','Ada Lovelace','MEC001815','2025-07-01 15:55:44.712120');
INSERT INTO users VALUES(4,'alan_turing','alan_turing@graduate.utm.my','$2b$12$FyfU/UCPoseCJNMXBiLnWeE.Qy0b5WP6tSTCCtJw7HfAxKIx1Oa2y','STUDENT','Alan Turing','MEC001912','2025-07-01 16:16:31.622391');
CREATE TABLE facilities (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	location VARCHAR(200) NOT NULL, 
	description TEXT, 
	is_bookable BOOLEAN, 
	is_active BOOLEAN, 
	capacity INTEGER, 
	operating_hours VARCHAR(100), 
	contact_info VARCHAR(200), 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO facilities VALUES(1,'Activity Learning Lab','Academic','Level 5 N28, FC',replace('Modern activity learning space with flexible seating arrangement. Features air-conditioning, ceiling-mounted projector, TV display, white board, and WiFi connectivity. Air-Conditioner, Projector (ceiling mounted), TV provided, White Board, WiFi facility\n\nDirections: From main entrance: Enter UTM campus via main gate. Head towards Faculty of Computing (N28A) building - the large building in the center-north area of campus. Take the elevator or stairs to Level 5. The Activity Learning Lab is located on Level 5 of the N28 building.','\n',char(10)),0,1,30,NULL,'Landmarks: Near Faculty of Computing N28A, close to Arked Angkasa food court|IMG:images/facilities/activity_learning_lab.jpg','2025-06-24 13:37:05.539875','2025-06-24 13:37:05.539875');
INSERT INTO facilities VALUES(2,'Lecture Room Type A','Academic','N28a, FC',replace('Traditional lecture hall with tiered seating for 45-60 people. Equipped with desktop PC, ceiling-mounted projector, air-conditioning, white board, and WiFi. Air-Conditioner, Desktop PC provided, White Board, WiFi facility, Projector (ceiling mounted), Total of 9 Lecture Hall available, 2 Located in N28a FC, 7 Located in N28 FC\n\nDirections: From main entrance: Enter campus and head to Faculty of Computing area. The N28A building is the main computing faculty building visible on the campus map. Lecture Room Type A is located within the N28A building. Multiple lecture halls are available - 2 in N28A building and 7 in N28 building.','\n',char(10)),0,1,52,NULL,'Landmarks: Faculty of Computing N28A building, near Arked Angkasa|IMG:images/facilities/lecture_room_type_a.jpg','2025-06-24 13:37:05.539878','2025-06-24 13:37:05.539878');
INSERT INTO facilities VALUES(3,'Lecture Room Type B','Academic','Level 1 N28 & N28a, FC',replace('Mid-sized lecture room with modern amenities. Features ceiling-mounted projector, air-conditioning, desktop PC, white board, microphone system, and WiFi connectivity. Projector (ceiling mounted), Air-Conditioner, Desktop PC provided, White Board, Microphone provided, Total of 9 lecturer room, WiFi facility, Located in level 1 N28 & N28a FC\n\nDirections: From main entrance: Navigate to the Faculty of Computing area. Head to Level 1 of both N28 and N28A buildings. These lecture rooms are on the ground level for easy access. Look for signage indicating Lecture Room Type B.','\n',char(10)),0,1,35,NULL,'Landmarks: Ground floor of N28 & N28A buildings, Faculty of Computing area|IMG:images/facilities/lecture_room_type_b.jpg','2025-06-24 13:37:05.539880','2025-06-24 13:37:05.539880');
INSERT INTO facilities VALUES(4,'Computer Lab','Laboratory','N28 & N28a, FC',replace('Well-equipped computer laboratory with individual workstations. Features ceiling-mounted projector, WiPG wireless system, air-conditioning, microphones, white board, and WiFi connectivity. Projector (ceiling mounted), WiPG Wireless system, Air-Conditioner, Microphone provided, White Board, WiFi facility, Total of 12 Computer lab, Located in N28 & N28a FC\n\nDirections: From main entrance: Proceed to Faculty of Computing buildings (N28 & N28A). The computer labs are distributed across both buildings. Look for "Computer Lab" signage. There are 12 computer labs total - some in N28A and others in N28 building.','\n',char(10)),1,1,55,NULL,'Landmarks: N28 & N28A buildings, Faculty of Computing complex|IMG:images/facilities/computer_lab.jpg','2025-06-24 13:37:05.539881','2025-06-24 13:37:05.539881');
INSERT INTO facilities VALUES(5,'CCNP Network Lab','Laboratory','Level 4 N28, FC',replace('Specialized networking laboratory for CCNP training and network configuration. Equipped with ceiling-mounted projector, air-conditioning, desktop PC, white board, and WiFi connectivity. Air-Conditioner, Projector (ceiling mounted), Desktop PC provided, White Board, WiFi facility, Located in level 4 N28 FC\n\nDirections: From main entrance: Head to Faculty of Computing area. Go to the N28 building and take elevator/stairs to Level 4. The CCNP Network Lab is a specialized networking laboratory located on the 4th floor of N28 building.','\n',char(10)),1,1,37,NULL,'Landmarks: Level 4 N28 building, Faculty of Computing area|IMG:images/facilities/ccnp_network_lab.jpg','2025-06-24 13:37:05.539882','2025-06-24 13:37:05.539882');
INSERT INTO facilities VALUES(6,'Tutorial Room','Academic','Level 1 N28a, FC',replace('Intimate tutorial space designed for small group discussions and tutoring sessions. Features ceiling-mounted projector, air-conditioning, desktop PC, white board, and WiFi connectivity. Projector (ceiling mounted), Air-Conditioner, Desktop PC provided, White Board, WiFi facility, Total of 6 tutorial room, Located in level 1 N28a FC\n\nDirections: From main entrance: Walk to Faculty of Computing buildings. Head to N28A building and go to Level 1 (ground floor). The tutorial rooms are designed for small group sessions. There are 6 tutorial rooms available on Level 1 of N28A.','\n',char(10)),1,1,22,NULL,'Landmarks: Ground floor N28A building, Faculty of Computing|IMG:images/facilities/tutorial_room.jpg','2025-06-24 13:37:05.539882','2025-06-24 13:37:05.539882');
INSERT INTO facilities VALUES(7,'Meeting Room','Administrative','N28a, FC and N28, FC',replace('Professional meeting space with tiered seating arrangement. Equipped with air-conditioning, computer access, WiPG wireless system, free WiFi, white board, and ceiling-mounted projector. Air-Conditioner, Computer provided, WiPG Wireless system, Free WiFi, White Board, Projector (ceiling mounted), Total of 3 meeting room available, 2 Located in N28a FC, 1 Located in N28 FC\n\nDirections: From main entrance: Navigate to Faculty of Computing area. Meeting rooms are located in both N28A and N28 buildings. 2 meeting rooms are in N28A building, and 1 is in N28 building. Look for meeting room signage in both buildings.','\n',char(10)),1,1,30,NULL,'Landmarks: N28A and N28 buildings, Faculty of Computing complex|IMG:images/facilities/meeting_room.jpg','2025-06-24 13:37:05.539883','2025-06-24 13:37:05.539883');
INSERT INTO facilities VALUES(8,'Kejora Hall','Event','N28a, FC',replace('Large seminar hall suitable for major events, conferences, and large gatherings. Features ceiling-mounted projector, WiPG wireless system, PA system, desktop PC, air-conditioning, white board, and WiFi connectivity. Projector (ceiling mounted), WiPG Wireless system, PA system provided, Desktop PC provided, WiFi facility, Air-Conditioner, White Board, Total of 1 seminar hall, Located in N28a FC\n\nDirections: From main entrance: Head to Faculty of Computing area and locate the N28A building. Kejora Hall is the main seminar hall located within the N28A building. It is the largest venue in the computing faculty, suitable for major events and conferences.','\n',char(10)),1,1,200,NULL,'Landmarks: N28A building, Faculty of Computing, near main campus center|IMG:images/facilities/kejora_hall.jpg','2025-06-24 13:37:05.539883','2025-06-24 13:37:05.539883');
INSERT INTO facilities VALUES(9,'Discussion Room','Academic','Level 2 N28a, FC',replace('Small discussion room perfect for team meetings and group work. Features air-conditioning, ceiling-mounted projector, white board, and WiFi connectivity. Air-Conditioner, Projector (ceiling mounted), White Board, WiFi facility, Total of 3 discussion room available, Located in level 2 N28a FC\n\nDirections: From main entrance: Go to Faculty of Computing buildings. Head to N28A building and proceed to Level 2. The discussion rooms are small, intimate spaces perfect for team meetings. There are 3 discussion rooms available on Level 2 of N28A.','\n',char(10)),1,1,9,NULL,'Landmarks: Level 2 N28A building, Faculty of Computing area|IMG:images/facilities/discussion_room.jpg','2025-06-24 13:37:05.539884','2025-06-24 13:37:05.539884');
INSERT INTO facilities VALUES(10,'Gymnasium','Sports','Sports Complex','Indoor gymnasium for sports activities',1,1,NULL,NULL,NULL,'2025-06-24 15:31:22.330235','2025-06-24 15:31:22.330238');
INSERT INTO facilities VALUES(11,'Male Hostel Block C','Accommodation','Hostel Area','Male student accommodation',0,1,NULL,NULL,NULL,'2025-06-24 15:31:22.331105','2025-06-24 15:31:22.331107');
INSERT INTO facilities VALUES(12,'Female Hostel Block D','Accommodation','Hostel Area','Female student accommodation',0,1,NULL,NULL,NULL,'2025-06-24 15:31:22.331108','2025-06-24 15:31:22.331109');
CREATE TABLE issues (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	description TEXT NOT NULL, 
	issue_type VARCHAR(10) NOT NULL, 
	priority VARCHAR(6), 
	status VARCHAR(11), 
	location VARCHAR(200) NOT NULL, 
	user_id INTEGER NOT NULL, 
	facility_id INTEGER, 
	assigned_to INTEGER, 
	created_at DATETIME, 
	updated_at DATETIME, 
	resolved_at DATETIME, 
	admin_notes TEXT, 
	feedback_rating INTEGER, 
	feedback_comment TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(facility_id) REFERENCES facilities (id), 
	FOREIGN KEY(assigned_to) REFERENCES users (id)
);
INSERT INTO issues VALUES(1,'Issue with Lecture Room Type A','Air conditioning broke down, the room is so hot, I can''t study','ELECTRICAL','HIGH','IN_PROGRESS','N28a, FC',3,NULL,NULL,'2025-07-01 16:01:16.095999','2025-07-01 16:15:18.582350',NULL,'I have asked the technician to check the air conditioning in Lecture Room Type A, please wait 1-2 days.',NULL,NULL);
INSERT INTO issues VALUES(2,'Issue with Female Hostel Block D','There are a lot of rats in the female dormroom.','HYGIENE','HIGH','RESOLVED','Hostel Area',3,NULL,NULL,'2025-07-01 16:02:12.388193','2025-07-01 16:15:34.103699','2025-07-01 16:15:34.103699','I killed all rats yesterday.',NULL,NULL);
INSERT INTO issues VALUES(3,'Issue with Male Hostel Block C','Someone did not flush the toilet, may we add automated flushing mechanisms?','HYGIENE','MEDIUM','CLOSED','Hostel Area',4,NULL,NULL,'2025-07-01 16:19:53.475900','2025-07-01 16:26:15.719653',NULL,'This is not an issue, you can flush it for your dorm mates.',NULL,NULL);
INSERT INTO issues VALUES(4,'Issue with Gymnasium','The weights are not heavy enough, I can''t gain enough muscle.','EQUIPMENT','LOW','REPORTED','Sports Complex',4,NULL,NULL,'2025-07-01 16:20:36.665158','2025-07-01 16:20:36.665158',NULL,NULL,NULL,NULL);
INSERT INTO issues VALUES(5,'Issue with Kejora Hall','The lights and mic are not working, I need to give a thesis presentation to Dr Shasha soon, please help to fix immediately.','EQUIPMENT','URGENT','IN_PROGRESS','N28a, FC',4,NULL,NULL,'2025-07-01 16:23:49.094618','2025-07-01 16:26:38.647362',NULL,'I have sent technicians to check on the issues, will be done today.',NULL,NULL);
CREATE TABLE chat_sessions (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	session_id VARCHAR(50) NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO chat_sessions VALUES(1,3,'8bbb33b3-f3ec-41e1-97bc-875280255e4c','2025-07-01 16:03:59.797055');
CREATE TABLE facility_bookings (
	id INTEGER NOT NULL, 
	facility_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	booking_date DATE NOT NULL, 
	start_hour INTEGER NOT NULL, 
	end_hour INTEGER NOT NULL, 
	purpose VARCHAR(200), 
	status VARCHAR(9), 
	admin_notes TEXT, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(facility_id) REFERENCES facilities (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO facility_bookings VALUES(1,4,3,'2025-12-10',8,9,'To practice on solving computer problems.','APPROVED','Please go ahead, I will turn on the electricity and check the computers before this slot.','2025-07-01 15:57:07.243055','2025-07-01 16:13:38.612712');
INSERT INTO facility_bookings VALUES(2,5,3,'2025-12-25',12,13,'To celebrate Christmas by solving network problems.','REJECTED','CCNP Network Lab is closed during Christmas, solve network problems elsewhere.','2025-07-01 15:58:49.919787','2025-07-01 16:14:20.953308');
INSERT INTO facility_bookings VALUES(3,10,4,'2026-06-23',8,9,'I need to gain muscle to learn computing.','APPROVED','Hope you gain huge muscles and become a computing legend with muscles.','2025-07-01 16:17:25.827752','2025-07-01 16:24:58.270405');
INSERT INTO facility_bookings VALUES(4,8,4,'2025-09-08',8,22,'I need to present my AI thesis to Dr Shasha. This research will change the whole world.','PENDING',NULL,'2025-07-01 16:18:31.001667','2025-07-01 16:18:31.001667');
INSERT INTO facility_bookings VALUES(5,6,4,'2025-07-02',8,22,'I need to do some tutorials to pass my exams.','CANCELLED','Date has passed, sorry I wasn''t able to approve in time.','2025-07-01 16:19:10.806312','2025-07-01 16:25:25.044133');
INSERT INTO facility_bookings VALUES(6,9,3,'2025-07-03',8,9,'To discuss and align on AI Assignment and Presentation.','APPROVED','Please go ahead.','2025-07-01 17:06:16.761724','2025-07-01 17:06:46.479440');
CREATE TABLE chat_messages (
	id INTEGER NOT NULL, 
	session_id INTEGER NOT NULL, 
	message TEXT NOT NULL, 
	is_user BOOLEAN NOT NULL, 
	intent VARCHAR(50), 
	entities JSON, 
	timestamp DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES chat_sessions (id)
);
INSERT INTO chat_messages VALUES(1,1,'1+1?',1,'general_info','{"facility": null, "location": null, "issue_type": null, "component": null}','2025-07-01 16:04:24.664257');
INSERT INTO chat_messages VALUES(2,1,replace('That’s a classic! In math terms, 1+1 = 2. 😊  \n\nIf you were testing me—I passed! Let me know if you have any *actual* questions about UTM’s facilities. For example:  \n- *"Where’s the gym?"*  \n- *"How do I book a meeting room?"*  \n\nHappy to help!','\n',char(10)),0,NULL,NULL,'2025-07-01 16:04:24.665286');
INSERT INTO chat_messages VALUES(3,1,'Where is the computer lab?',1,'search','{"facility": "Computer Lab", "location": null, "issue_type": null, "component": null}','2025-07-01 16:05:19.975432');
INSERT INTO chat_messages VALUES(4,1,replace('The **Computer Lab** is located in **N28 & N28a (Faculty Cluster, FC)**. It''s a **bookable** facility for academic or research use.  \n\nNeed help booking, or looking for a specific lab (e.g., CCNP Network Lab on Level 4 N28)? Just ask! 😊','\n',char(10)),0,NULL,NULL,'2025-07-01 16:05:19.976429');
INSERT INTO chat_messages VALUES(5,1,'How to report a broken air conditioner?',1,'report_issue','{"facility": null, "location": null, "issue_type": "equipment", "component": "air conditioner"}','2025-07-01 16:05:57.792867');
INSERT INTO chat_messages VALUES(6,1,replace('Got it! To report a *broken air conditioner* (or any facility issue) at UTM:  \n\n1. **Specify the location** (e.g., *"Hostel Block C, Room 205"* or *"Level 5 Activity Learning Lab, N28"*) so I can direct you further.  \n2. **Reporting Options**:  \n   - *Online Portal*: Submit via the official UTM facilities maintenance system (link not visible here).  \n   - *In-Person*: Visit the Facilities Management Office (Ground Floor, N28).  \n\nNeed more details (e.g., severity, noise/leakage)? Let me know! 🌟  \n\n*(Note: Exact reporting steps may vary—check campus notices for updates.)*','\n',char(10)),0,NULL,NULL,'2025-07-01 16:05:57.793864');
INSERT INTO chat_messages VALUES(7,1,'Hi, are there air conditioning in this facility?',1,'general_info','{"facility": null, "location": null, "issue_type": null, "component": "air conditioning"}','2025-07-01 16:53:06.078639');
INSERT INTO chat_messages VALUES(8,1,'Hi there! Yes, Kejora Hall at N28a, FC is air-conditioned. If you''re planning an event there, you can book it through the campus booking system. Let me know if you''d like more details! 😊',0,NULL,NULL,'2025-07-01 16:53:06.423819');
INSERT INTO chat_messages VALUES(9,1,'In Kejora Hall, the air conditioning is not working, what do I do?',1,'report_issue','{"facility": "Kejora Hall", "location": "N28a, FC", "issue_type": "electrical", "component": "air conditioning"}','2025-07-01 16:56:24.800240');
INSERT INTO chat_messages VALUES(10,1,replace('👋 **UTM Campus Assistant** can help you with:\n\n• 🔍 **Find facilities** - Ask about locations and details\n• 🔧 **Report issues** - Submit facility problems\n• 📅 **Booking info** - Get booking information\n• ℹ️ **General info** - Campus facility questions\n\nWhat can I help you with today?','\n',char(10)),0,NULL,NULL,'2025-07-01 16:56:24.800240');
INSERT INTO chat_messages VALUES(11,1,'How do I report the issue of broken air conditioning in Kejora Hall?',1,'general_info','{}','2025-07-01 17:00:45.444207');
INSERT INTO chat_messages VALUES(12,1,replace('🔧 To report a facility issue:\n1. Go to the **Report Issue** page\n2. Describe the problem in detail\n3. Select the issue type and location\n4. Submit your report\n\nYou can track the status of your report from your dashboard.','\n',char(10)),0,NULL,NULL,'2025-07-01 17:00:45.444207');
INSERT INTO chat_messages VALUES(13,1,'How do I book the Kejora Hall?',1,'general_info','{}','2025-07-01 17:02:13.387369');
INSERT INTO chat_messages VALUES(14,1,'📚 The **Library** is located at **Block B, Ground Floor**. It''s open from 8:00 AM to 10:00 PM and provides study spaces and resources for students.',0,NULL,NULL,'2025-07-01 17:02:13.387369');
INSERT INTO chat_messages VALUES(15,1,'How to book a facility?',1,'general_info','{}','2025-07-01 17:02:27.695017');
INSERT INTO chat_messages VALUES(16,1,'📚 The **Library** is located at **Block B, Ground Floor**. It''s open from 8:00 AM to 10:00 PM and provides study spaces and resources for students.',0,NULL,NULL,'2025-07-01 17:02:27.695986');
INSERT INTO chat_messages VALUES(17,1,'What is 1 + 1?',1,'general_info','{}','2025-07-01 17:03:01.218290');
INSERT INTO chat_messages VALUES(18,1,replace('👋 **UTM Campus Assistant** can help you with:\n\n• 🔍 **Find facilities** - Ask about locations and details\n• 🔧 **Report issues** - Submit facility problems\n• 📅 **Booking info** - Get booking information\n• ℹ️ **General info** - Campus facility questions\n\nWhat can I help you with today?','\n',char(10)),0,NULL,NULL,'2025-07-01 17:03:01.218290');
COMMIT;
