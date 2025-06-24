Facility Management
===================

This comprehensive guide covers all aspects of managing campus facilities in the UTM Campus Assistant system.

Overview
--------

The facility management system provides administrators with complete control over campus facilities, including adding new facilities, modifying existing ones, and managing facility status. The system ensures data integrity while providing flexible management capabilities.

Facility Management Interface
-----------------------------

Accessing Facility Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access the facility management system through multiple paths:

1. **Admin Dashboard**: Click "Manage Facilities" from the quick actions panel
2. **Direct Navigation**: Use the URL ``/manage_facilities``
3. **Menu Navigation**: Admin menu → Facility Management

The interface provides a comprehensive view of all facilities with search, filtering, and management capabilities.

Main Features
~~~~~~~~~~~~~

**Facility Overview Table**

The main interface displays facilities in a sortable table showing:

- Facility name and description
- Category and location
- Capacity information
- Booking availability status
- Active/inactive status
- Creation date
- Quick action buttons

**Search and Filter Options**

- **Text Search**: Search by facility name or location
- **Category Filter**: Filter by facility type
- **Status Filter**: Show active, inactive, or all facilities
- **Combined Filtering**: Use multiple filters simultaneously

Adding New Facilities
---------------------

Step-by-Step Process
~~~~~~~~~~~~~~~~~~~~

1. **Navigate to Add Facility**
   
   Click "Add New Facility" from the facility management page.

2. **Complete Facility Information**
   
   Fill in all required and optional fields:

   .. list-table:: Facility Form Fields
      :widths: 25 15 60
      :header-rows: 1

      * - Field
        - Required
        - Description
      * - Facility Name
        - Yes
        - Clear, descriptive name (2-100 characters)
      * - Category
        - Yes
        - Select from predefined categories
      * - Location
        - Yes
        - Detailed location with building/room (5-200 characters)
      * - Description
        - No
        - Comprehensive facility description (up to 1000 characters)
      * - Capacity
        - No
        - Maximum occupancy (1-1000 people)
      * - Operating Hours
        - No
        - When facility is available (up to 100 characters)
      * - Contact Info
        - No
        - Landmarks and contact details (up to 200 characters)
      * - Can be Booked
        - No
        - Enable online booking for students
      * - Active
        - No
        - Facility is visible and available (default: Yes)

3. **Save Facility**
   
   Click "Save Facility" to create the new facility.

Field Guidelines
~~~~~~~~~~~~~~~~

**Facility Name Best Practices**

- Use descriptive, unique names
- Include identifying information (building, floor)
- Avoid abbreviations that may confuse users
- Examples:
  
  - Good: "Computer Lab 1 - Block A"
  - Poor: "CL1" or "Lab"

**Location Format**

Structure location information hierarchically:

.. code-block:: text

   Building Name, Floor/Level, Room Number
   Example: "Faculty of Computing, Level 2, Room FC201"

**Category Selection**

Choose the most appropriate category:

- **Laboratory**: Computer labs, research facilities, science labs
- **Academic**: Classrooms, lecture halls, libraries
- **Sports**: Gymnasium, courts, sports facilities
- **Administrative**: Meeting rooms, offices
- **Accommodation**: Student housing, dormitories
- **Dining**: Cafeterias, food courts
- **Event**: Auditoriums, event halls

**Description Content**

Include relevant information such as:

- Equipment available
- Special features
- Accessibility information
- Usage restrictions
- Technical specifications

Editing Existing Facilities
---------------------------

Modification Process
~~~~~~~~~~~~~~~~~~~~

1. **Locate Facility**
   
   Use search and filters to find the facility in the management table.

2. **Access Edit Form**
   
   Click the edit (pencil) icon in the actions column.

3. **Update Information**
   
   Modify any fields as needed. All fields can be updated.

4. **Save Changes**
   
   Click "Save Facility" to apply updates.

Edit Form Features
~~~~~~~~~~~~~~~~~~

**Pre-populated Fields**

The edit form displays current facility information with:

- All existing field values
- Creation date and last update timestamp
- Usage statistics (bookings, issues)

**Change Tracking**

The system tracks:

- When facilities were last updated
- Which administrator made changes
- Historical facility information

**Validation**

The same validation rules apply as when adding facilities:

- Required fields must be completed
- Capacity must be within valid range
- Text fields respect character limits

Facility Status Management
--------------------------

Active/Inactive Status
~~~~~~~~~~~~~~~~~~~~~~

**Status Meanings**

- **Active**: Facility is visible to users and can be booked
- **Inactive**: Facility is hidden from users but data is preserved

**Toggling Status**

1. Locate facility in the management table
2. Click the pause/play icon in the actions column
3. Confirm the status change
4. System updates immediately

**Effects of Status Changes**

**Deactivating Facilities**

- Facility disappears from student view
- Existing bookings remain valid
- AI chatbot excludes from recommendations
- Admin can still view and manage

**Reactivating Facilities**

- Facility becomes visible to students
- Booking availability restored (if enabled)
- AI chatbot includes in responses
- All historical data preserved

Facility Deletion
-----------------

.. warning::
   Facility deletion is permanent and cannot be undone. Consider deactivation instead.

Deletion Process
~~~~~~~~~~~~~~~~

1. **Check Dependencies**
   
   System automatically checks for:
   
   - Associated facility bookings
   - Related issue reports
   - Historical data references

2. **Attempt Deletion**
   
   Click the delete (trash) icon in the actions column.

3. **Confirmation Dialog**
   
   Review the confirmation dialog carefully:
   
   - Displays facility name
   - Shows warning about permanence
   - Notes about dependencies

4. **Final Confirmation**
   
   Click "Delete Permanently" to proceed.

Deletion Restrictions
~~~~~~~~~~~~~~~~~~~~~

**Protected Facilities**

Facilities cannot be deleted if they have:

- Active or historical bookings
- Associated issue reports
- Pending approval requests

**Alternative Actions**

Instead of deletion, consider:

- **Deactivation**: Hide facility while preserving data
- **Status Update**: Mark as unavailable temporarily
- **Category Change**: Reclassify facility type

**Error Handling**

If deletion fails, the system provides clear error messages:

- Specific count of blocking records
- Suggestion to deactivate instead
- Links to view blocking records

Booking Configuration
---------------------

Bookable Facility Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Enabling Booking**

To make a facility bookable:

1. Edit the facility
2. Check "Can be Booked"
3. Ensure facility is active
4. Save changes

**Booking Recommendations**

**Suitable for Booking**

- Computer labs and teaching labs
- Meeting rooms and conference rooms
- Event halls and auditoriums
- Study rooms and group spaces

**Not Suitable for Booking**

- Dining facilities (cafeterias, restaurants)
- Accommodation (dormitories, housing)
- Administrative offices
- Public spaces (lobbies, corridors)

**Capacity Considerations**

Set appropriate capacity limits for:

- Fire safety compliance
- COVID-19 restrictions
- Equipment limitations
- Space constraints

Facility Categories in Detail
-----------------------------

Laboratory Facilities
~~~~~~~~~~~~~~~~~~~~~

**Typical Features**

- Specialized equipment
- Computer workstations
- Research instruments
- Safety equipment

**Management Considerations**

- Regular equipment maintenance
- Software updates
- Safety protocols
- Booking time limits

**Example Facilities**

- Computer Lab 1 - 40 workstations with latest software
- Chemistry Lab A - Fume hoods and analytical equipment
- Engineering Workshop - 3D printers and manufacturing tools

Academic Facilities
~~~~~~~~~~~~~~~~~~~

**Typical Features**

- Classroom seating
- Presentation equipment
- Whiteboards/projectors
- Audio-visual systems

**Management Considerations**

- Furniture arrangements
- Technology maintenance
- Cleaning schedules
- Accessibility compliance

**Example Facilities**

- Lecture Hall A - 200-seat auditorium with AV system
- Seminar Room 3 - 20-person discussion space
- Library Study Room - Quiet individual study space

Sports Facilities
~~~~~~~~~~~~~~~~~

**Typical Features**

- Sports equipment
- Safety features
- Changing facilities
- First aid provisions

**Management Considerations**

- Equipment safety checks
- Weather restrictions
- Maintenance schedules
- Insurance requirements

**Example Facilities**

- Main Gymnasium - Full court with bleachers
- Tennis Court 1 - Outdoor hard court
- Swimming Pool - Olympic-size with lanes

Data Management and Reporting
-----------------------------

Facility Analytics
~~~~~~~~~~~~~~~~~~

**Usage Statistics**

Track facility utilization through:

- Booking frequency
- Popular time slots
- User demographics
- Cancellation rates

**Performance Metrics**

Monitor facility performance:

- Issue report frequency
- Resolution times
- User satisfaction ratings
- Maintenance costs

**Reporting Capabilities**

Generate reports for:

- Management reviews
- Budget planning
- Space utilization
- Maintenance scheduling

Data Export and Import
~~~~~~~~~~~~~~~~~~~~~~

**Export Facility Data**

.. code-block:: python

   # Example export script
   import csv
   from models import Facility
   
   facilities = Facility.query.all()
   with open('facilities_export.csv', 'w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(['Name', 'Category', 'Location', 'Capacity', 'Active'])
       for facility in facilities:
           writer.writerow([
               facility.name,
               facility.category,
               facility.location,
               facility.capacity,
               facility.is_active
           ])

**Import Facility Data**

.. code-block:: python

   # Example import script
   import csv
   from models import Facility
   from app import db
   
   with open('facilities_import.csv', 'r') as file:
       reader = csv.DictReader(file)
       for row in reader:
           facility = Facility(
               name=row['Name'],
               category=row['Category'],
               location=row['Location'],
               capacity=int(row['Capacity']) if row['Capacity'] else None,
               is_active=row['Active'].lower() == 'true'
           )
           db.session.add(facility)
       db.session.commit()

Integration with Other Systems
------------------------------

AI Chatbot Integration
~~~~~~~~~~~~~~~~~~~~~~

**Cache Management**

The facility management system automatically:

- Updates AI service cache when facilities change
- Ensures chatbot has current facility information
- Filters inactive facilities from responses

**Search Optimization**

Facility data is optimized for AI search:

- Keywords extracted from descriptions
- Location information standardized
- Category-based filtering enabled

Booking System Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Automatic Updates**

Changes to facility booking status immediately affect:

- Available facilities in booking forms
- Booking validation rules
- Conflict detection algorithms

**Capacity Management**

Facility capacity settings control:

- Maximum booking sizes
- Overbooking prevention
- Resource allocation

Issue Management Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Facility Relationships**

Issues can be linked to specific facilities:

- Automatic facility suggestion based on location
- Facility-specific issue categories
- Maintenance tracking per facility

**Status Impact**

Facility status affects issue handling:

- Inactive facilities noted in issue context
- Maintenance issues may trigger status changes
- Resolution tracking per facility

Troubleshooting Facility Management
-----------------------------------

Common Issues
~~~~~~~~~~~~~

**Cannot Delete Facility**

**Problem**: Error message when attempting deletion

**Causes and Solutions**:

1. **Has Bookings**: Facility has associated bookings
   
   - Check booking history
   - Consider deactivation instead
   - Contact bookings to cancel if appropriate

2. **Has Issues**: Facility has associated issue reports
   
   - Review open issues
   - Resolve or close issues first
   - Archive old issues if policy allows

3. **System Error**: Database or application error
   
   - Check application logs
   - Verify database connectivity
   - Contact system administrator

**Facility Not Appearing in Booking**

**Problem**: Active, bookable facility not showing in booking form

**Troubleshooting Steps**:

1. Verify facility status:
   
   - Check "Active" checkbox is enabled
   - Verify "Can be Booked" is enabled
   - Confirm category is appropriate for booking

2. Clear system cache:
   
   - Use "Refresh Cache" in admin dashboard
   - Restart application if necessary

3. Check booking form logic:
   
   - Review facility filtering in booking form
   - Verify no JavaScript errors in browser console

**Search Not Working**

**Problem**: Facility search returns no results

**Solutions**:

1. **Clear Filters**: Reset all search criteria
2. **Check Spelling**: Verify search terms are correct
3. **Broaden Search**: Use shorter, more general terms
4. **Status Filter**: Ensure correct status filter is selected

**Performance Issues**

**Problem**: Facility management page loads slowly

**Optimization Steps**:

1. **Database Optimization**:
   
   - Check database size
   - Analyze query performance
   - Consider adding indexes

2. **Data Cleanup**:
   
   - Archive old facilities
   - Remove duplicate entries
   - Optimize facility descriptions

3. **System Resources**:
   
   - Monitor server performance
   - Check available memory
   - Review concurrent user load

Best Practices Summary
----------------------

Planning and Organization
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Facility Naming**
   
   - Use consistent naming conventions
   - Include identifying information
   - Avoid confusing abbreviations

2. **Category Assignment**
   
   - Choose appropriate categories
   - Maintain consistency across similar facilities
   - Regular category review and updates

3. **Information Completeness**
   
   - Provide comprehensive descriptions
   - Include all relevant details
   - Regular information updates

Operational Management
~~~~~~~~~~~~~~~~~~~~~~

1. **Regular Reviews**
   
   - Monthly facility information review
   - Quarterly capacity assessment
   - Annual category and naming review

2. **Status Management**
   
   - Use deactivation for temporary closures
   - Document reasons for status changes
   - Communicate changes to stakeholders

3. **Data Integrity**
   
   - Avoid deletion when possible
   - Maintain historical records
   - Regular data backup verification

User Experience
~~~~~~~~~~~~~~~

1. **Clear Information**
   
   - Write user-friendly descriptions
   - Include practical details
   - Use language appropriate for students

2. **Accurate Locations**
   
   - Provide detailed location information
   - Include landmarks and navigation aids
   - Verify location accuracy regularly

3. **Appropriate Booking Settings**
   
   - Enable booking only for suitable facilities
   - Set realistic capacity limits
   - Consider operational constraints

Security and Access Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Admin Access**
   
   - Limit facility management to appropriate administrators
   - Regular review of admin privileges
   - Audit trail maintenance

2. **Change Management**
   
   - Document significant changes
   - Coordinate with affected departments
   - Communicate changes to users

3. **Data Protection**
   
   - Regular backup of facility data
   - Secure handling of sensitive information
   - Compliance with data protection policies