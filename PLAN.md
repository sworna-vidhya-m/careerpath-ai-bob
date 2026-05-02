# Analytics Endpoints Implementation Plan

## Overview

This document provides a step-by-step implementation plan for the 5 analytics endpoints documented in [`app/routers/analytics.py`](app/routers/analytics.py:1). The endpoints are ordered from simplest to most complex to enable incremental delivery.

## Implementation Order

1. **GET /analytics/skill-gap/{employee_id}** — Small complexity
2. **GET /analytics/industry-trends/{business_unit_id}** — Small complexity
3. **GET /analytics/skill-heatmap** — Medium complexity
4. **GET /analytics/career-recommendations/{employee_id}** — Medium complexity
5. **POST /analytics/trigger-bench-learning** — Large complexity

---

## Endpoint 1: GET /analytics/skill-gap/{employee_id}

### Endpoint Signature
- **Path**: `/analytics/skill-gap/{employee_id}`
- **Method**: GET
- **Path Parameters**: 
  - `employee_id` (int, required) — Employee primary key
- **Query Parameters**: None
- **Response Shape**: `SkillGapAnalysisRead`

```python
{
  "employee_id": 1,
  "employee_name": "Raj Kumar",
  "current_role": "Software Engineer",
  "business_unit_id": 1,
  "skill_gaps": [
    {
      "skill_id": 5,
      "skill_name": "Kubernetes",
      "current_proficiency": 0,  # 0 means not possessed
      "required_proficiency": 4,
      "gap": 4,
      "is_critical": true,
      "recommended_resources": [
        {
          "resource_id": 2,
          "title": "Kubernetes in Action",
          "type": "COURSE",
          "duration_hours": 40
        }
      ]
    }
  ],
  "total_gaps": 3,
  "critical_gaps": 1
}
```

### Data Sources
- [`Employee`](app/models.py:127) — Get employee details (name, role, business_unit_id)
- [`EmployeeSkill`](app/models.py:221) — Get current employee skills and proficiency levels
- [`CareerPath`](app/models.py:262) — Find career paths where `from_role` matches employee's current role
- [`CareerPathSkillRequirement`](app/models.py:277) — Get required skills for identified career paths
- [`Skill`](app/models.py:199) — Get skill names and categories
- [`LearningResource`](app/models.py:298) — Get recommended learning resources for gap skills

### Algorithm
1. Fetch employee by `employee_id`; raise [`NotFoundError`](app/exceptions.py:30) if not found
2. Query all [`EmployeeSkill`](app/models.py:221) records for this employee to build a proficiency map
3. Query [`CareerPath`](app/models.py:262) where `from_role` equals employee's current role and `business_unit_id` matches
4. For each career path, fetch [`CareerPathSkillRequirement`](app/models.py:277) records
5. Compare required proficiency vs. current proficiency (0 if skill not possessed)
6. For each gap (required > current), fetch 1-3 [`LearningResource`](app/models.py:298) records for that skill
7. Mark gaps as critical if `gap >= 3` or if skill has `is_emerging=True`
8. Return aggregated skill gap analysis

### Pydantic Schemas to Add
**File**: `app/schemas.py`

```python
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
```

### Test Cases to Add
**File**: `tests/test_analytics.py` (new file)

1. **Happy path**: `test_skill_gap_analysis_for_employee_with_gaps`
   - Use employee_id=1 (seeded data)
   - Assert response has expected structure
   - Assert `total_gaps >= 0`
   - Assert `skill_gaps` list contains valid gap items

2. **Error case**: `test_skill_gap_analysis_employee_not_found`
   - Use employee_id=99999
   - Assert 404 status code
   - Assert error message contains "Employee"

3. **Edge case**: `test_skill_gap_analysis_employee_with_no_career_paths`
   - Use employee with role that has no career paths defined
   - Assert response has `total_gaps=0` and empty `skill_gaps` list

### Estimated Complexity
**Small** — Straightforward data aggregation with clear relationships. No complex business logic.

---

## Endpoint 2: GET /analytics/industry-trends/{business_unit_id}

### Endpoint Signature
- **Path**: `/analytics/industry-trends/{business_unit_id}`
- **Method**: GET
- **Path Parameters**:
  - `business_unit_id` (int, required) — Business unit primary key
- **Query Parameters**:
  - `trend_filter` (Optional[SkillTrend]) — Filter by RISING, STABLE, or DECLINING
  - `limit` (int, default=20) — Max skills to return
- **Response Shape**: `IndustryTrendsRead`

```python
{
  "business_unit_id": 1,
  "business_unit_name": "Cloud Services",
  "trending_skills": [
    {
      "skill_id": 15,
      "skill_name": "GenAI Engineering",
      "category": "TECHNICAL",
      "is_emerging": true,
      "importance": 5,
      "trend": "RISING",
      "employee_count": 3,  # employees in BU with this skill
      "avg_proficiency": 2.7
    }
  ],
  "total_skills": 15,
  "rising_count": 8,
  "stable_count": 5,
  "declining_count": 2
}
```

### Data Sources
- [`BusinessUnit`](app/models.py:107) — Get business unit name
- [`IndustryStandardSkill`](app/models.py:242) — Get skills tracked for this BU with importance and trend
- [`Skill`](app/models.py:199) — Get skill details (name, category, is_emerging)
- [`EmployeeSkill`](app/models.py:221) — Count employees with each skill and calculate avg proficiency
- [`Employee`](app/models.py:127) — Filter employees by business_unit_id

### Algorithm
1. Fetch business unit by `business_unit_id`; raise [`NotFoundError`](app/exceptions.py:30) if not found
2. Query [`IndustryStandardSkill`](app/models.py:242) for this business unit
3. Apply optional `trend_filter` if provided
4. For each industry standard skill, join with [`Skill`](app/models.py:199) to get details
5. For each skill, count employees in this BU who possess it via [`EmployeeSkill`](app/models.py:221) join
6. Calculate average proficiency for employees in this BU who have the skill
7. Sort by importance DESC, then by trend (RISING first), limit results
8. Aggregate trend counts (rising, stable, declining)

### Pydantic Schemas to Add
**File**: `app/schemas.py`

```python
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
```

### Test Cases to Add
**File**: `tests/test_analytics.py`

1. **Happy path**: `test_industry_trends_for_business_unit`
   - Use business_unit_id=1 (seeded data)
   - Assert response structure is correct
   - Assert `trending_skills` list is not empty
   - Assert trend counts sum correctly

2. **Error case**: `test_industry_trends_business_unit_not_found`
   - Use business_unit_id=99999
   - Assert 404 status code

3. **Edge case**: `test_industry_trends_with_trend_filter_rising`
   - Use business_unit_id=1 with `trend_filter=RISING`
   - Assert all returned skills have `trend="RISING"`

### Estimated Complexity
**Small** — Simple aggregation query with filtering. No complex calculations.

---

## Endpoint 3: GET /analytics/skill-heatmap

### Endpoint Signature
- **Path**: `/analytics/skill-heatmap`
- **Method**: GET
- **Path Parameters**: None
- **Query Parameters**:
  - `business_unit_id` (Optional[int]) — Filter by business unit
  - `skill_category` (Optional[SkillCategory]) — Filter by TECHNICAL, DOMAIN, or SOFT
  - `min_importance` (Optional[int], 1-5) — Minimum importance threshold
- **Response Shape**: `SkillHeatmapRead`

```python
{
  "filters": {
    "business_unit_id": 1,
    "skill_category": "TECHNICAL",
    "min_importance": 3
  },
  "heatmap_data": [
    {
      "skill_id": 5,
      "skill_name": "Kubernetes",
      "category": "TECHNICAL",
      "is_emerging": false,
      "total_employees": 12,
      "proficiency_distribution": {
        "1": 2,
        "2": 3,
        "3": 4,
        "4": 2,
        "5": 1
      },
      "avg_proficiency": 2.9,
      "certified_count": 3,
      "business_units": [
        {
          "business_unit_id": 1,
          "business_unit_name": "Cloud Services",
          "employee_count": 8,
          "avg_proficiency": 3.2
        }
      ]
    }
  ],
  "total_skills": 25,
  "total_employees_analyzed": 30
}
```

### Data Sources
- [`Skill`](app/models.py:199) — Get all skills or filter by category
- [`EmployeeSkill`](app/models.py:221) — Get proficiency data for all employees
- [`Employee`](app/models.py:127) — Filter by business_unit_id if provided
- [`BusinessUnit`](app/models.py:107) — Get business unit names
- [`IndustryStandardSkill`](app/models.py:242) — Filter by min_importance if provided

### Algorithm
1. Build base query for [`Skill`](app/models.py:199), apply `skill_category` filter if provided
2. If `min_importance` provided, join with [`IndustryStandardSkill`](app/models.py:242) and filter
3. For each skill, query [`EmployeeSkill`](app/models.py:221) records
4. If `business_unit_id` provided, join with [`Employee`](app/models.py:127) to filter
5. For each skill, calculate:
   - Total employee count with this skill
   - Proficiency distribution (count per level 1-5)
   - Average proficiency
   - Count of certified employees
6. Group by business unit to show per-BU breakdown
7. Sort by total_employees DESC, then by avg_proficiency DESC

### Pydantic Schemas to Add
**File**: `app/schemas.py`

```python
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
```

### Test Cases to Add
**File**: `tests/test_analytics.py`

1. **Happy path**: `test_skill_heatmap_no_filters`
   - Call endpoint with no filters
   - Assert `heatmap_data` is not empty
   - Assert `total_skills > 0`
   - Assert proficiency_distribution sums match total_employees

2. **Error case**: `test_skill_heatmap_invalid_min_importance`
   - Use `min_importance=10` (out of range)
   - Assert 422 validation error

3. **Edge case**: `test_skill_heatmap_with_all_filters`
   - Apply business_unit_id, skill_category, and min_importance
   - Assert filters are reflected in response
   - Assert results match filter criteria

### Estimated Complexity
**Medium** — Requires aggregation across multiple dimensions (skills, employees, business units) with complex grouping logic.

---

## Endpoint 4: GET /analytics/career-recommendations/{employee_id}

### Endpoint Signature
- **Path**: `/analytics/career-recommendations/{employee_id}`
- **Method**: GET
- **Path Parameters**:
  - `employee_id` (int, required) — Employee primary key
- **Query Parameters**:
  - `include_cross_bu` (bool, default=false) — Include career paths from other business units
  - `max_recommendations` (int, default=5) — Maximum recommendations to return
- **Response Shape**: `CareerRecommendationsRead`

```python
{
  "employee_id": 1,
  "employee_name": "Raj Kumar",
  "current_role": "Software Engineer",
  "current_band": "B3",
  "business_unit_id": 1,
  "recommendations": [
    {
      "career_path_id": 3,
      "to_role": "Senior Software Engineer",
      "to_band": "B4",  # inferred from employees in that role
      "business_unit_id": 1,
      "business_unit_name": "Cloud Services",
      "match_score": 0.85,  # 0.0-1.0
      "readiness": "HIGH",  # HIGH, MEDIUM, LOW
      "required_skills": 8,
      "possessed_skills": 7,
      "skill_gaps": 1,
      "missing_skills": [
        {
          "skill_id": 5,
          "skill_name": "Kubernetes",
          "required_proficiency": 4,
          "current_proficiency": 0
        }
      ],
      "estimated_learning_hours": 40
    }
  ],
  "total_recommendations": 3
}
```

### Data Sources
- [`Employee`](app/models.py:127) — Get employee details and current role
- [`EmployeeSkill`](app/models.py:221) — Get employee's current skills
- [`CareerPath`](app/models.py:262) — Find paths from employee's current role
- [`CareerPathSkillRequirement`](app/models.py:277) — Get required skills for each path
- [`Skill`](app/models.py:199) — Get skill details
- [`LearningResource`](app/models.py:298) — Calculate estimated learning hours for gaps
- [`BusinessUnit`](app/models.py:107) — Get business unit names

### Algorithm
1. Fetch employee by `employee_id`; raise [`NotFoundError`](app/exceptions.py:30) if not found
2. Query [`CareerPath`](app/models.py:262) where `from_role` matches employee's role
3. If `include_cross_bu=false`, filter to employee's business_unit_id only
4. For each career path:
   - Fetch all [`CareerPathSkillRequirement`](app/models.py:277) records
   - Compare with employee's [`EmployeeSkill`](app/models.py:221) records
   - Calculate match_score: `possessed_skills / required_skills`
   - Determine readiness: HIGH (>0.8), MEDIUM (0.5-0.8), LOW (<0.5)
   - Identify missing skills (required but not possessed or proficiency too low)
   - Sum duration_hours from [`LearningResource`](app/models.py:298) for missing skills
5. Sort by match_score DESC, limit to `max_recommendations`
6. Infer `to_band` by querying employees in `to_role` and taking most common band

### Pydantic Schemas to Add
**File**: `app/schemas.py`

```python
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
```

### Test Cases to Add
**File**: `tests/test_analytics.py`

1. **Happy path**: `test_career_recommendations_for_employee`
   - Use employee_id=1
   - Assert recommendations list is not empty
   - Assert match_scores are between 0.0 and 1.0
   - Assert readiness values are valid (HIGH/MEDIUM/LOW)

2. **Error case**: `test_career_recommendations_employee_not_found`
   - Use employee_id=99999
   - Assert 404 status code

3. **Edge case**: `test_career_recommendations_include_cross_bu`
   - Use employee_id=1 with `include_cross_bu=true`
   - Assert some recommendations may be from different business units

### Estimated Complexity
**Medium** — Requires scoring algorithm, complex filtering, and aggregation across multiple tables. Band inference adds complexity.

---

## Endpoint 5: POST /analytics/trigger-bench-learning

### Endpoint Signature
- **Path**: `/analytics/trigger-bench-learning`
- **Method**: POST
- **Path Parameters**: None
- **Query Parameters**: None
- **Request Body**: `BenchLearningTriggerRequest`

```python
{
  "business_unit_id": 1,  # optional, null means all BUs
  "skill_ids": [5, 12, 18],  # optional, null means auto-select
  "max_enrollments_per_employee": 3,
  "dry_run": false
}
```

- **Response Shape**: `BenchLearningTriggerRead`

```python
{
  "triggered_at": "2026-05-02T16:30:00Z",
  "dry_run": false,
  "filters": {
    "business_unit_id": 1,
    "skill_ids": [5, 12, 18]
  },
  "bench_employees_found": 6,
  "enrollments_created": 12,
  "enrollments": [
    {
      "employee_id": 3,
      "employee_name": "Arun Patel",
      "resource_id": 2,
      "resource_title": "Kubernetes in Action",
      "skill_id": 5,
      "skill_name": "Kubernetes",
      "enrollment_id": 45,  # null if dry_run=true
      "reason": "Skill gap for career path to Senior Engineer"
    }
  ],
  "summary": {
    "total_hours_allocated": 480,
    "skills_targeted": 3,
    "avg_enrollments_per_employee": 2.0
  }
}
```

### Data Sources
- [`Employee`](app/models.py:127) — Find employees with `current_status=BENCH`
- [`EmployeeSkill`](app/models.py:221) — Identify skill gaps for bench employees
- [`CareerPath`](app/models.py:262) — Find career paths from employee's current role
- [`CareerPathSkillRequirement`](app/models.py:277) — Determine required skills
- [`IndustryStandardSkill`](app/models.py:242) — Prioritize high-importance skills
- [`LearningResource`](app/models.py:298) — Find resources for gap skills
- [`LearningEnrollment`](app/models.py:314) — Create new enrollments (if not dry_run)
- [`BusinessUnit`](app/models.py:107) — Filter by business unit if provided

### Algorithm
1. Query [`Employee`](app/models.py:127) where `current_status=BENCH`
2. If `business_unit_id` provided, filter to that BU
3. For each bench employee:
   - Get current skills from [`EmployeeSkill`](app/models.py:221)
   - Find career paths from [`CareerPath`](app/models.py:262) matching their role
   - Identify skill gaps from [`CareerPathSkillRequirement`](app/models.py:277)
   - If `skill_ids` provided, filter gaps to those skills only
   - Otherwise, prioritize by [`IndustryStandardSkill`](app/models.py:242) importance
4. For each skill gap, find best [`LearningResource`](app/models.py:298) (shortest duration, prefer COURSE type)
5. Limit to `max_enrollments_per_employee` per employee
6. If `dry_run=false`, create [`LearningEnrollment`](app/models.py:314) records with status=ENROLLED
7. Calculate summary statistics (total hours, skills targeted, avg enrollments)
8. Return detailed enrollment list with reasons

### Pydantic Schemas to Add
**File**: `app/schemas.py`

```python
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
```

### Test Cases to Add
**File**: `tests/test_analytics.py`

1. **Happy path**: `test_trigger_bench_learning_dry_run`
   - Use dry_run=true
   - Assert bench_employees_found > 0
   - Assert enrollments list is populated
   - Assert all enrollment_id values are null

2. **Error case**: `test_trigger_bench_learning_invalid_business_unit`
   - Use business_unit_id=99999
   - Assert 404 status code or empty result with 0 bench employees

3. **Edge case**: `test_trigger_bench_learning_with_skill_filter`
   - Provide specific skill_ids list
   - Assert all enrollments target only those skills
   - Assert enrollments_created <= (bench_employees * max_enrollments_per_employee)

4. **Integration test**: `test_trigger_bench_learning_creates_enrollments`
   - Use dry_run=false
   - Assert enrollments are created in database
   - Query [`LearningEnrollment`](app/models.py:314) to verify records exist
   - Assert enrollment_id values are not null

### Estimated Complexity
**Large** — Most complex endpoint. Requires:
- Multi-step business logic (find bench employees, analyze gaps, prioritize, create enrollments)
- Write operations (creating enrollments)
- Transaction management
- Complex filtering and prioritization
- Dry-run mode support
- Comprehensive validation

---

## Implementation Checklist

### Phase 1: Foundation (Before Endpoint Implementation)
- [ ] Add all Pydantic schemas to [`app/schemas.py`](app/schemas.py:1)
- [ ] Create [`tests/test_analytics.py`](tests/test_analytics.py) with test fixtures
- [ ] Import necessary models and exceptions in [`app/routers/analytics.py`](app/routers/analytics.py:1)

### Phase 2: Endpoint Implementation (In Order)
- [ ] Implement Endpoint 1: `GET /analytics/skill-gap/{employee_id}`
- [ ] Write tests for Endpoint 1
- [ ] Implement Endpoint 2: `GET /analytics/industry-trends/{business_unit_id}`
- [ ] Write tests for Endpoint 2
- [ ] Implement Endpoint 3: `GET /analytics/skill-heatmap`
- [ ] Write tests for Endpoint 3
- [ ] Implement Endpoint 4: `GET /analytics/career-recommendations/{employee_id}`
- [ ] Write tests for Endpoint 4
- [ ] Implement Endpoint 5: `POST /analytics/trigger-bench-learning`
- [ ] Write tests for Endpoint 5

### Phase 3: Validation
- [ ] Run full test suite: `pytest -v`
- [ ] Verify all 21 existing smoke tests still pass
- [ ] Verify all new analytics tests pass
- [ ] Test endpoints manually via `/static/index.html` or curl
- [ ] Update [`AGENTS.md`](AGENTS.md:1) to reflect implemented endpoints

---

## Common Patterns to Follow

### Exception Handling
All endpoints must follow this pattern:

```python
try:
    # Domain logic that may raise AppException
    result = some_operation()
    return result
except NotFoundError as exc:
    raise_http_from_app_exception(exc)
except ValidationError as exc:
    raise_http_from_app_exception(exc)
except BusinessRuleError as exc:
    raise_http_from_app_exception(exc)
```

### Database Session Management
Use dependency injection:

```python
@router.get("/analytics/example")
def example_endpoint(db: Session = Depends(get_db)) -> SomeSchema:
    # Use db session here
    pass
```

### Logging
Add info-level logging for successful operations:

```python
logger.info("Skill gap analysis completed for employee_id=%d, gaps=%d", 
            employee_id, len(gaps))
```

### Python 3.9 Compatibility
- Use `Optional[Type]` instead of `Type | None`
- Use `List[Type]` instead of `list[Type]`
- Use `Dict[str, Type]` instead of `dict[str, Type]`
- No `match` statements

### Response Models
Always specify `response_model` in route decorator:

```python
@router.get("/analytics/example", response_model=ExampleRead)
def example_endpoint(...) -> ModelClass:
    pass
```

---

## Testing Strategy

### Test File Structure
```python
# tests/test_analytics.py

import pytest
from fastapi.testclient import TestClient

# Endpoint 1 tests
def test_skill_gap_analysis_for_employee_with_gaps(client: TestClient) -> None:
    pass

def test_skill_gap_analysis_employee_not_found(client: TestClient) -> None:
    pass

# ... more tests
```

### Test Data
All tests use seeded data from [`app/seed.py`](app/seed.py:1):
- 8 business units
- 30 employees (6 BENCH, 4 LEARNING, 20 ACTIVE)
- 52 skills (12 emerging)
- 20 projects
- Multiple career paths and skill requirements

### Assertions
Each test should verify:
1. HTTP status code
2. Response structure matches schema
3. Business logic correctness
4. Edge case handling

---

## Notes

- All endpoints are read-only except `POST /analytics/trigger-bench-learning`
- No authentication/authorization required (per existing pattern)
- All dates/times use ISO 8601 format
- Proficiency scale is 1-5 (per [`EmployeeSkill`](app/models.py:221) constraint)
- Importance scale is 1-5 (per [`IndustryStandardSkill`](app/models.py:242) constraint)
- Line length limit: 100 characters (Black/Ruff configured)
- Keep functions under 50 lines where reasonable

---

## Estimated Timeline

- **Endpoint 1**: 2-3 hours (implementation + tests)
- **Endpoint 2**: 2-3 hours (implementation + tests)
- **Endpoint 3**: 4-5 hours (implementation + tests)
- **Endpoint 4**: 4-5 hours (implementation + tests)
- **Endpoint 5**: 6-8 hours (implementation + tests)

**Total**: 18-24 hours for complete implementation and testing.

---

## Success Criteria

1. All 5 endpoints implemented and functional
2. All new tests pass (minimum 15 tests total)
3. All existing 21 smoke tests still pass
4. Code follows existing patterns in [`app/routers/`](app/routers/)
5. Exception handling uses domain exceptions from [`app/exceptions.py`](app/exceptions.py:1)
6. Pydantic schemas added to [`app/schemas.py`](app/schemas.py:1)
7. Python 3.9 compatible (no modern syntax)
8. Line length ≤ 100 characters
9. Functions ≤ 50 lines where reasonable
10. Proper logging for all operations