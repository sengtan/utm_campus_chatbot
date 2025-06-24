Database Schema Reference
=========================

This document describes the complete database schema for the UTM Campus Assistant system.

Overview
--------

The system uses SQLite as the default database with the following core tables:

- **users**: User account information
- **facilities**: Campus facility data
- **issues**: Facility issue reports
- **facility_bookings**: Facility booking requests
- **chat_sessions**: Chatbot conversation sessions
- **chat_messages**: Individual chat messages

Entity Relationship Diagram
---------------------------

.. code-block:: text

   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │    users    │    │ facilities  │    │   issues    │
   │─────────────│    │─────────────│    │─────────────│
   │ id (PK)     │◄──┐│ id (PK)     │◄──┐│ id (PK)     │
   │ username    │   ││ name        │   ││ title       │
   │ email       │   ││ category    │   ││ description │
   │ password_hash│   ││ location    │   ││ user_id (FK)│
   │ role        │   ││ description │   ││facility_id │
   │ full_name   │   ││ is_bookable │   │└─────────────┘
   │ student_id  │   ││ capacity    │   │
   │ created_at  │   │└─────────────┘   │
   └─────────────┘   │                  │
           │         │                  │
           │         │ ┌─────────────┐  │
           │         └─┤facility_    │  │
           │           │bookings     │  │
           │           │─────────────│  │
           │           │ id (PK)     │  │
           │           │facility_id  │  │
           │           │ user_id (FK)├──┘
           │           │booking_date │
           │           │ start_hour  │
           │           │ end_hour    │
           │           │ status      │
           │           └─────────────┘
           │
           │ ┌─────────────┐    ┌─────────────┐
           └─┤chat_sessions│◄──┐│chat_messages│
             │─────────────│   ││─────────────│
             │ id (PK)     │   ││ id (PK)     │
             │ user_id (FK)│   ││session_id   │
             │ session_id  │   ││ message     │
             │ created_at  │   ││ is_user     │
             └─────────────┘   ││ intent      │
                               ││ entities    │
                               │└─────────────┘
                               │
                               └──────────────────┘

Table Schemas
-------------

users
~~~~~

Stores user account information for both students and administrators.

.. list-table:: users Table Schema
   :widths: 20 20 15 45
   :header-rows: 1

   * - Column
     - Type
     - Constraints
     - Description
   * - id
     - INTEGER
     - PRIMARY KEY
     - Unique user identifier
   * - username
     - VARCHAR(80)
     - UNIQUE, NOT NULL
     - Login username (4-20 characters)
   * - email
     - VARCHAR(120)
     - UNIQUE, NOT NULL
     - User email address
   * - password_hash
     - VARCHAR(256)
     - NOT NULL
     - Bcrypt hashed password
   * - role
     - ENUM
     - NOT NULL, DEFAULT 'student'
     - User role (student/admin)
   * - full_name
     - VARCHAR(100)
     - NOT NULL
     - Complete user name
   * - student_id
     - VARCHAR(20)
     - UNIQUE, NULLABLE
     - University student ID
   * - created_at
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Account creation time

**Indexes:**
- Unique index on username
- Unique index on email
- Unique index on student_id (where not null)

**Example Record:**

.. code-block:: sql

   INSERT INTO users VALUES (
       1,
       'student001',
       'student001@utm.my',
       '$2b$12$hash...',
       'student',
       'Ahmad bin Ali',
       'A20EC0001',
       '2025-01-15 10:30:00'
   );

facilities
~~~~~~~~~~

Contains information about campus facilities available for booking and issue reporting.

.. list-table:: facilities Table Schema
   :widths: 20 20 15 45
   :header-rows: 1

   * - Column
     - Type
     - Constraints
     - Description
   * - id
     - INTEGER
     - PRIMARY KEY
     - Unique facility identifier
   * - name
     - VARCHAR(100)
     - NOT NULL
     - Facility name
   * - category
     - VARCHAR(50)
     - NOT NULL
     - Facility category
   * - location
     - VARCHAR(200)
     - NOT NULL
     - Physical location description
   * - description
     - TEXT
     - NULLABLE
     - Detailed facility description
   * - is_bookable
     - BOOLEAN
     - DEFAULT FALSE
     - Whether facility can be booked
   * - capacity
     - INTEGER
     - NULLABLE
     - Maximum occupancy
   * - operating_hours
     - VARCHAR(100)
     - NULLABLE
     - Operating hours description
   * - contact_info
     - VARCHAR(200)
     - NULLABLE
     - Contact information/landmarks
   * - created_at
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Record creation time

**Indexes:**
- Index on category
- Index on is_bookable
- Index on name

**Facility Categories:**
- Laboratory
- Academic
- Sports
- Administrative
- Accommodation
- Dining
- Event

**Example Record:**

.. code-block:: sql

   INSERT INTO facilities VALUES (
       1,
       'Computer Lab 1',
       'Laboratory',
       'Block A, Level 2, Room A201',
       'Main computer lab with 40 workstations equipped with latest software',
       TRUE,
       40,
       '8:00 AM - 6:00 PM (Mon-Fri)',
       'Near main entrance, Landmarks: Faculty of Computing building',
       '2025-01-10 09:00:00'
   );

issues
~~~~~~

Tracks facility-related issues reported by users.

.. list-table:: issues Table Schema
   :widths: 20 20 15 45
   :header-rows: 1

   * - Column
     - Type
     - Constraints
     - Description
   * - id
     - INTEGER
     - PRIMARY KEY
     - Unique issue identifier
   * - title
     - VARCHAR(200)
     - NOT NULL
     - Issue title/summary
   * - description
     - TEXT
     - NOT NULL
     - Detailed issue description
   * - issue_type
     - ENUM
     - NOT NULL
     - Type of issue
   * - priority
     - ENUM
     - DEFAULT 'medium'
     - Issue priority level
   * - status
     - ENUM
     - DEFAULT 'reported'
     - Current issue status
   * - location
     - VARCHAR(200)
     - NOT NULL
     - Issue location
   * - user_id
     - INTEGER
     - FOREIGN KEY
     - Reporter user ID
   * - facility_id
     - INTEGER
     - FOREIGN KEY, NULLABLE
     - Related facility ID
   * - assigned_to
     - INTEGER
     - FOREIGN KEY, NULLABLE
     - Assigned admin user ID
   * - admin_notes
     - TEXT
     - NULLABLE
     - Administrative notes
   * - feedback_rating
     - INTEGER
     - NULLABLE
     - User feedback rating (1-5)
   * - feedback_comment
     - TEXT
     - NULLABLE
     - User feedback comment
   * - created_at
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Issue creation time
   * - updated_at
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Last update time
   * - resolved_at
     - DATETIME
     - NULLABLE
     - Resolution timestamp

**Enums:**

- **issue_type**: electrical, hygiene, structural, equipment, security, other
- **priority**: low, medium, high, urgent
- **status**: reported, in_progress, resolved, closed

**Foreign Keys:**
- user_id → users.id
- facility_id → facilities.id
- assigned_to → users.id

**Indexes:**
- Index on user_id
- Index on facility_id
- Index on status
- Index on priority
- Index on created_at

**Example Record:**

.. code-block:: sql

   INSERT INTO issues VALUES (
       1,
       'Air conditioning not working',
       'The air conditioning unit in Computer Lab 1 has been malfunctioning since yesterday. Room temperature is too high for comfortable use.',
       'equipment',
       'high',
       'reported',
       'Computer Lab 1, Block A Level 2',
       1,
       1,
       NULL,
       NULL,
       NULL,
       NULL,
       '2025-01-20 14:30:00',
       '2025-01-20 14:30:00',
       NULL
   );

facility_bookings
~~~~~~~~~~~~~~~~~

Manages facility booking requests and schedules.

.. list-table:: facility_bookings Table Schema
   :widths: 20 20 15 45
   :header-rows: 1

   * - Column
     - Type
     - Constraints
     - Description
   * - id
     - INTEGER
     - PRIMARY KEY
     - Unique booking identifier
   * - facility_id
     - INTEGER
     - FOREIGN KEY, NOT NULL
     - Booked facility ID
   * - user_id
     - INTEGER
     - FOREIGN KEY, NOT NULL
     - Booking user ID
   * - booking_date
     - DATE
     - NOT NULL
     - Booking date
   * - start_hour
     - INTEGER
     - NOT NULL
     - Start hour (0-23)
   * - end_hour
     - INTEGER
     - NOT NULL
     - End hour (0-23)
   * - purpose
     - VARCHAR(200)
     - NULLABLE
     - Booking purpose description
   * - status
     - ENUM
     - DEFAULT 'pending'
     - Booking status
   * - admin_notes
     - TEXT
     - NULLABLE
     - Administrative notes
   * - created_at
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Booking request time
   * - updated_at
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Last update time

**Enums:**
- **status**: pending, approved, rejected, cancelled

**Foreign Keys:**
- facility_id → facilities.id
- user_id → users.id

**Indexes:**
- Index on facility_id
- Index on user_id
- Index on booking_date
- Index on status
- Composite index on (facility_id, booking_date)

**Constraints:**
- end_hour must be greater than start_hour
- booking_date must be in the future
- No overlapping bookings for same facility

**Example Record:**

.. code-block:: sql

   INSERT INTO facility_bookings VALUES (
       1,
       1,
       1,
       '2025-01-25',
       9,
       11,
       'Software development workshop for final year students',
       'pending',
       NULL,
       '2025-01-20 10:15:00',
       '2025-01-20 10:15:00'
   );

chat_sessions
~~~~~~~~~~~~~

Manages chatbot conversation sessions.

.. list-table:: chat_sessions Table Schema
   :widths: 20 20 15 45
   :header-rows: 1

   * - Column
     - Type
     - Constraints
     - Description
   * - id
     - INTEGER
     - PRIMARY KEY
     - Unique session identifier
   * - user_id
     - INTEGER
     - FOREIGN KEY, NOT NULL
     - Session user ID
   * - session_id
     - VARCHAR(50)
     - NOT NULL
     - Session UUID
   * - created_at
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Session start time

**Foreign Keys:**
- user_id → users.id

**Indexes:**
- Index on user_id
- Index on session_id
- Index on created_at

chat_messages
~~~~~~~~~~~~~

Stores individual messages within chat sessions.

.. list-table:: chat_messages Table Schema
   :widths: 20 20 15 45
   :header-rows: 1

   * - Column
     - Type
     - Constraints
     - Description
   * - id
     - INTEGER
     - PRIMARY KEY
     - Unique message identifier
   * - session_id
     - INTEGER
     - FOREIGN KEY, NOT NULL
     - Chat session ID
   * - message
     - TEXT
     - NOT NULL
     - Message content
   * - is_user
     - BOOLEAN
     - NOT NULL
     - True if user message, false if bot
   * - intent
     - VARCHAR(50)
     - NULLABLE
     - Detected user intent
   * - entities
     - JSON
     - NULLABLE
     - Extracted entities
   * - timestamp
     - DATETIME
     - DEFAULT CURRENT_TIMESTAMP
     - Message timestamp

**Foreign Keys:**
- session_id → chat_sessions.id

**Indexes:**
- Index on session_id
- Index on timestamp
- Index on is_user

Database Operations
-------------------

Common Queries
~~~~~~~~~~~~~~

**User Management:**

.. code-block:: sql

   -- Find all admin users
   SELECT username, email, full_name FROM users WHERE role = 'admin';
   
   -- Count users by role
   SELECT role, COUNT(*) FROM users GROUP BY role;
   
   -- Find users registered in last 7 days
   SELECT username, email, created_at FROM users 
   WHERE created_at >= datetime('now', '-7 days');

**Issue Management:**

.. code-block:: sql

   -- Find all open issues
   SELECT i.id, i.title, u.full_name as reporter, i.priority, i.status
   FROM issues i
   JOIN users u ON i.user_id = u.id
   WHERE i.status IN ('reported', 'in_progress');
   
   -- Count issues by status
   SELECT status, COUNT(*) FROM issues GROUP BY status;
   
   -- Find high priority unassigned issues
   SELECT id, title, priority, created_at FROM issues
   WHERE priority = 'high' AND assigned_to IS NULL;

**Facility Management:**

.. code-block:: sql

   -- List all bookable facilities
   SELECT name, category, location, capacity FROM facilities 
   WHERE is_bookable = TRUE;
   
   -- Find facility utilization
   SELECT f.name, COUNT(fb.id) as booking_count
   FROM facilities f
   LEFT JOIN facility_bookings fb ON f.id = fb.facility_id
   WHERE fb.status = 'approved'
   GROUP BY f.id, f.name
   ORDER BY booking_count DESC;

**Booking Management:**

.. code-block:: sql

   -- Find pending bookings
   SELECT fb.id, f.name, u.full_name, fb.booking_date, fb.start_hour, fb.end_hour
   FROM facility_bookings fb
   JOIN facilities f ON fb.facility_id = f.id
   JOIN users u ON fb.user_id = u.id
   WHERE fb.status = 'pending'
   ORDER BY fb.booking_date, fb.start_hour;
   
   -- Check for booking conflicts
   SELECT fb1.id, fb2.id, f.name, fb1.booking_date
   FROM facility_bookings fb1
   JOIN facility_bookings fb2 ON fb1.facility_id = fb2.facility_id
   JOIN facilities f ON fb1.facility_id = f.id
   WHERE fb1.id != fb2.id
   AND fb1.booking_date = fb2.booking_date
   AND fb1.start_hour < fb2.end_hour
   AND fb1.end_hour > fb2.start_hour
   AND fb1.status IN ('approved', 'pending')
   AND fb2.status IN ('approved', 'pending');

Database Maintenance
--------------------

Regular Maintenance Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~

**Daily Tasks:**

.. code-block:: sql

   -- Clean up old chat sessions (older than 30 days)
   DELETE FROM chat_messages WHERE session_id IN (
       SELECT id FROM chat_sessions 
       WHERE created_at < datetime('now', '-30 days')
   );
   
   DELETE FROM chat_sessions 
   WHERE created_at < datetime('now', '-30 days');

**Weekly Tasks:**

.. code-block:: sql

   -- Vacuum database to reclaim space
   VACUUM;
   
   -- Analyze tables for query optimization
   ANALYZE;
   
   -- Check database integrity
   PRAGMA integrity_check;

**Monthly Tasks:**

.. code-block:: sql

   -- Archive old resolved issues (optional)
   CREATE TABLE IF NOT EXISTS issues_archive AS 
   SELECT * FROM issues WHERE 0; -- Create structure only
   
   INSERT INTO issues_archive 
   SELECT * FROM issues 
   WHERE status = 'closed' 
   AND resolved_at < datetime('now', '-90 days');

Backup and Recovery
~~~~~~~~~~~~~~~~~~~

**Database Backup:**

.. code-block:: bash

   # Create database backup
   cp instance/utm_campus.db backups/utm_campus_$(date +%Y%m%d_%H%M%S).db
   
   # Create SQL dump
   sqlite3 instance/utm_campus.db .dump > backups/utm_campus_$(date +%Y%m%d).sql

**Database Recovery:**

.. code-block:: bash

   # Restore from backup file
   cp backups/utm_campus_YYYYMMDD_HHMMSS.db instance/utm_campus.db
   
   # Restore from SQL dump
   sqlite3 instance/utm_campus_new.db < backups/utm_campus_YYYYMMDD.sql

Performance Optimization
-------------------------

Index Optimization
~~~~~~~~~~~~~~~~~~

Current indexes provide efficient querying for:

- User lookups by username/email
- Issue filtering by status/priority
- Facility searches by category
- Booking conflicts detection
- Chat session retrieval

**Monitor Query Performance:**

.. code-block:: sql

   -- Enable query plan output
   .eqp on
   
   -- Analyze slow queries
   EXPLAIN QUERY PLAN 
   SELECT * FROM issues 
   WHERE status = 'reported' 
   ORDER BY created_at DESC;

Database Size Management
~~~~~~~~~~~~~~~~~~~~~~~~

**Monitor Database Size:**

.. code-block:: bash

   # Check database file size
   du -h instance/utm_campus.db
   
   # Check table sizes
   sqlite3 instance/utm_campus.db "
   SELECT name, 
          COUNT(*) as row_count
   FROM sqlite_master m
   JOIN pragma_table_info(m.name) p
   WHERE m.type = 'table'
   GROUP BY name;"

Migration Scripts
-----------------

Schema Updates
~~~~~~~~~~~~~~

When updating the database schema, use migration scripts:

.. code-block:: python

   # Example migration script
   from app import app, db
   
   def migrate_add_column():
       with app.app_context():
           # Add new column to existing table
           db.engine.execute('ALTER TABLE users ADD COLUMN last_login DATETIME')
           db.session.commit()
           print('Migration completed: Added last_login column')

Data Migration
~~~~~~~~~~~~~~

For data transformations:

.. code-block:: python

   def migrate_facility_categories():
       with app.app_context():
           # Update old category names to new standard
           facilities = Facility.query.filter_by(category='Lab').all()
           for facility in facilities:
               facility.category = 'Laboratory'
           db.session.commit()
           print(f'Updated {len(facilities)} facility categories')

Security Considerations
-----------------------

Data Protection
~~~~~~~~~~~~~~~

- **Password Hashing**: All passwords stored using bcrypt
- **Input Validation**: All user inputs validated and sanitized
- **SQL Injection Prevention**: Using SQLAlchemy ORM with parameterized queries
- **Session Security**: Secure session cookies with proper configuration

Access Control
~~~~~~~~~~~~~~

- **Role-Based Access**: Users can only access appropriate data
- **Data Isolation**: Users can only see their own issues and bookings
- **Admin Auditing**: All admin actions should be logged

Backup Security
~~~~~~~~~~~~~~~

- **Encrypted Backups**: Consider encrypting database backups
- **Secure Storage**: Store backups in secure, access-controlled locations
- **Regular Testing**: Regularly test backup restoration procedures