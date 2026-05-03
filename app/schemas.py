"""Pydantic v2 schemas for request validation and response serialisation.

Each entity has four schema classes:
  XBase    — shared fields
  XCreate  — fields required on POST
  XUpdate  — all fields optional for partial PUT
  XRead    — full response including id and timestamps
"""

import logging
from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import (
    EmployeeStatus,
    EnrollmentStatus,
    LearningResourceType,
    ProjectStatus,
    SkillCategory,
    SkillTrend,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# BusinessUnit
# ---------------------------------------------------------------------------


class BusinessUnitBase(BaseModel):
    """Shared fields for BusinessUnit."""

    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = None


class BusinessUnitCreate(BusinessUnitBase):
    """Fields required to create a BusinessUnit."""


class BusinessUnitUpdate(BaseModel):
    """All fields optional for partial update of BusinessUnit."""

    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = None


class BusinessUnitRead(BusinessUnitBase):
    """Full BusinessUnit response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Employee
# ---------------------------------------------------------------------------


class EmployeeBase(BaseModel):
    """Shared fields for Employee."""

    name: str = Field(..., min_length=1, max_length=120)
    email: str = Field(..., max_length=255)
    role: str = Field(..., min_length=1, max_length=120)
    band: str = Field(..., min_length=1, max_length=60)
    business_unit_id: int
    line_manager_id: Optional[int] = None
    current_status: EmployeeStatus = EmployeeStatus.ACTIVE
    hire_date: date


class EmployeeCreate(EmployeeBase):
    """Fields required to create an Employee."""


class EmployeeUpdate(BaseModel):
    """All fields optional for partial update of Employee."""

    name: Optional[str] = Field(None, min_length=1, max_length=120)
    email: Optional[str] = Field(None, max_length=255)
    role: Optional[str] = Field(None, min_length=1, max_length=120)
    band: Optional[str] = Field(None, min_length=1, max_length=60)
    business_unit_id: Optional[int] = None
    line_manager_id: Optional[int] = None
    current_status: Optional[EmployeeStatus] = None
    hire_date: Optional[date] = None


class EmployeeRead(EmployeeBase):
    """Full Employee response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------


class ProjectBase(BaseModel):
    """Shared fields for Project."""

    name: str = Field(..., min_length=1, max_length=200)
    client: str = Field(..., min_length=1, max_length=200)
    start_date: date
    end_date: Optional[date] = None
    status: ProjectStatus


class ProjectCreate(ProjectBase):
    """Fields required to create a Project."""


class ProjectUpdate(BaseModel):
    """All fields optional for partial update of Project."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    client: Optional[str] = Field(None, min_length=1, max_length=200)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ProjectStatus] = None


class ProjectRead(ProjectBase):
    """Full Project response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# ProjectAssignment
# ---------------------------------------------------------------------------


class ProjectAssignmentBase(BaseModel):
    """Shared fields for ProjectAssignment."""

    employee_id: int
    project_id: int
    role_on_project: str = Field(..., min_length=1, max_length=120)
    allocation_pct: int = Field(default=100, ge=0, le=100)
    start_date: date
    end_date: Optional[date] = None


class ProjectAssignmentCreate(ProjectAssignmentBase):
    """Fields required to create a ProjectAssignment."""


class ProjectAssignmentUpdate(BaseModel):
    """All fields optional for partial update of ProjectAssignment."""

    employee_id: Optional[int] = None
    project_id: Optional[int] = None
    role_on_project: Optional[str] = Field(None, min_length=1, max_length=120)
    allocation_pct: Optional[int] = Field(None, ge=0, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectAssignmentRead(ProjectAssignmentBase):
    """Full ProjectAssignment response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Skill
# ---------------------------------------------------------------------------


class SkillBase(BaseModel):
    """Shared fields for Skill."""

    name: str = Field(..., min_length=1, max_length=120)
    category: SkillCategory
    is_emerging: bool = False


class SkillCreate(SkillBase):
    """Fields required to create a Skill."""


class SkillUpdate(BaseModel):
    """All fields optional for partial update of Skill."""

    name: Optional[str] = Field(None, min_length=1, max_length=120)
    category: Optional[SkillCategory] = None
    is_emerging: Optional[bool] = None


class SkillRead(SkillBase):
    """Full Skill response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# EmployeeSkill
# ---------------------------------------------------------------------------


class EmployeeSkillBase(BaseModel):
    """Shared fields for EmployeeSkill."""

    employee_id: int
    skill_id: int
    proficiency: int = Field(..., ge=1, le=5)
    last_used_at: Optional[date] = None
    certified: bool = False


class EmployeeSkillCreate(EmployeeSkillBase):
    """Fields required to create an EmployeeSkill."""


class EmployeeSkillUpdate(BaseModel):
    """All fields optional for partial update of EmployeeSkill."""

    employee_id: Optional[int] = None
    skill_id: Optional[int] = None
    proficiency: Optional[int] = Field(None, ge=1, le=5)
    last_used_at: Optional[date] = None
    certified: Optional[bool] = None


class EmployeeSkillRead(EmployeeSkillBase):
    """Full EmployeeSkill response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# IndustryStandardSkill
# ---------------------------------------------------------------------------


class IndustryStandardSkillBase(BaseModel):
    """Shared fields for IndustryStandardSkill."""

    business_unit_id: int
    skill_id: int
    importance: int = Field(..., ge=1, le=5)
    trend: SkillTrend


class IndustryStandardSkillCreate(IndustryStandardSkillBase):
    """Fields required to create an IndustryStandardSkill."""


class IndustryStandardSkillUpdate(BaseModel):
    """All fields optional for partial update of IndustryStandardSkill."""

    business_unit_id: Optional[int] = None
    skill_id: Optional[int] = None
    importance: Optional[int] = Field(None, ge=1, le=5)
    trend: Optional[SkillTrend] = None


class IndustryStandardSkillRead(IndustryStandardSkillBase):
    """Full IndustryStandardSkill response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# CareerPath
# ---------------------------------------------------------------------------


class CareerPathBase(BaseModel):
    """Shared fields for CareerPath."""

    business_unit_id: int
    from_role: str = Field(..., min_length=1, max_length=120)
    to_role: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = None


class CareerPathCreate(CareerPathBase):
    """Fields required to create a CareerPath."""


class CareerPathUpdate(BaseModel):
    """All fields optional for partial update of CareerPath."""

    business_unit_id: Optional[int] = None
    from_role: Optional[str] = Field(None, min_length=1, max_length=120)
    to_role: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = None


class CareerPathRead(CareerPathBase):
    """Full CareerPath response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# CareerPathSkillRequirement
# ---------------------------------------------------------------------------


class CareerPathSkillRequirementBase(BaseModel):
    """Shared fields for CareerPathSkillRequirement."""

    career_path_id: int
    skill_id: int
    min_proficiency: int = Field(..., ge=1, le=5)


class CareerPathSkillRequirementCreate(CareerPathSkillRequirementBase):
    """Fields required to create a CareerPathSkillRequirement."""


class CareerPathSkillRequirementUpdate(BaseModel):
    """All fields optional for partial update of CareerPathSkillRequirement."""

    career_path_id: Optional[int] = None
    skill_id: Optional[int] = None
    min_proficiency: Optional[int] = Field(None, ge=1, le=5)


class CareerPathSkillRequirementRead(CareerPathSkillRequirementBase):
    """Full CareerPathSkillRequirement response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# LearningResource
# ---------------------------------------------------------------------------


class LearningResourceBase(BaseModel):
    """Shared fields for LearningResource."""

    skill_id: int
    title: str = Field(..., min_length=1, max_length=255)
    type: LearningResourceType
    url: Optional[str] = Field(None, max_length=500)
    duration_hours: int = Field(..., gt=0)


class LearningResourceCreate(LearningResourceBase):
    """Fields required to create a LearningResource."""


class LearningResourceUpdate(BaseModel):
    """All fields optional for partial update of LearningResource."""

    skill_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[LearningResourceType] = None
    url: Optional[str] = Field(None, max_length=500)
    duration_hours: Optional[int] = Field(None, gt=0)


class LearningResourceRead(LearningResourceBase):
    """Full LearningResource response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# LearningEnrollment
# ---------------------------------------------------------------------------


class LearningEnrollmentBase(BaseModel):
    """Shared fields for LearningEnrollment."""

    employee_id: int
    resource_id: int
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    status: EnrollmentStatus = EnrollmentStatus.ENROLLED


class LearningEnrollmentCreate(LearningEnrollmentBase):
    """Fields required to create a LearningEnrollment."""


class LearningEnrollmentUpdate(BaseModel):
    """All fields optional for partial update of LearningEnrollment."""

    employee_id: Optional[int] = None
    resource_id: Optional[int] = None
    enrolled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Optional[EnrollmentStatus] = None


class LearningEnrollmentRead(LearningEnrollmentBase):
    """Full LearningEnrollment response including id and timestamps."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime



# ---------------------------------------------------------------------------
# Analytics — Skill Gap Analysis
# ---------------------------------------------------------------------------


class RecommendedResourceRead(BaseModel):
    """Minimal learning resource info for recommendations."""
    model_config = ConfigDict(from_attributes=True)
    
    resource_id: int
    title: str
    type: LearningResourceType
    duration_hours: int


class SkillGapItem(BaseModel):
    """Individual skill gap with recommendation."""
    
    skill_id: int
    skill_name: str
    current_proficiency: int  # 0-5, 0 means not possessed
    required_proficiency: int  # 1-5
    gap: int
    is_critical: bool
    recommended_resources: List[RecommendedResourceRead]


class SkillGapAnalysisRead(BaseModel):
    """Complete skill gap analysis for an employee."""
    
    employee_id: int
    employee_name: str
    current_role: str
    business_unit_id: int
    skill_gaps: List[SkillGapItem]
    total_gaps: int
    critical_gaps: int


# ---------------------------------------------------------------------------
# Analytics — Industry Trends
# ---------------------------------------------------------------------------


class TrendingSkillItem(BaseModel):
    """Industry trend data for a single skill."""
    
    skill_id: int
    skill_name: str
    category: SkillCategory
    is_emerging: bool
    importance: int  # 1-5
    trend: SkillTrend
    employee_count: int
    avg_proficiency: float  # 0.0-5.0


class IndustryTrendsRead(BaseModel):
    """Industry skill trends for a business unit."""
    
    business_unit_id: int
    business_unit_name: str
    trending_skills: List[TrendingSkillItem]
    total_skills: int
    rising_count: int
    stable_count: int
    declining_count: int


# ---------------------------------------------------------------------------
# Analytics — Skill Heatmap
# ---------------------------------------------------------------------------


class BusinessUnitSkillBreakdown(BaseModel):
    """Skill metrics for a specific business unit."""
    
    business_unit_id: int
    business_unit_name: str
    employee_count: int
    avg_proficiency: float


class SkillHeatmapItem(BaseModel):
    """Heatmap data for a single skill across the organization."""
    
    skill_id: int
    skill_name: str
    category: SkillCategory
    is_emerging: bool
    total_employees: int
    proficiency_distribution: Dict[str, int]  # "1": count, "2": count, etc.
    avg_proficiency: float
    certified_count: int
    business_units: List[BusinessUnitSkillBreakdown]


class SkillHeatmapFilters(BaseModel):
    """Applied filters for the heatmap query."""
    
    business_unit_id: Optional[int] = None
    skill_category: Optional[SkillCategory] = None
    min_importance: Optional[int] = None


class SkillHeatmapRead(BaseModel):
    """Complete skill heatmap across organization or filtered subset."""
    
    filters: SkillHeatmapFilters
    heatmap_data: List[SkillHeatmapItem]
    total_skills: int
    total_employees_analyzed: int


# ---------------------------------------------------------------------------
# Analytics — Career Recommendations
# ---------------------------------------------------------------------------


class MissingSkillItem(BaseModel):
    """Skill gap detail for career recommendation."""
    
    skill_id: int
    skill_name: str
    required_proficiency: int
    current_proficiency: int


class CareerRecommendationItem(BaseModel):
    """Single career path recommendation with readiness assessment."""
    
    career_path_id: int
    to_role: str
    to_band: Optional[str]  # inferred from employees in that role
    business_unit_id: int
    business_unit_name: str
    match_score: float  # 0.0-1.0
    readiness: str  # HIGH, MEDIUM, LOW
    required_skills: int
    possessed_skills: int
    skill_gaps: int
    missing_skills: List[MissingSkillItem]
    estimated_learning_hours: int


class CareerRecommendationsRead(BaseModel):
    """Career path recommendations for an employee."""
    
    employee_id: int
    employee_name: str
    current_role: str
    current_band: str
    business_unit_id: int
    recommendations: List[CareerRecommendationItem]
    total_recommendations: int


# ---------------------------------------------------------------------------
# Analytics — Bench Learning Trigger
# ---------------------------------------------------------------------------


class BenchLearningTriggerRequest(BaseModel):
    """Request to trigger learning enrollments for bench employees."""
    
    business_unit_id: Optional[int] = None
    skill_ids: Optional[List[int]] = None
    max_enrollments_per_employee: int = Field(default=3, ge=1, le=10)
    dry_run: bool = False


class BenchLearningFilters(BaseModel):
    """Filters applied to bench learning trigger."""
    
    business_unit_id: Optional[int] = None
    skill_ids: Optional[List[int]] = None


class BenchEnrollmentItem(BaseModel):
    """Single enrollment created for a bench employee."""
    
    employee_id: int
    employee_name: str
    resource_id: int
    resource_title: str
    skill_id: int
    skill_name: str
    enrollment_id: Optional[int]  # null if dry_run=true
    reason: str


class BenchLearningSummary(BaseModel):
    """Summary statistics for bench learning trigger."""
    
    total_hours_allocated: int
    skills_targeted: int
    avg_enrollments_per_employee: float


class BenchLearningTriggerRead(BaseModel):
    """Result of triggering bench learning enrollments."""
    
    triggered_at: datetime
    dry_run: bool
    filters: BenchLearningFilters
    bench_employees_found: int
    enrollments_created: int
    enrollments: List[BenchEnrollmentItem]
    summary: BenchLearningSummary
