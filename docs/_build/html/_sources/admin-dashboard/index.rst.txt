Admin Dashboard
===============

The admin dashboard is the central control panel for managing the UTM Campus Assistant system. This guide covers all administrative functions and features available to system administrators.

Accessing the Admin Dashboard
-----------------------------

1. **Login as Administrator**
   
   Navigate to the login page and enter your admin credentials.

2. **Dashboard Overview**
   
   Upon login, administrators are automatically redirected to the admin dashboard at ``/admin_dashboard``.

Dashboard Layout
----------------

The admin dashboard is organized into several key sections:

Header Section
~~~~~~~~~~~~~~

- **System Status Indicator**: Shows overall system health
- **User Profile**: Quick access to admin profile settings
- **Navigation Menu**: Links to all admin functions
- **Logout Option**: Secure session termination

Main Dashboard Cards
~~~~~~~~~~~~~~~~~~~~

The dashboard displays key metrics and quick actions:

.. list-table:: Dashboard Metrics
   :widths: 25 75
   :header-rows: 1

   * - Metric
     - Description
   * - Total Issues
     - Count of all facility issues in the system
   * - Pending Issues
     - Issues awaiting admin attention
   * - Active Users
     - Number of registered users
   * - Facilities
     - Total facility count in the system

Quick Actions Panel
~~~~~~~~~~~~~~~~~~~

Provides one-click access to common administrative tasks:

- **View All Issues**: Direct link to issue management
- **Manage Users**: Access user administration
- **Facility Management**: Edit facility information
- **System Settings**: Configure system parameters
- **Generate Reports**: Create system reports

Core Administrative Functions
-----------------------------

Issue Management
~~~~~~~~~~~~~~~~

**Viewing Issues**

1. Click "View All Issues" from the dashboard
2. Issues are displayed in a sortable table with:
   
   - Issue ID and title
   - Reporter information
   - Priority level (Urgent, High, Medium, Low)
   - Current status
   - Creation date
   - Assigned administrator

**Issue Status Management**

Administrators can update issue status through several states:

.. mermaid::
   
   graph LR
       A[Reported] --> B[In Progress]
       B --> C[Resolved]
       C --> D[Closed]
       B --> A
       C --> B

**Status Definitions:**

- **Reported**: New issue awaiting review
- **In Progress**: Issue being actively worked on
- **Resolved**: Issue fixed, awaiting user confirmation
- **Closed**: Issue completed with user feedback

**Updating Issue Status**

1. Click on an issue ID to view details
2. Select new status from dropdown
3. Add admin notes (optional but recommended)
4. Click "Update Status"

**Issue Assignment**

- Assign issues to specific administrators
- Track workload distribution
- Set priority levels for urgent matters

User Management
~~~~~~~~~~~~~~~

**User Overview**

Access user management through the "Manage Users" link:

- View all registered users
- See user roles (Student/Admin)
- Check account creation dates
- Monitor user activity

**User Roles**

The system supports two primary roles:

.. list-table:: User Roles
   :widths: 25 75
   :header-rows: 1

   * - Role
     - Permissions
   * - Student
     - Report issues, use chatbot, view facilities, track own issues
   * - Admin
     - All student permissions plus: manage users, update issues, system administration

**Promoting Users to Admin**

To grant admin privileges:

1. Navigate to user management
2. Locate the target user
3. Click "Promote to Admin"
4. Confirm the action

.. warning::
   Admin privileges provide full system access. Only promote trusted users.

**User Account Management**

- Reset user passwords
- Deactivate problematic accounts
- View user activity logs
- Update user information

Facility Management
~~~~~~~~~~~~~~~~~~~

The facility management system provides comprehensive tools for managing campus facilities.

**Accessing Facility Management**

Navigate to facility management through:

1. Admin Dashboard → "Manage Facilities" button
2. Quick Actions panel → "Manage Facilities"
3. Direct URL: ``/manage_facilities``

**Adding New Facilities**

To add a new facility:

1. Click "Add New Facility" from the management page
2. Fill in the facility information form:
   
   - **Facility Name**: Clear, descriptive name
   - **Category**: Select from predefined categories
   - **Location**: Detailed location with building and room
   - **Description**: Comprehensive facility description
   - **Capacity**: Maximum occupancy (optional)
   - **Operating Hours**: When facility is available
   - **Contact Info**: Landmarks and contact details
   - **Bookable**: Whether students can book online
   - **Active**: Whether facility is currently active

3. Click "Save Facility" to create

**Editing Existing Facilities**

To modify facility information:

1. Navigate to "Manage Facilities"
2. Locate the facility in the table
3. Click the "Edit" (pencil) icon
4. Update any necessary information
5. Save changes

**Facility Status Management**

**Activating/Deactivating Facilities**

- Click the "Pause/Play" icon to toggle facility status
- Inactive facilities are hidden from students
- Existing bookings remain valid
- Use this for temporary closures

**Deleting Facilities**

.. warning::
   Facility deletion is permanent and cannot be undone.

To delete a facility:

1. Click the "Delete" (trash) icon
2. Confirm deletion in the modal dialog
3. Facilities with existing bookings or issues cannot be deleted

**Facility Categories**

The system supports seven facility categories:

.. list-table:: Facility Categories
   :widths: 20 80
   :header-rows: 1

   * - Category
     - Examples
   * - Laboratory
     - Computer labs, research facilities, science labs
   * - Academic
     - Classrooms, lecture halls, libraries, study rooms
   * - Sports
     - Gymnasium, sports complex, fields, courts
   * - Administrative
     - Offices, meeting rooms, conference rooms
   * - Accommodation
     - Student housing, dormitories, hostels
   * - Dining
     - Cafeterias, food courts, restaurants
   * - Event
     - Event halls, auditoriums, theaters

**Search and Filtering**

The facility management interface provides:

- **Text Search**: Search by name or location
- **Category Filter**: Filter by facility category
- **Status Filter**: Show active, inactive, or all facilities
- **Clear Filters**: Reset all search criteria

**Facility Booking Configuration**

Administrators can control booking availability:

- **Bookable Facilities**: Only certain categories should be bookable
  
  - Recommended: Laboratory, Event, Administrative (meeting rooms)
  - Not recommended: Dining, Accommodation

- **Booking Permissions**: Set which facilities students can book
- **Capacity Limits**: Define maximum occupancy
- **Operating Hours**: Set availability windows

**Best Practices for Facility Management**

**Naming Conventions**

- Use clear, descriptive names
- Include building and room numbers
- Avoid abbreviations that may confuse users
- Example: "Computer Lab 1 - Block A" not "CL1-BA"

**Location Descriptions**

- Provide detailed location information
- Include building, floor, and room number
- Add nearby landmarks for easier navigation
- Example: "Block A, Level 2, Room A201 (near main entrance)"

**Facility Descriptions**

- Include equipment and features available
- Mention capacity and layout
- Note any special requirements
- Update regularly to reflect changes

**Status Management**

- Use deactivation instead of deletion when possible
- Keep historical data for reporting
- Communicate facility closures to users
- Regular review of facility status

**Data Integrity Considerations**

The system prevents data loss through:

- **Relationship Protection**: Facilities with bookings/issues cannot be deleted
- **Status Tracking**: Maintains audit trail of changes
- **Cache Updates**: Automatically refreshes AI service data
- **Validation**: Ensures required fields are completed

Booking Request Workflow
~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::
   
   graph TD
       A[Student Request] --> B[Pending Review]
       B --> C{Admin Decision}
       C -->|Approve| D[Approved]
       C -->|Reject| E[Rejected]
       D --> F[Active Booking]
       E --> G[Notification Sent]

**Managing Booking Requests**

1. Access "Manage Bookings" from the dashboard
2. Review pending requests
3. Check for conflicts
4. Approve or reject with notes
5. Send notifications to users

System Administration
---------------------

Database Management
~~~~~~~~~~~~~~~~~~~

**Database Status**

Monitor database health and performance:

- Connection status
- Database size
- Query performance
- Backup status

**Database Operations**

Available operations for administrators:

- **Refresh Cache**: Update facility information cache
- **Reset Database**: Restore to initial state (development only)
- **Export Data**: Generate database backups
- **Import Data**: Restore from backups

.. danger::
   Database reset will permanently delete all data. Use only in development environments.

AI Service Management
~~~~~~~~~~~~~~~~~~~~~

**AI Service Status**

Monitor the chatbot AI service:

- Connection status to DeepSeek LLM
- Response time metrics
- Error rates
- Cache status

**AI Configuration**

Administrators can:

- Test AI connectivity
- Refresh facility cache
- Monitor conversation logs
- Adjust AI response parameters

System Monitoring
~~~~~~~~~~~~~~~~~

**Performance Metrics**

Track system performance through:

- Response times
- User activity levels
- Error rates
- Resource usage

**System Health Checks**

Regular monitoring includes:

- Database connectivity
- AI service availability
- File system status
- Network connectivity

**Log Management**

Access and review system logs:

- Application logs
- Error logs
- User activity logs
- Security logs

Security Management
~~~~~~~~~~~~~~~~~~~

**Session Management**

- Monitor active user sessions
- Force logout suspicious sessions
- Set session timeout policies

**Access Control**

- Review user permissions
- Audit admin actions
- Monitor failed login attempts

**Security Settings**

Configure security parameters:

- Password policies
- Session timeouts
- Login attempt limits
- Security notifications

Reporting and Analytics
-----------------------

**Issue Reports**

Generate reports on:

- Issue resolution times
- Issue categories and trends
- User activity patterns
- Facility usage statistics

**User Analytics**

Track user engagement:

- Registration trends
- Feature usage
- Support request patterns
- Geographic distribution

**Facility Utilization**

Monitor facility usage:

- Booking frequency
- Popular facilities
- Peak usage times
- Maintenance patterns

**Custom Reports**

Create custom reports for:

- Management presentations
- Budget planning
- Resource allocation
- Performance reviews

Best Practices
--------------

Daily Administration Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Review New Issues**
   
   - Check for urgent issues
   - Assign issues to appropriate staff
   - Update issue status

2. **Monitor System Health**
   
   - Check system performance
   - Review error logs
   - Verify backup status

3. **User Support**
   
   - Respond to user queries
   - Process access requests
   - Handle password resets

Weekly Administration Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **System Maintenance**
   
   - Review system performance
   - Update facility information
   - Clean up old data

2. **Security Review**
   
   - Audit user accounts
   - Review access logs
   - Update security settings

3. **Reporting**
   
   - Generate weekly reports
   - Review usage analytics
   - Plan improvements

Monthly Administration Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **System Updates**
   
   - Apply security patches
   - Update dependencies
   - Review system configuration

2. **Data Management**
   
   - Perform database maintenance
   - Archive old records
   - Verify backup integrity

3. **Planning**
   
   - Review user feedback
   - Plan system improvements
   - Update documentation

Troubleshooting Common Issues
-----------------------------

Dashboard Access Problems
~~~~~~~~~~~~~~~~~~~~~~~~~

**Cannot Access Dashboard**

1. Verify admin role assignment
2. Check session validity
3. Clear browser cache
4. Review server logs

**Performance Issues**

1. Check system resources
2. Review database performance
3. Monitor network connectivity
4. Analyze user load

**Feature Malfunctions**

1. Check error logs
2. Verify database connectivity
3. Test AI service status
4. Review configuration settings

Getting Help
------------

If you encounter issues not covered in this guide:

1. **Check the troubleshooting section**: :doc:`../troubleshooting/index`
2. **Review system logs**: Look for error messages
3. **Contact IT Support**: it-support@utm.my
4. **Emergency Contact**: +60-7-553-4100

Next Steps
----------

After mastering the admin dashboard:

1. Explore :doc:`../user-management/index` for detailed user administration
2. Learn about :doc:`../facility-management/index` for facility operations
3. Review :doc:`../monitoring/index` for system monitoring
4. Set up :doc:`../backup/index` for data protection