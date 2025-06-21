from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import Enum
import enum

class UserRole(enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"

class IssueStatus(enum.Enum):
    REPORTED = "reported"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class IssueType(enum.Enum):
    ELECTRICAL = "electrical"
    HYGIENE = "hygiene"
    STRUCTURAL = "structural"
    EQUIPMENT = "equipment"
    SECURITY = "security"
    OTHER = "other"

class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    full_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Facility(db.Model):
    __tablename__ = 'facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_bookable = db.Column(db.Boolean, default=False)
    capacity = db.Column(db.Integer)
    operating_hours = db.Column(db.String(100))
    contact_info = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Issue(db.Model):
    __tablename__ = 'issues'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    issue_type = db.Column(Enum(IssueType), nullable=False)
    priority = db.Column(Enum(Priority), default=Priority.MEDIUM)
    status = db.Column(Enum(IssueStatus), default=IssueStatus.REPORTED)
    location = db.Column(db.String(200), nullable=False)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Additional fields
    admin_notes = db.Column(db.Text)
    feedback_rating = db.Column(db.Integer)  # 1-5 rating
    feedback_comment = db.Column(db.Text)
    
    # Relationships
    reporter = db.relationship('User', foreign_keys=[user_id])
    assignee = db.relationship('User', foreign_keys=[assigned_to])
    facility = db.relationship('Facility')

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    messages = db.relationship('ChatMessage', cascade='all, delete-orphan')

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, nullable=False)  # True for user, False for bot
    intent = db.Column(db.String(50))  # Detected intent
    entities = db.Column(db.JSON)  # Extracted entities
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    session = db.relationship('ChatSession')

class FacilityBooking(db.Model):
    __tablename__ = 'facility_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    facility = db.relationship('Facility')
    user = db.relationship('User')