from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, IntegerField, BooleanField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from models import User, UserRole, IssueType, Priority, BookingStatus

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    student_id = StringField('Student ID (Optional)', validators=[Length(max=20)])
    role = SelectField('Role', choices=[(UserRole.STUDENT.value, 'Student'), (UserRole.ADMIN.value, 'Admin')], 
                      default=UserRole.STUDENT.value)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

    def validate_student_id(self, student_id):
        if student_id.data:
            user = User.query.filter_by(student_id=student_id.data).first()
            if user:
                raise ValidationError('Student ID already registered.')

class IssueForm(FlaskForm):
    title = StringField('Issue Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    issue_type = SelectField('Issue Type', 
                            choices=[(t.value, t.value.title()) for t in IssueType],
                            validators=[DataRequired()])
    priority = SelectField('Priority', 
                          choices=[(p.value, p.value.title()) for p in Priority],
                          default=Priority.MEDIUM.value)
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Submit Issue')

class FeedbackForm(FlaskForm):
    rating = SelectField('Rating', 
                        choices=[('1', '1 Star'), ('2', '2 Stars'), ('3', '3 Stars'), 
                               ('4', '4 Stars'), ('5', '5 Stars')],
                        validators=[DataRequired()])
    comment = TextAreaField('Feedback Comment', validators=[Length(max=500)])
    submit = SubmitField('Submit Feedback')

class BookingForm(FlaskForm):
    facility_id = SelectField('Facility', coerce=int, validators=[DataRequired()])
    booking_date = DateField('Booking Date', validators=[DataRequired()])
    start_hour = SelectField('Start Time', coerce=int, validators=[DataRequired()],
                           choices=[(i, f"{i:02d}:00") for i in range(8, 22)])  # 8 AM to 9 PM
    end_hour = SelectField('End Time', coerce=int, validators=[DataRequired()],
                         choices=[(i, f"{i:02d}:00") for i in range(9, 23)])   # 9 AM to 10 PM
    purpose = StringField('Purpose', validators=[DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Book Facility')
    
    def validate_booking_date(self, booking_date):
        from datetime import date
        if booking_date.data < date.today():
            raise ValidationError('Booking date cannot be in the past.')
    
    def validate_end_hour(self, end_hour):
        if end_hour.data <= self.start_hour.data:
            raise ValidationError('End time must be after start time.')

class BookingManagementForm(FlaskForm):
    status = SelectField('Status', validators=[DataRequired()],
                        choices=[(s.value, s.value.title()) for s in BookingStatus])
    admin_notes = TextAreaField('Admin Notes', validators=[Length(max=500)])
    submit = SubmitField('Update Booking')

class FacilityForm(FlaskForm):
    name = StringField('Facility Name', validators=[DataRequired(), Length(min=2, max=100)])
    category = SelectField('Category', validators=[DataRequired()],
                          choices=[
                              ('Laboratory', 'Laboratory'),
                              ('Academic', 'Academic'),
                              ('Sports', 'Sports'),
                              ('Administrative', 'Administrative'),
                              ('Accommodation', 'Accommodation'),
                              ('Dining', 'Dining'),
                              ('Event', 'Event')
                          ])
    location = StringField('Location', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    is_bookable = BooleanField('Can be Booked')
    is_active = BooleanField('Active', default=True)
    capacity = IntegerField('Capacity', validators=[Optional(), NumberRange(min=1, max=1000)])
    operating_hours = StringField('Operating Hours', validators=[Length(max=100)])
    contact_info = StringField('Contact Info/Landmarks', validators=[Length(max=200)])
    submit = SubmitField('Save Facility')

class FacilityManagementForm(FlaskForm):
    is_active = BooleanField('Active')
    admin_notes = TextAreaField('Admin Notes', validators=[Length(max=500)])
    submit = SubmitField('Update Status')
