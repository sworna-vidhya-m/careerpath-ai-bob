"""SQLAlchemy ORM models for CareerPath AI Bob.

Defines 11 entities covering the full talent-development domain:
BusinessUnit, Employee, Project, ProjectAssignment, Skill, EmployeeSkill,
IndustryStandardSkill, CareerPath, CareerPathSkillRequirement,
LearningResource, LearningEnrollment.
"""

import enum
import logging
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class EmployeeStatus(str, enum.Enum):
    """Lifecycle status of an employee."""

    ACTIVE = "ACTIVE"
    BENCH = "BENCH"
    LEARNING = "LEARNING"


class SkillCategory(str, enum.Enum):
    """Broad category of a skill."""

    TECHNICAL = "TECHNICAL"
    DOMAIN = "DOMAIN"
    SOFT = "SOFT"


class SkillTrend(str, enum.Enum):
    """Market trend direction for an industry-standard skill."""

    RISING = "RISING"
    STABLE = "STABLE"
    DECLINING = "DECLINING"


class ProjectStatus(str, enum.Enum):
    """Lifecycle status of a project."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"


class EnrollmentStatus(str, enum.Enum):
    """Lifecycle status of a learning enrollment."""

    ENROLLED = "ENROLLED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"


class LearningResourceType(str, enum.Enum):
    """Format category of a learning resource."""

    COURSE = "COURSE"
    CERTIFICATION = "CERTIFICATION"
    BOOK = "BOOK"
    WORKSHOP = "WORKSHOP"


# ---------------------------------------------------------------------------
# Shared timestamp mixin
# ---------------------------------------------------------------------------


class TimestampMixin:
    """Adds created_at / updated_at columns to any model."""

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class BusinessUnit(TimestampMixin, Base):
    """An organisational business unit within the company.

    Attributes:
        id: Primary key.
        name: Unique, indexed name of the business unit.
        description: Optional free-text description.
    """

    __tablename__ = "business_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    employees = relationship("Employee", back_populates="business_unit")
    industry_standards = relationship("IndustryStandardSkill", back_populates="business_unit")
    career_paths = relationship("CareerPath", back_populates="business_unit")


class Employee(TimestampMixin, Base):
    """An employee within the organisation.

    Supports a self-referential manager hierarchy via line_manager_id.
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(120), nullable=False)
    band = Column(String(60), nullable=False)
    business_unit_id = Column(Integer, ForeignKey("business_units.id"), nullable=False)
    line_manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    current_status = Column(
        Enum(EmployeeStatus), nullable=False, default=EmployeeStatus.ACTIVE
    )
    hire_date = Column(Date, nullable=False)

    business_unit = relationship("BusinessUnit", back_populates="employees")
    line_manager = relationship("Employee", remote_side="Employee.id", back_populates="reports")
    reports = relationship("Employee", back_populates="line_manager")
    skills = relationship("EmployeeSkill", back_populates="employee")
    assignments = relationship("ProjectAssignment", back_populates="employee")
    enrollments = relationship("LearningEnrollment", back_populates="employee")

    __table_args__ = (Index("ix_employees_bu_status", "business_unit_id", "current_status"),)


class Project(TimestampMixin, Base):
    """A client-facing or internal project.

    Attributes:
        name: Project name.
        client: Client or sponsor name.
        status: Current project lifecycle status.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    client = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(Enum(ProjectStatus), nullable=False)

    assignments = relationship("ProjectAssignment", back_populates="project")


class ProjectAssignment(TimestampMixin, Base):
    """Assignment of an employee to a project with a given role and allocation."""

    __tablename__ = "project_assignments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    role_on_project = Column(String(120), nullable=False)
    allocation_pct = Column(Integer, nullable=False, default=100)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    employee = relationship("Employee", back_populates="assignments")
    project = relationship("Project", back_populates="assignments")

    __table_args__ = (
        CheckConstraint("allocation_pct >= 0 AND allocation_pct <= 100", name="ck_alloc_pct"),
    )


class Skill(TimestampMixin, Base):
    """A skill tracked by the platform.

    Attributes:
        name: Unique skill name.
        category: TECHNICAL, DOMAIN, or SOFT.
        is_emerging: True for emerging/high-demand skills.
    """

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False, index=True)
    category = Column(Enum(SkillCategory), nullable=False)
    is_emerging = Column(Boolean, nullable=False, default=False)

    employee_skills = relationship("EmployeeSkill", back_populates="skill")
    industry_standards = relationship("IndustryStandardSkill", back_populates="skill")
    career_path_requirements = relationship("CareerPathSkillRequirement", back_populates="skill")
    learning_resources = relationship("LearningResource", back_populates="skill")


class EmployeeSkill(TimestampMixin, Base):
    """Junction table recording an employee's proficiency in a skill."""

    __tablename__ = "employee_skills"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency = Column(Integer, nullable=False)
    last_used_at = Column(Date, nullable=True)
    certified = Column(Boolean, nullable=False, default=False)

    employee = relationship("Employee", back_populates="skills")
    skill = relationship("Skill", back_populates="employee_skills")

    __table_args__ = (
        UniqueConstraint("employee_id", "skill_id", name="uq_employee_skill"),
        CheckConstraint("proficiency >= 1 AND proficiency <= 5", name="ck_proficiency"),
    )


class IndustryStandardSkill(TimestampMixin, Base):
    """Records the importance and trend of a skill for a given business unit."""

    __tablename__ = "industry_standard_skills"

    id = Column(Integer, primary_key=True, index=True)
    business_unit_id = Column(Integer, ForeignKey("business_units.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    importance = Column(Integer, nullable=False)
    trend = Column(Enum(SkillTrend), nullable=False)

    business_unit = relationship("BusinessUnit", back_populates="industry_standards")
    skill = relationship("Skill", back_populates="industry_standards")

    __table_args__ = (
        UniqueConstraint("business_unit_id", "skill_id", name="uq_bu_skill"),
        CheckConstraint("importance >= 1 AND importance <= 5", name="ck_importance"),
    )


class CareerPath(TimestampMixin, Base):
    """Defines a progression path from one role to another within a business unit."""

    __tablename__ = "career_paths"

    id = Column(Integer, primary_key=True, index=True)
    business_unit_id = Column(Integer, ForeignKey("business_units.id"), nullable=False)
    from_role = Column(String(120), nullable=False)
    to_role = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)

    business_unit = relationship("BusinessUnit", back_populates="career_paths")
    skill_requirements = relationship("CareerPathSkillRequirement", back_populates="career_path")


class CareerPathSkillRequirement(TimestampMixin, Base):
    """Minimum skill proficiency required to traverse a career path."""

    __tablename__ = "career_path_skill_requirements"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    min_proficiency = Column(Integer, nullable=False)

    career_path = relationship("CareerPath", back_populates="skill_requirements")
    skill = relationship("Skill", back_populates="career_path_requirements")

    __table_args__ = (
        UniqueConstraint("career_path_id", "skill_id", name="uq_path_skill"),
        CheckConstraint(
            "min_proficiency >= 1 AND min_proficiency <= 5", name="ck_min_proficiency"
        ),
    )


class LearningResource(TimestampMixin, Base):
    """A learning resource (course, certification, book, workshop) for a skill."""

    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(Enum(LearningResourceType), nullable=False)
    url = Column(String(500), nullable=True)
    duration_hours = Column(Integer, nullable=False)

    skill = relationship("Skill", back_populates="learning_resources")
    enrollments = relationship("LearningEnrollment", back_populates="resource")


class LearningEnrollment(TimestampMixin, Base):
    """Records an employee's enrollment in a learning resource."""

    __tablename__ = "learning_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("learning_resources.id"), nullable=False)
    enrolled_at = Column(DateTime, nullable=False, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    status = Column(Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.ENROLLED)

    employee = relationship("Employee", back_populates="enrollments")
    resource = relationship("LearningResource", back_populates="enrollments")
