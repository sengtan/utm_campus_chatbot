from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User, UserRole, IssueType, Priority

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
