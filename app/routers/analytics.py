"""Analytics router — intelligent endpoints reserved for IBM Bob.

This module is intentionally a stub. The following endpoints will be
implemented during the hackathon by IBM Bob:

  - GET /analytics/skill-gap/{employee_id}
  - GET /analytics/career-recommendations/{employee_id}
  - POST /analytics/trigger-bench-learning
  - GET /analytics/industry-trends/{business_unit_id}
  - GET /analytics/skill-heatmap

Until then, this router exposes a single health probe so the route is
registered and the smoke test can verify wiring.
"""

import logging
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import NotFoundError, raise_http_from_app_exception
from app.models import (
    CareerPath,
    CareerPathSkillRequirement,
    Employee,
    EmployeeSkill,
    LearningResource,
    Skill,
)
from app.schemas import (
    RecommendedResourceRead,
    SkillGapAnalysisRead,
    SkillGapItem,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/health")
def analytics_health() -> dict[str, str]:
    """Health probe confirming the analytics router is mounted."""
    return {"status": "ok", "module": "analytics", "implemented": "pending-bob"}


@router.get("/skill-gap/{employee_id}", response_model=SkillGapAnalysisRead)
def get_skill_gap_analysis(
    employee_id: int, db: Session = Depends(get_db)
) -> SkillGapAnalysisRead:
    """Analyze skill gaps for an employee based on career path requirements.
    
    Args:
        employee_id: Employee primary key
        db: Database session
        
    Returns:
        Skill gap analysis with recommendations
        
    Raises:
        HTTPException: 404 if employee not found
    """
    try:
        # Step 1: Fetch employee
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise NotFoundError(
                f"Employee with id {employee_id} not found",
                {"employee_id": employee_id}
            )
        
        # Step 2: Build proficiency map for employee
        employee_skills = (
            db.query(EmployeeSkill)
            .filter(EmployeeSkill.employee_id == employee_id)
            .all()
        )
        proficiency_map: Dict[int, int] = {
            es.skill_id: es.proficiency for es in employee_skills
        }
        
        # Step 3: Find career paths from employee's current role
        career_paths = (
            db.query(CareerPath)
            .filter(
                CareerPath.from_role == employee.role,
                CareerPath.business_unit_id == employee.business_unit_id
            )
            .all()
        )
        
        # Step 4-7: Analyze skill gaps
        skill_gaps_dict: Dict[int, SkillGapItem] = {}
        
        for career_path in career_paths:
            requirements = (
                db.query(CareerPathSkillRequirement)
                .filter(
                    CareerPathSkillRequirement.career_path_id == career_path.id
                )
                .all()
            )
            
            for req in requirements:
                current_prof = proficiency_map.get(req.skill_id, 0)
                gap = req.min_proficiency - current_prof
                
                if gap > 0:
                    # Only process if not already in dict or if gap is larger
                    if req.skill_id not in skill_gaps_dict:
                        skill = (
                            db.query(Skill)
                            .filter(Skill.id == req.skill_id)
                            .first()
                        )
                        
                        # Fetch 1-3 learning resources for this skill
                        resources = (
                            db.query(LearningResource)
                            .filter(LearningResource.skill_id == req.skill_id)
                            .order_by(LearningResource.duration_hours)
                            .limit(3)
                            .all()
                        )
                        
                        recommended = [
                            RecommendedResourceRead(
                                resource_id=r.id,
                                title=r.title,
                                type=r.type,
                                duration_hours=r.duration_hours
                            )
                            for r in resources
                        ]
                        
                        # Mark as critical if gap >= 3 or skill is emerging
                        is_critical = gap >= 3 or skill.is_emerging
                        
                        skill_gaps_dict[req.skill_id] = SkillGapItem(
                            skill_id=req.skill_id,
                            skill_name=skill.name,
                            current_proficiency=current_prof,
                            required_proficiency=req.min_proficiency,
                            gap=gap,
                            is_critical=is_critical,
                            recommended_resources=recommended
                        )
                    else:
                        # Update if this requirement is higher
                        existing = skill_gaps_dict[req.skill_id]
                        if req.min_proficiency > existing.required_proficiency:
                            new_gap = req.min_proficiency - current_prof
                            skill = (
                                db.query(Skill)
                                .filter(Skill.id == req.skill_id)
                                .first()
                            )
                            is_critical = new_gap >= 3 or skill.is_emerging
                            existing.required_proficiency = req.min_proficiency
                            existing.gap = new_gap
                            existing.is_critical = is_critical
        
        # Step 8: Build response
        skill_gaps = list(skill_gaps_dict.values())
        critical_gaps = sum(1 for gap in skill_gaps if gap.is_critical)
        
        logger.info(
            "Skill gap analysis completed for employee_id=%d, gaps=%d",
            employee_id, len(skill_gaps)
        )
        
        return SkillGapAnalysisRead(
            employee_id=employee.id,
            employee_name=employee.name,
            current_role=employee.role,
            business_unit_id=employee.business_unit_id,
            skill_gaps=skill_gaps,
            total_gaps=len(skill_gaps),
            critical_gaps=critical_gaps
        )
        
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)
