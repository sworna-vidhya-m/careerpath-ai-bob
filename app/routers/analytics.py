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
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import NotFoundError, raise_http_from_app_exception
from app.models import (
    BusinessUnit,
    CareerPath,
    CareerPathSkillRequirement,
    Employee,
    EmployeeSkill,
    IndustryStandardSkill,
    LearningResource,
    Skill,
    SkillCategory,
    SkillTrend,
)
from app.schemas import (
    BusinessUnitSkillBreakdown,
    CareerRecommendationItem,
    CareerRecommendationsRead,
    IndustryTrendsRead,
    MissingSkillItem,
    RecommendedResourceRead,
    SkillGapAnalysisRead,
    SkillGapItem,
    SkillHeatmapFilters,
    SkillHeatmapItem,
    SkillHeatmapRead,
    TrendingSkillItem,
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


@router.get(
    "/industry-trends/{business_unit_id}",
    response_model=IndustryTrendsRead
)
def get_industry_trends(
    business_unit_id: int,
    trend_filter: Optional[SkillTrend] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
) -> IndustryTrendsRead:
    """Get industry skill trends for a business unit.
    
    Args:
        business_unit_id: Business unit primary key
        trend_filter: Optional filter by RISING, STABLE, or DECLINING
        limit: Max skills to return (default 20, max 100)
        db: Database session
        
    Returns:
        Industry trends with skill statistics
        
    Raises:
        HTTPException: 404 if business unit not found
    """
    try:
        # Step 1: Fetch business unit
        business_unit = (
            db.query(BusinessUnit)
            .filter(BusinessUnit.id == business_unit_id)
            .first()
        )
        if not business_unit:
            raise NotFoundError(
                f"BusinessUnit with id {business_unit_id} not found",
                {"business_unit_id": business_unit_id}
            )
        
        # Step 2: Query IndustryStandardSkill for this business unit
        query = (
            db.query(IndustryStandardSkill)
            .filter(IndustryStandardSkill.business_unit_id == business_unit_id)
        )
        
        # Step 3: Apply optional trend_filter
        if trend_filter:
            query = query.filter(IndustryStandardSkill.trend == trend_filter)
        
        industry_standards = query.all()
        
        # Step 4-6: Build trending skills with employee stats
        trending_skills: List[TrendingSkillItem] = []
        
        for ind_std in industry_standards:
            # Step 4: Join with Skill to get details
            skill = db.query(Skill).filter(Skill.id == ind_std.skill_id).first()
            if not skill:
                continue
            
            # Step 5: Count employees in this BU who possess this skill
            employee_count = (
                db.query(func.count(EmployeeSkill.id))
                .join(Employee, Employee.id == EmployeeSkill.employee_id)
                .filter(
                    Employee.business_unit_id == business_unit_id,
                    EmployeeSkill.skill_id == ind_std.skill_id
                )
                .scalar()
            ) or 0
            
            # Step 6: Calculate average proficiency for employees in this BU
            avg_proficiency_result = (
                db.query(func.avg(EmployeeSkill.proficiency))
                .join(Employee, Employee.id == EmployeeSkill.employee_id)
                .filter(
                    Employee.business_unit_id == business_unit_id,
                    EmployeeSkill.skill_id == ind_std.skill_id
                )
                .scalar()
            )
            avg_proficiency = (
                float(avg_proficiency_result) if avg_proficiency_result else 0.0
            )
            
            trending_skills.append(
                TrendingSkillItem(
                    skill_id=skill.id,
                    skill_name=skill.name,
                    category=skill.category,
                    is_emerging=skill.is_emerging,
                    importance=ind_std.importance,
                    trend=ind_std.trend,
                    employee_count=employee_count,
                    avg_proficiency=round(avg_proficiency, 1)
                )
            )
        
        # Step 7: Sort by importance DESC, then by trend (RISING first)
        trend_order = {SkillTrend.RISING: 0, SkillTrend.STABLE: 1,
                       SkillTrend.DECLINING: 2}
        trending_skills.sort(
            key=lambda x: (-x.importance, trend_order.get(x.trend, 3))
        )
        trending_skills = trending_skills[:limit]
        
        # Step 8: Aggregate trend counts
        rising_count = sum(
            1 for std in industry_standards if std.trend == SkillTrend.RISING
        )
        stable_count = sum(
            1 for std in industry_standards if std.trend == SkillTrend.STABLE
        )
        declining_count = sum(
            1 for std in industry_standards if std.trend == SkillTrend.DECLINING
        )
        
        logger.info(
            "Industry trends retrieved for business_unit_id=%d, skills=%d",
            business_unit_id, len(trending_skills)
        )
        
        return IndustryTrendsRead(
            business_unit_id=business_unit.id,
            business_unit_name=business_unit.name,
            trending_skills=trending_skills,
            total_skills=len(industry_standards),
            rising_count=rising_count,
            stable_count=stable_count,
            declining_count=declining_count
        )
        
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.get("/skill-heatmap", response_model=SkillHeatmapRead)
def get_skill_heatmap(
    business_unit_id: Optional[int] = Query(None),
    skill_category: Optional[SkillCategory] = Query(None),
    min_importance: Optional[int] = Query(None, ge=1, le=5),
    db: Session = Depends(get_db)
) -> SkillHeatmapRead:
    """Get skill heatmap across organization or filtered subset.
    
    Args:
        business_unit_id: Optional filter by business unit
        skill_category: Optional filter by TECHNICAL, DOMAIN, or SOFT
        min_importance: Optional minimum importance threshold (1-5)
        db: Database session
        
    Returns:
        Skill heatmap with proficiency distribution and business unit breakdown
    """
    try:
        # Step 1: Build base query for Skills
        skills_query = db.query(Skill)
        
        # Apply skill_category filter if provided
        if skill_category:
            skills_query = skills_query.filter(Skill.category == skill_category)
        
        # Step 2: If min_importance provided, join with IndustryStandardSkill
        skill_ids_with_importance = None
        if min_importance is not None:
            importance_subquery = (
                db.query(IndustryStandardSkill.skill_id)
                .filter(IndustryStandardSkill.importance >= min_importance)
                .distinct()
            )
            skill_ids_with_importance = [row[0] for row in importance_subquery.all()]
            if skill_ids_with_importance:
                skills_query = skills_query.filter(
                    Skill.id.in_(skill_ids_with_importance)
                )
            else:
                # No skills meet importance threshold
                return SkillHeatmapRead(
                    filters=SkillHeatmapFilters(
                        business_unit_id=business_unit_id,
                        skill_category=skill_category,
                        min_importance=min_importance
                    ),
                    heatmap_data=[],
                    total_skills=0,
                    total_employees_analyzed=0
                )
        
        skills = skills_query.all()
        
        # Step 3-6: For each skill, calculate metrics
        heatmap_items: List[SkillHeatmapItem] = []
        total_employees_set = set()
        
        for skill in skills:
            # Query EmployeeSkill records for this skill
            emp_skill_query = (
                db.query(EmployeeSkill, Employee)
                .join(Employee, Employee.id == EmployeeSkill.employee_id)
                .filter(EmployeeSkill.skill_id == skill.id)
            )
            
            # Step 4: Apply business_unit_id filter if provided
            if business_unit_id is not None:
                emp_skill_query = emp_skill_query.filter(
                    Employee.business_unit_id == business_unit_id
                )
            
            emp_skills = emp_skill_query.all()
            
            if not emp_skills:
                continue  # Skip skills with no employees
            
            # Step 5: Calculate metrics
            total_employees = len(emp_skills)
            proficiency_dist: Dict[str, int] = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
            total_prof = 0
            certified_count = 0
            
            for emp_skill, employee in emp_skills:
                total_employees_set.add(employee.id)
                prof_str = str(emp_skill.proficiency)
                proficiency_dist[prof_str] = proficiency_dist.get(prof_str, 0) + 1
                total_prof += emp_skill.proficiency
                if emp_skill.certified:
                    certified_count += 1
            
            avg_proficiency = round(total_prof / total_employees, 1)
            
            # Step 6: Group by business unit for breakdown
            bu_breakdown_dict: Dict[int, Dict] = {}
            for emp_skill, employee in emp_skills:
                bu_id = employee.business_unit_id
                if bu_id not in bu_breakdown_dict:
                    bu_breakdown_dict[bu_id] = {
                        "count": 0,
                        "total_prof": 0,
                        "bu_name": None
                    }
                bu_breakdown_dict[bu_id]["count"] += 1
                bu_breakdown_dict[bu_id]["total_prof"] += emp_skill.proficiency
            
            # Fetch business unit names and build breakdown list
            business_units: List[BusinessUnitSkillBreakdown] = []
            for bu_id, data in bu_breakdown_dict.items():
                bu = db.query(BusinessUnit).filter(BusinessUnit.id == bu_id).first()
                if bu:
                    business_units.append(
                        BusinessUnitSkillBreakdown(
                            business_unit_id=bu.id,
                            business_unit_name=bu.name,
                            employee_count=data["count"],
                            avg_proficiency=round(
                                data["total_prof"] / data["count"], 1
                            )
                        )
                    )
            
            heatmap_items.append(
                SkillHeatmapItem(
                    skill_id=skill.id,
                    skill_name=skill.name,
                    category=skill.category,
                    is_emerging=skill.is_emerging,
                    total_employees=total_employees,
                    proficiency_distribution=proficiency_dist,
                    avg_proficiency=avg_proficiency,
                    certified_count=certified_count,
                    business_units=business_units
                )
            )
        
        # Step 7: Sort by total_employees DESC, then by avg_proficiency DESC
        heatmap_items.sort(
            key=lambda x: (-x.total_employees, -x.avg_proficiency)
        )
        
        logger.info(
            "Skill heatmap retrieved, skills=%d, employees=%d",
            len(heatmap_items), len(total_employees_set)
        )
        
        return SkillHeatmapRead(
            filters=SkillHeatmapFilters(
                business_unit_id=business_unit_id,
                skill_category=skill_category,
                min_importance=min_importance
            ),
            heatmap_data=heatmap_items,
            total_skills=len(heatmap_items),
            total_employees_analyzed=len(total_employees_set)
        )
        
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)



@router.get(
    "/career-recommendations/{employee_id}",
    response_model=CareerRecommendationsRead
)
def get_career_recommendations(
    employee_id: int,
    include_cross_bu: bool = Query(False),
    max_recommendations: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
) -> CareerRecommendationsRead:
    """Get career path recommendations for an employee.
    
    Args:
        employee_id: Employee primary key
        include_cross_bu: Include career paths from other business units
        max_recommendations: Maximum recommendations to return (default 5, max 20)
        db: Database session
        
    Returns:
        Career recommendations with readiness assessment
        
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
        
        # Step 3: Query CareerPath where from_role matches employee's role
        career_paths_query = (
            db.query(CareerPath)
            .filter(CareerPath.from_role == employee.role)
        )
        
        # Filter by business unit if include_cross_bu is False
        if not include_cross_bu:
            career_paths_query = career_paths_query.filter(
                CareerPath.business_unit_id == employee.business_unit_id
            )
        
        career_paths = career_paths_query.all()
        
        # Step 4: For each career path, calculate metrics
        recommendations: List[CareerRecommendationItem] = []
        
        for career_path in career_paths:
            # Fetch all skill requirements for this path
            requirements = (
                db.query(CareerPathSkillRequirement)
                .filter(
                    CareerPathSkillRequirement.career_path_id == career_path.id
                )
                .all()
            )
            
            if not requirements:
                continue  # Skip paths with no requirements
            
            required_skills = len(requirements)
            possessed_skills = 0
            missing_skills_list: List[MissingSkillItem] = []
            estimated_hours = 0
            
            # Compare requirements with employee's skills
            for req in requirements:
                current_prof = proficiency_map.get(req.skill_id, 0)
                
                if current_prof >= req.min_proficiency:
                    possessed_skills += 1
                else:
                    # This is a missing skill
                    skill = (
                        db.query(Skill)
                        .filter(Skill.id == req.skill_id)
                        .first()
                    )
                    
                    if skill:
                        missing_skills_list.append(
                            MissingSkillItem(
                                skill_id=req.skill_id,
                                skill_name=skill.name,
                                required_proficiency=req.min_proficiency,
                                current_proficiency=current_prof
                            )
                        )
                        
                        # Sum learning hours for this skill
                        resources = (
                            db.query(LearningResource)
                            .filter(LearningResource.skill_id == req.skill_id)
                            .all()
                        )
                        if resources:
                            # Take minimum duration as estimate
                            estimated_hours += min(
                                r.duration_hours for r in resources
                            )
            
            # Calculate match_score
            match_score = (
                possessed_skills / required_skills if required_skills > 0 else 0.0
            )
            
            # Determine readiness
            if match_score > 0.8:
                readiness = "HIGH"
            elif match_score >= 0.5:
                readiness = "MEDIUM"
            else:
                readiness = "LOW"
            
            skill_gaps = required_skills - possessed_skills
            
            # Step 6: Infer to_band by querying employees in to_role
            to_band = None
            employees_in_role = (
                db.query(Employee.band, func.count(Employee.id))
                .filter(Employee.role == career_path.to_role)
                .group_by(Employee.band)
                .order_by(func.count(Employee.id).desc())
                .first()
            )
            if employees_in_role:
                to_band = employees_in_role[0]
            
            # Get business unit name
            business_unit = (
                db.query(BusinessUnit)
                .filter(BusinessUnit.id == career_path.business_unit_id)
                .first()
            )
            business_unit_name = business_unit.name if business_unit else "Unknown"
            
            recommendations.append(
                CareerRecommendationItem(
                    career_path_id=career_path.id,
                    to_role=career_path.to_role,
                    to_band=to_band,
                    business_unit_id=career_path.business_unit_id,
                    business_unit_name=business_unit_name,
                    match_score=round(match_score, 2),
                    readiness=readiness,
                    required_skills=required_skills,
                    possessed_skills=possessed_skills,
                    skill_gaps=skill_gaps,
                    missing_skills=missing_skills_list,
                    estimated_learning_hours=estimated_hours
                )
            )
        
        # Step 5: Sort by match_score DESC, limit to max_recommendations
        recommendations.sort(key=lambda x: -x.match_score)
        recommendations = recommendations[:max_recommendations]
        
        logger.info(
            "Career recommendations retrieved for employee_id=%d, count=%d",
            employee_id, len(recommendations)
        )
        
        return CareerRecommendationsRead(
            employee_id=employee.id,
            employee_name=employee.name,
            current_role=employee.role,
            current_band=employee.band,
            business_unit_id=employee.business_unit_id,
            recommendations=recommendations,
            total_recommendations=len(recommendations)
        )
        
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)
