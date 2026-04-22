from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Numeric,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app import db

VALID_STATUSES = (
    "Applied",
    "Phone Screen",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
)

_status_check = CheckConstraint(
    "status IN ('Applied', 'Phone Screen', 'Interview', "
    "'Offer', 'Rejected', 'Withdrawn')",
    name="ck_job_entries_status",
)


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Profile fields
    full_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    ic_number = Column(String(50), nullable=True)
    avatar_url = Column(Text, nullable=True)
    avatar_public_id = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    entries = relationship(
        "JobEntry",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class JobEntry(db.Model):
    __tablename__ = "job_entries"
    __table_args__ = (_status_check,)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    application_date = Column(Date, nullable=True)
    location = Column(String(255), nullable=True)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    job_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    file_url = Column(Text, nullable=True)
    file_public_id = Column(Text, nullable=True)
    file_original_name = Column(Text, nullable=True)
    platform = Column(String(100), nullable=True)
    contact_person = Column(String(255), nullable=True)
    work_type = Column(String(50), nullable=True)
    employment_type = Column(String(50), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    user = relationship("User", back_populates="entries")
    attachments = relationship(
        "JobAttachment",
        back_populates="job_entry",
        cascade="all, delete-orphan",
    )


class JobAttachment(db.Model):
    __tablename__ = "job_attachments"

    id = Column(Integer, primary_key=True)
    job_entry_id = Column(Integer, ForeignKey("job_entries.id"), nullable=False)
    file_url = Column(Text, nullable=False)
    file_public_id = Column(Text, nullable=True)
    file_original_name = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    job_entry = relationship("JobEntry", back_populates="attachments")
