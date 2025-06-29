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
INSERT INTO users VALUES(1,'student','student@graduate.utm.my','$2b$12$F8FoM25d1iAAs07jiASlYOdw57khxyvWyAJCw/O0rEAxYKk3hlfhW','STUDENT','student','1234','2025-06-24 13:29:20.232277');
INSERT INTO users VALUES(2,'admin','admin@graduate.utm.my','$2b$12$AoWg5BcxhONNeohDD7cgSentxG2k1HpKwe9yCxcQxPR9TorpEQvk.','ADMIN','admin',NULL,'2025-06-24 14:18:06.746334');
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
INSERT INTO issues VALUES(1,'Broken air conditioning unit','Air cond broke','OTHER','MEDIUM','REPORTED','Kejora Hall',1,NULL,NULL,'2025-06-29 17:43:59.610016','2025-06-29 17:43:59.610016',NULL,NULL,NULL,NULL);
CREATE TABLE chat_sessions (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	session_id VARCHAR(50) NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO chat_sessions VALUES(1,1,'7da4b478-41e0-4d5b-8c79-f3f1b477f3f4','2025-06-24 13:29:45.114085');
INSERT INTO chat_sessions VALUES(2,1,'3bbcb977-779c-46a9-9535-021ccf1ece61','2025-06-24 15:05:10.476680');
INSERT INTO chat_sessions VALUES(3,1,'1b632250-c40d-4e82-a08a-c8acc349c2b4','2025-06-29 16:19:35.332287');
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
INSERT INTO facility_bookings VALUES(1,1,1,'2025-06-28',9,10,'uh to practioce','CANCELLED','nou','2025-06-24 13:30:42.076453','2025-06-29 17:18:57.756225');
INSERT INTO facility_bookings VALUES(2,1,1,'2025-06-24',8,9,'hehehehe','REJECTED','NO','2025-06-24 13:31:10.086738','2025-06-24 14:18:36.447643');
INSERT INTO facility_bookings VALUES(3,5,1,'2025-07-05',8,9,'for fun','PENDING','ok','2025-06-29 16:58:04.990629','2025-06-29 17:33:21.064520');
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
INSERT INTO chat_messages VALUES(1,2,'Where is the computer lab?',1,'search','{"facility": "Computer Lab", "location": "N28 & N28a, FC"}','2025-06-24 15:05:14.505242');
INSERT INTO chat_messages VALUES(2,2,replace('**Computer Lab**\n≡ƒôì Location: N28 & N28a, FC\n≡ƒÅó Category: Academic\nΓä╣∩╕Å Description: Well-equipped computer laboratory with individual workstations. Features ceiling-mounted projector, WiPG wireless system, air-conditioning, microphones, white board, and WiFi connectivity. Projector (ceiling mounted), WiPG Wireless system, Air-Conditioner, Microphone provided, White Board, WiFi facility, Total of 12 Computer lab, Located in N28 & N28a FC\n\nDirections: From main entrance: Proceed to Faculty of Computing buildings (N28 & N28A). The computer labs are distributed across both buildings. Look for "Computer Lab" signage. There are 12 computer labs total - some in N28A and others in N28 building.\n≡ƒôà This facility is bookable - you can make a reservation!\n','\n',char(10)),0,NULL,NULL,'2025-06-24 15:05:14.505838');
INSERT INTO chat_messages VALUES(3,2,'Where is the computer lab?',1,'search','{"facility": "Computer Lab", "location": "N28 & N28a, FC"}','2025-06-24 15:07:02.589434');
INSERT INTO chat_messages VALUES(4,2,replace('**Computer Lab**\n≡ƒôì Location: N28 & N28a, FC\n≡ƒÅó Category: Academic\nΓä╣∩╕Å Description: Well-equipped computer laboratory with individual workstations. Features ceiling-mounted projector, WiPG wireless system, air-conditioning, microphones, white board, and WiFi connectivity. Projector (ceiling mounted), WiPG Wireless system, Air-Conditioner, Microphone provided, White Board, WiFi facility, Total of 12 Computer lab, Located in N28 & N28a FC\n\nDirections: From main entrance: Proceed to Faculty of Computing buildings (N28 & N28A). The computer labs are distributed across both buildings. Look for "Computer Lab" signage. There are 12 computer labs total - some in N28A and others in N28 building.\n≡ƒôà This facility is bookable - you can make a reservation!\n','\n',char(10)),0,NULL,NULL,'2025-06-24 15:07:02.590504');
INSERT INTO chat_messages VALUES(5,3,'what equiment is in this lab',1,'general_info','{"facility": null, "location": null, "issue_type": null, "component": "equiment"}','2025-06-29 16:20:34.530433');
INSERT INTO chat_messages VALUES(6,3,replace('It looks like you''re asking about equipment in a lab, but I''m not sure which lab you''re referring to. Could you specify the lab? For example:  \n\n- **Computer Lab (N28 & N28a, FC)** – Typically has computers, printers, and software for general use.  \n- **CCNP Network Lab (Level 4, N28, FC)** – Contains networking equipment like routers, switches, and servers for IT/engineering courses.  \n\nLet me know which lab you''re interested in, and I can give you more details!','\n',char(10)),0,NULL,NULL,'2025-06-29 16:20:34.531918');
INSERT INTO chat_messages VALUES(7,3,'what lab is this',1,'general_info','{"facility": null, "location": null, "issue_type": null, "component": null}','2025-06-29 16:40:02.273777');
INSERT INTO chat_messages VALUES(8,3,replace('It seems you''re asking about the lab you''re currently in. Could you share more details about the lab''s location (e.g., building, level) or its features?  \n\nHere’s a quick list of bookable labs at UTM:  \n- **Computer Lab** – N28 & N28a, FC  \n- **CCNP Network Lab** – Level 4, N28, FC  \n\nLet me know if you need specifics!','\n',char(10)),0,NULL,NULL,'2025-06-29 16:40:02.275772');
INSERT INTO chat_messages VALUES(9,3,'what lab',1,'search','{"facility": "lab", "location": null, "issue_type": null, "component": null}','2025-06-29 16:41:02.228674');
INSERT INTO chat_messages VALUES(10,3,replace('Here are the labs available at UTM:  \n\n1. **Computer Lab** – Located at N28 & N28a, FC (Bookable)  \n2. **CCNP Network Lab** – Located at Level 4, N28, FC (Bookable)  \n\nLet me know if you need details on booking or any specific lab!','\n',char(10)),0,NULL,NULL,'2025-06-29 16:41:02.229437');
INSERT INTO chat_messages VALUES(11,3,'Where is the computer lab?',1,'search','{"facility": "Computer Lab", "location": null, "issue_type": null, "component": null}','2025-06-29 16:47:21.251598');
INSERT INTO chat_messages VALUES(12,3,'🖥️ **Computer Lab 1** is located at **Block A, Level 2**. It has 40 workstations and is available for booking. You can use it for coursework and projects.',0,NULL,NULL,'2025-06-29 16:47:21.252595');
INSERT INTO chat_messages VALUES(13,3,'Where is the computer lab?',1,'search','{"facility": "Computer Lab", "location": null, "issue_type": null, "component": null}','2025-06-29 16:51:14.234036');
INSERT INTO chat_messages VALUES(14,3,'🖥️ **Computer Lab 1** is located at **Block A, Level 2**. It has 40 workstations and is available for booking. You can use it for coursework and projects.',0,NULL,NULL,'2025-06-29 16:51:14.235033');
INSERT INTO chat_messages VALUES(15,3,'what lab is this',1,'general_info','{"facility": null, "location": null, "issue_type": null, "component": null}','2025-06-29 16:51:53.266309');
INSERT INTO chat_messages VALUES(16,3,'🖥️ **Computer Lab 1** is located at **Block A, Level 2**. It has 40 workstations and is available for booking. You can use it for coursework and projects.',0,NULL,NULL,'2025-06-29 16:51:53.267311');
INSERT INTO chat_messages VALUES(17,3,'tell me the name of the lab',1,'general_info','{}','2025-06-29 16:52:58.270728');
INSERT INTO chat_messages VALUES(18,3,'🖥️ **Computer Lab 1** is located at **Block A, Level 2**. It has 40 workstations and is available for booking. You can use it for coursework and projects.',0,NULL,NULL,'2025-06-29 16:52:58.271725');
INSERT INTO chat_messages VALUES(19,3,'tell me the name of the lab',1,'general_info','{}','2025-06-29 16:56:18.274827');
INSERT INTO chat_messages VALUES(20,3,'🖥️ **Computer Lab 1** is located at **Block A, Level 2**. It has 40 workstations and is available for booking. You can use it for coursework and projects.',0,NULL,NULL,'2025-06-29 16:56:18.274993');
COMMIT;
