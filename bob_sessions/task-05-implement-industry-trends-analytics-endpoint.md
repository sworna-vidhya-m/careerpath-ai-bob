**User:**

<task>
Implement Endpoint 2 from @PLAN.md: GET /analytics/industry-trends/{business_unit_id}.

Scope (do this and ONLY this):

1. Add the two new Pydantic schemas (`TrendingSkillItem`, `IndustryTrendsRead`) to `app/schemas.py` exactly as specified in PLAN.md Endpoint 2 section. Place them logically — group with related schemas, not blindly at the end.

2. Implement the endpoint in `app/routers/analytics.py`, alongside the existing routes. Do not modify or remove the `/analytics/health` route or the `/analytics/skill-gap/{employee_id}` route. Follow the algorithm in PLAN.md "Endpoint 2: Algorithm" step by step. Use the same exception pattern as Endpoint 1.

3. Append three new tests to `tests/test_analytics.py` (do not delete existing tests):
   - `test_industry_trends_for_business_unit` (happy path, business_unit_id=1)
   - `test_industry_trends_business_unit_not_found` (error case, business_unit_id=99999, expect 404)
   - `test_industry_trends_with_trend_filter_rising` (edge case, business_unit_id=1, trend_filter=RISING)

4. Run `pytest -v` after implementation. Stop only after ALL tests pass — 21 smoke + 3 skill-gap + 3 new industry-trends = 27 total.

5. Verify the app still imports cleanly: `python -c "from app.main import app"`. Must return exit code 0.

Constraints:
- Python 3.9 syntax only — `Optional[X]`, `List[X]`. No `X | Y`.
- Line length ≤ 100 characters.
- Functions ≤ 50 lines where reasonable.
- Reference @.bob/skills/add-feature.md for behavioral guidance.
- Reference @.bob/rules/project-rules.md for coding standards.
- Do NOT touch any file outside: `app/schemas.py`, `app/routers/analytics.py`, `tests/test_analytics.py`.
- Do NOT update README.md, AGENTS.md, or PLAN.md.

Deliverable: 3 files modified, all 27 tests passing, app imports cleanly.
</task>
<environment_details>
# VSCode Visible Files
demo-script.md

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:28:58.394Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (/Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob) Files
.gitignore
AGENTS.md
demo-script.md
PLAN.md
pyproject.toml
README_CHECKLIST.md
README.md
requirements.txt
run.sh
.bob/
app/
app/__init__.py
app/database.py
app/exceptions.py
app/logging_config.py
app/main.py
app/models.py
app/schemas.py
app/seed.py
app/routers/
app/routers/__init__.py
app/routers/analytics.py
app/routers/assignments.py
app/routers/business_units.py
app/routers/career_path_requirements.py
app/routers/career_paths.py
app/routers/employee_skills.py
app/routers/employees.py
app/routers/enrollments.py
app/routers/industry_standards.py
app/routers/learning_resources.py
app/routers/projects.py
app/routers/skills.py
bob_sessions/
bob_sessions/.gitkeep
bob_sessions/README.md
bob_sessions/task-01-summarize-app-flow.md
bob_sessions/task-01-summarize-app-flow.png
bob_sessions/task-02-Agent-md-created.md
bob_sessions/task-02-Agent-md-created.png
bob_sessions/task-03-create-implementation-plan-md-file.md
bob_sessions/task-03-create-implementation-plan-md-file.png
bob_sessions/task-04-implement-skilGap-analytics-endpoint.md
bob_sessions/task-04-implement-skilGap-analytics-endpoint.png
data/
data/.gitkeep
docs/
docs/.gitkeep
static/
static/index.html
tests/
tests/__init__.py
tests/conftest.py
tests/test_analytics.py
tests/test_smoke.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll implement Endpoint 2 step by step. Let me start by reading the relevant files to understand the current state and the plan.

<read_file>
<args>
<file>
<path>PLAN.md</path>
<line_range>1-200</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>PLAN.md</path>
<content lines="1-200">
  1 | # Analytics Endpoints Implementation Plan
  2 | 
  3 | ## Overview
  4 | 
  5 | This document provides a step-by-step implementation plan for the 5 analytics endpoints documented in [`app/routers/analytics.py`](app/routers/analytics.py:1). The endpoints are ordered from simplest to most complex to enable incremental delivery.
  6 | 
  7 | ## Implementation Order
  8 | 
  9 | 1. **GET /analytics/skill-gap/{employee_id}** — Small complexity
 10 | 2. **GET /analytics/industry-trends/{business_unit_id}** — Small complexity
 11 | 3. **GET /analytics/skill-heatmap** — Medium complexity
 12 | 4. **GET /analytics/career-recommendations/{employee_id}** — Medium complexity
 13 | 5. **POST /analytics/trigger-bench-learning** — Large complexity
 14 | 
 15 | ---
 16 | 
 17 | ## Endpoint 1: GET /analytics/skill-gap/{employee_id}
 18 | 
 19 | ### Endpoint Signature
 20 | - **Path**: `/analytics/skill-gap/{employee_id}`
 21 | - **Method**: GET
 22 | - **Path Parameters**: 
 23 |   - `employee_id` (int, required) — Employee primary key
 24 | - **Query Parameters**: None
 25 | - **Response Shape**: `SkillGapAnalysisRead`
 26 | 
 27 | ```python
 28 | {
 29 |   "employee_id": 1,
 30 |   "employee_name": "Raj Kumar",
 31 |   "current_role": "Software Engineer",
 32 |   "business_unit_id": 1,
 33 |   "skill_gaps": [
 34 |     {
 35 |       "skill_id": 5,
 36 |       "skill_name": "Kubernetes",
 37 |       "current_proficiency": 0,  # 0 means not possessed
 38 |       "required_proficiency": 4,
 39 |       "gap": 4,
 40 |       "is_critical": true,
 41 |       "recommended_resources": [
 42 |         {
 43 |           "resource_id": 2,
 44 |           "title": "Kubernetes in Action",
 45 |           "type": "COURSE",
 46 |           "duration_hours": 40
 47 |         }
 48 |       ]
 49 |     }
 50 |   ],
 51 |   "total_gaps": 3,
 52 |   "critical_gaps": 1
 53 | }
 54 | ```
 55 | 
 56 | ### Data Sources
 57 | - [`Employee`](app/models.py:127) — Get employee details (name, role, business_unit_id)
 58 | - [`EmployeeSkill`](app/models.py:221) — Get current employee skills and proficiency levels
 59 | - [`CareerPath`](app/models.py:262) — Find career paths where `from_role` matches employee's current role
 60 | - [`CareerPathSkillRequirement`](app/models.py:277) — Get required skills for identified career paths
 61 | - [`Skill`](app/models.py:199) — Get skill names and categories
 62 | - [`LearningResource`](app/models.py:298) — Get recommended learning resources for gap skills
 63 | 
 64 | ### Algorithm
 65 | 1. Fetch employee by `employee_id`; raise [`NotFoundError`](app/exceptions.py:30) if not found
 66 | 2. Query all [`EmployeeSkill`](app/models.py:221) records for this employee to build a proficiency map
 67 | 3. Query [`CareerPath`](app/models.py:262) where `from_role` equals employee's current role and `business_unit_id` matches
 68 | 4. For each career path, fetch [`CareerPathSkillRequirement`](app/models.py:277) records
 69 | 5. Compare required proficiency vs. current proficiency (0 if skill not possessed)
 70 | 6. For each gap (required > current), fetch 1-3 [`LearningResource`](app/models.py:298) records for that skill
 71 | 7. Mark gaps as critical if `gap >= 3` or if skill has `is_emerging=True`
 72 | 8. Return aggregated skill gap analysis
 73 | 
 74 | ### Pydantic Schemas to Add
 75 | **File**: `app/schemas.py`
 76 | 
 77 | ```python
 78 | class RecommendedResourceRead(BaseModel):
 79 |     """Minimal learning resource info for recommendations."""
 80 |     model_config = ConfigDict(from_attributes=True)
 81 |     
 82 |     resource_id: int
 83 |     title: str
 84 |     type: LearningResourceType
 85 |     duration_hours: int
 86 | 
 87 | 
 88 | class SkillGapItem(BaseModel):
 89 |     """Individual skill gap with recommendation."""
 90 |     
 91 |     skill_id: int
 92 |     skill_name: str
 93 |     current_proficiency: int  # 0-5, 0 means not possessed
 94 |     required_proficiency: int  # 1-5
 95 |     gap: int
 96 |     is_critical: bool
 97 |     recommended_resources: List[RecommendedResourceRead]
 98 | 
 99 | 
100 | class SkillGapAnalysisRead(BaseModel):
101 |     """Complete skill gap analysis for an employee."""
102 |     
103 |     employee_id: int
104 |     employee_name: str
105 |     current_role: str
106 |     business_unit_id: int
107 |     skill_gaps: List[SkillGapItem]
108 |     total_gaps: int
109 |     critical_gaps: int
110 | ```
111 | 
112 | ### Test Cases to Add
113 | **File**: `tests/test_analytics.py` (new file)
114 | 
115 | 1. **Happy path**: `test_skill_gap_analysis_for_employee_with_gaps`
116 |    - Use employee_id=1 (seeded data)
117 |    - Assert response has expected structure
118 |    - Assert `total_gaps >= 0`
119 |    - Assert `skill_gaps` list contains valid gap items
120 | 
121 | 2. **Error case**: `test_skill_gap_analysis_employee_not_found`
122 |    - Use employee_id=99999
123 |    - Assert 404 status code
124 |    - Assert error message contains "Employee"
125 | 
126 | 3. **Edge case**: `test_skill_gap_analysis_employee_with_no_career_paths`
127 |    - Use employee with role that has no career paths defined
128 |    - Assert response has `total_gaps=0` and empty `skill_gaps` list
129 | 
130 | ### Estimated Complexity
131 | **Small** — Straightforward data aggregation with clear relationships. No complex business logic.
132 | 
133 | ---
134 | 
135 | ## Endpoint 2: GET /analytics/industry-trends/{business_unit_id}
136 | 
137 | ### Endpoint Signature
138 | - **Path**: `/analytics/industry-trends/{business_unit_id}`
139 | - **Method**: GET
140 | - **Path Parameters**:
141 |   - `business_unit_id` (int, required) — Business unit primary key
142 | - **Query Parameters**:
143 |   - `trend_filter` (Optional[SkillTrend]) — Filter by RISING, STABLE, or DECLINING
144 |   - `limit` (int, default=20) — Max skills to return
145 | - **Response Shape**: `IndustryTrendsRead`
146 | 
147 | ```python
148 | {
149 |   "business_unit_id": 1,
150 |   "business_unit_name": "Cloud Services",
151 |   "trending_skills": [
152 |     {
153 |       "skill_id": 15,
154 |       "skill_name": "GenAI Engineering",
155 |       "category": "TECHNICAL",
156 |       "is_emerging": true,
157 |       "importance": 5,
158 |       "trend": "RISING",
159 |       "employee_count": 3,  # employees in BU with this skill
160 |       "avg_proficiency": 2.7
161 |     }
162 |   ],
163 |   "total_skills": 15,
164 |   "rising_count": 8,
165 |   "stable_count": 5,
166 |   "declining_count": 2
167 | }
168 | ```
169 | 
170 | ### Data Sources
171 | - [`BusinessUnit`](app/models.py:107) — Get business unit name
172 | - [`IndustryStandardSkill`](app/models.py:242) — Get skills tracked for this BU with importance and trend
173 | - [`Skill`](app/models.py:199) — Get skill details (name, category, is_emerging)
174 | - [`EmployeeSkill`](app/models.py:221) — Count employees with each skill and calculate avg proficiency
175 | - [`Employee`](app/models.py:127) — Filter employees by business_unit_id
176 | 
177 | ### Algorithm
178 | 1. Fetch business unit by `business_unit_id`; raise [`NotFoundError`](app/exceptions.py:30) if not found
179 | 2. Query [`IndustryStandardSkill`](app/models.py:242) for this business unit
180 | 3. Apply optional `trend_filter` if provided
181 | 4. For each industry standard skill, join with [`Skill`](app/models.py:199) to get details
182 | 5. For each skill, count employees in this BU who possess it via [`EmployeeSkill`](app/models.py:221) join
183 | 6. Calculate average proficiency for employees in this BU who have the skill
184 | 7. Sort by importance DESC, then by trend (RISING first), limit results
185 | 8. Aggregate trend counts (rising, stable, declining)
186 | 
187 | ### Pydantic Schemas to Add
188 | **File**: `app/schemas.py`
189 | 
190 | ```python
191 | class TrendingSkillItem(BaseModel):
192 |     """Industry trend data for a single skill."""
193 |     
194 |     skill_id: int
195 |     skill_name: str
196 |     category: SkillCategory
197 |     is_emerging: bool
198 |     importance: int  # 1-5
199 |     trend: SkillTrend
200 |     employee_count: int
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
demo-script.md

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:29:04.285Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>PLAN.md</path>
<line_range>200-250</line_range>
</file>
<file>
<path>app/schemas.py</path>
</file>
<file>
<path>app/routers/analytics.py</path>
</file>
<file>
<path>tests/test_analytics.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>PLAN.md</path>
<content lines="200-250">
200 |     employee_count: int
201 |     avg_proficiency: float  # 0.0-5.0
202 | 
203 | 
204 | class IndustryTrendsRead(BaseModel):
205 |     """Industry skill trends for a business unit."""
206 |     
207 |     business_unit_id: int
208 |     business_unit_name: str
209 |     trending_skills: List[TrendingSkillItem]
210 |     total_skills: int
211 |     rising_count: int
212 |     stable_count: int
213 |     declining_count: int
214 | ```
215 | 
216 | ### Test Cases to Add
217 | **File**: `tests/test_analytics.py`
218 | 
219 | 1. **Happy path**: `test_industry_trends_for_business_unit`
220 |    - Use business_unit_id=1 (seeded data)
221 |    - Assert response structure is correct
222 |    - Assert `trending_skills` list is not empty
223 |    - Assert trend counts sum correctly
224 | 
225 | 2. **Error case**: `test_industry_trends_business_unit_not_found`
226 |    - Use business_unit_id=99999
227 |    - Assert 404 status code
228 | 
229 | 3. **Edge case**: `test_industry_trends_with_trend_filter_rising`
230 |    - Use business_unit_id=1 with `trend_filter=RISING`
231 |    - Assert all returned skills have `trend="RISING"`
232 | 
233 | ### Estimated Complexity
234 | **Small** — Simple aggregation query with filtering. No complex calculations.
235 | 
236 | ---
237 | 
238 | ## Endpoint 3: GET /analytics/skill-heatmap
239 | 
240 | ### Endpoint Signature
241 | - **Path**: `/analytics/skill-heatmap`
242 | - **Method**: GET
243 | - **Path Parameters**: None
244 | - **Query Parameters**:
245 |   - `business_unit_id` (Optional[int]) — Filter by business unit
246 |   - `skill_category` (Optional[SkillCategory]) — Filter by TECHNICAL, DOMAIN, or SOFT
247 |   - `min_importance` (Optional[int], 1-5) — Minimum importance threshold
248 | - **Response Shape**: `SkillHeatmapRead`
249 | 
250 | ```python
</content>
</file>
<file><path>app/schemas.py</path>
<content lines="1-483">
  1 | """Pydantic v2 schemas for request validation and response serialisation.
  2 | 
  3 | Each entity has four schema classes:
  4 |   XBase    — shared fields
  5 |   XCreate  — fields required on POST
  6 |   XUpdate  — all fields optional for partial PUT
  7 |   XRead    — full response including id and timestamps
  8 | """
  9 | 
 10 | import logging
 11 | from datetime import date, datetime
 12 | from typing import List, Optional
 13 | 
 14 | from pydantic import BaseModel, ConfigDict, EmailStr, Field
 15 | 
 16 | from app.models import (
 17 |     EmployeeStatus,
 18 |     EnrollmentStatus,
 19 |     LearningResourceType,
 20 |     ProjectStatus,
 21 |     SkillCategory,
 22 |     SkillTrend,
 23 | )
 24 | 
 25 | logger = logging.getLogger(__name__)
 26 | 
 27 | # ---------------------------------------------------------------------------
 28 | # BusinessUnit
 29 | # ---------------------------------------------------------------------------
 30 | 
 31 | 
 32 | class BusinessUnitBase(BaseModel):
 33 |     """Shared fields for BusinessUnit."""
 34 | 
 35 |     name: str = Field(..., min_length=1, max_length=120)
 36 |     description: Optional[str] = None
 37 | 
 38 | 
 39 | class BusinessUnitCreate(BusinessUnitBase):
 40 |     """Fields required to create a BusinessUnit."""
 41 | 
 42 | 
 43 | class BusinessUnitUpdate(BaseModel):
 44 |     """All fields optional for partial update of BusinessUnit."""
 45 | 
 46 |     name: Optional[str] = Field(None, min_length=1, max_length=120)
 47 |     description: Optional[str] = None
 48 | 
 49 | 
 50 | class BusinessUnitRead(BusinessUnitBase):
 51 |     """Full BusinessUnit response including id and timestamps."""
 52 | 
 53 |     model_config = ConfigDict(from_attributes=True)
 54 | 
 55 |     id: int
 56 |     created_at: datetime
 57 |     updated_at: datetime
 58 | 
 59 | 
 60 | # ---------------------------------------------------------------------------
 61 | # Employee
 62 | # ---------------------------------------------------------------------------
 63 | 
 64 | 
 65 | class EmployeeBase(BaseModel):
 66 |     """Shared fields for Employee."""
 67 | 
 68 |     name: str = Field(..., min_length=1, max_length=120)
 69 |     email: str = Field(..., max_length=255)
 70 |     role: str = Field(..., min_length=1, max_length=120)
 71 |     band: str = Field(..., min_length=1, max_length=60)
 72 |     business_unit_id: int
 73 |     line_manager_id: Optional[int] = None
 74 |     current_status: EmployeeStatus = EmployeeStatus.ACTIVE
 75 |     hire_date: date
 76 | 
 77 | 
 78 | class EmployeeCreate(EmployeeBase):
 79 |     """Fields required to create an Employee."""
 80 | 
 81 | 
 82 | class EmployeeUpdate(BaseModel):
 83 |     """All fields optional for partial update of Employee."""
 84 | 
 85 |     name: Optional[str] = Field(None, min_length=1, max_length=120)
 86 |     email: Optional[str] = Field(None, max_length=255)
 87 |     role: Optional[str] = Field(None, min_length=1, max_length=120)
 88 |     band: Optional[str] = Field(None, min_length=1, max_length=60)
 89 |     business_unit_id: Optional[int] = None
 90 |     line_manager_id: Optional[int] = None
 91 |     current_status: Optional[EmployeeStatus] = None
 92 |     hire_date: Optional[date] = None
 93 | 
 94 | 
 95 | class EmployeeRead(EmployeeBase):
 96 |     """Full Employee response including id and timestamps."""
 97 | 
 98 |     model_config = ConfigDict(from_attributes=True)
 99 | 
100 |     id: int
101 |     created_at: datetime
102 |     updated_at: datetime
103 | 
104 | 
105 | # ---------------------------------------------------------------------------
106 | # Project
107 | # ---------------------------------------------------------------------------
108 | 
109 | 
110 | class ProjectBase(BaseModel):
111 |     """Shared fields for Project."""
112 | 
113 |     name: str = Field(..., min_length=1, max_length=200)
114 |     client: str = Field(..., min_length=1, max_length=200)
115 |     start_date: date
116 |     end_date: Optional[date] = None
117 |     status: ProjectStatus
118 | 
119 | 
120 | class ProjectCreate(ProjectBase):
121 |     """Fields required to create a Project."""
122 | 
123 | 
124 | class ProjectUpdate(BaseModel):
125 |     """All fields optional for partial update of Project."""
126 | 
127 |     name: Optional[str] = Field(None, min_length=1, max_length=200)
128 |     client: Optional[str] = Field(None, min_length=1, max_length=200)
129 |     start_date: Optional[date] = None
130 |     end_date: Optional[date] = None
131 |     status: Optional[ProjectStatus] = None
132 | 
133 | 
134 | class ProjectRead(ProjectBase):
135 |     """Full Project response including id and timestamps."""
136 | 
137 |     model_config = ConfigDict(from_attributes=True)
138 | 
139 |     id: int
140 |     created_at: datetime
141 |     updated_at: datetime
142 | 
143 | 
144 | # ---------------------------------------------------------------------------
145 | # ProjectAssignment
146 | # ---------------------------------------------------------------------------
147 | 
148 | 
149 | class ProjectAssignmentBase(BaseModel):
150 |     """Shared fields for ProjectAssignment."""
151 | 
152 |     employee_id: int
153 |     project_id: int
154 |     role_on_project: str = Field(..., min_length=1, max_length=120)
155 |     allocation_pct: int = Field(default=100, ge=0, le=100)
156 |     start_date: date
157 |     end_date: Optional[date] = None
158 | 
159 | 
160 | class ProjectAssignmentCreate(ProjectAssignmentBase):
161 |     """Fields required to create a ProjectAssignment."""
162 | 
163 | 
164 | class ProjectAssignmentUpdate(BaseModel):
165 |     """All fields optional for partial update of ProjectAssignment."""
166 | 
167 |     employee_id: Optional[int] = None
168 |     project_id: Optional[int] = None
169 |     role_on_project: Optional[str] = Field(None, min_length=1, max_length=120)
170 |     allocation_pct: Optional[int] = Field(None, ge=0, le=100)
171 |     start_date: Optional[date] = None
172 |     end_date: Optional[date] = None
173 | 
174 | 
175 | class ProjectAssignmentRead(ProjectAssignmentBase):
176 |     """Full ProjectAssignment response including id and timestamps."""
177 | 
178 |     model_config = ConfigDict(from_attributes=True)
179 | 
180 |     id: int
181 |     created_at: datetime
182 |     updated_at: datetime
183 | 
184 | 
185 | # ---------------------------------------------------------------------------
186 | # Skill
187 | # ---------------------------------------------------------------------------
188 | 
189 | 
190 | class SkillBase(BaseModel):
191 |     """Shared fields for Skill."""
192 | 
193 |     name: str = Field(..., min_length=1, max_length=120)
194 |     category: SkillCategory
195 |     is_emerging: bool = False
196 | 
197 | 
198 | class SkillCreate(SkillBase):
199 |     """Fields required to create a Skill."""
200 | 
201 | 
202 | class SkillUpdate(BaseModel):
203 |     """All fields optional for partial update of Skill."""
204 | 
205 |     name: Optional[str] = Field(None, min_length=1, max_length=120)
206 |     category: Optional[SkillCategory] = None
207 |     is_emerging: Optional[bool] = None
208 | 
209 | 
210 | class SkillRead(SkillBase):
211 |     """Full Skill response including id and timestamps."""
212 | 
213 |     model_config = ConfigDict(from_attributes=True)
214 | 
215 |     id: int
216 |     created_at: datetime
217 |     updated_at: datetime
218 | 
219 | 
220 | # ---------------------------------------------------------------------------
221 | # EmployeeSkill
222 | # ---------------------------------------------------------------------------
223 | 
224 | 
225 | class EmployeeSkillBase(BaseModel):
226 |     """Shared fields for EmployeeSkill."""
227 | 
228 |     employee_id: int
229 |     skill_id: int
230 |     proficiency: int = Field(..., ge=1, le=5)
231 |     last_used_at: Optional[date] = None
232 |     certified: bool = False
233 | 
234 | 
235 | class EmployeeSkillCreate(EmployeeSkillBase):
236 |     """Fields required to create an EmployeeSkill."""
237 | 
238 | 
239 | class EmployeeSkillUpdate(BaseModel):
240 |     """All fields optional for partial update of EmployeeSkill."""
241 | 
242 |     employee_id: Optional[int] = None
243 |     skill_id: Optional[int] = None
244 |     proficiency: Optional[int] = Field(None, ge=1, le=5)
245 |     last_used_at: Optional[date] = None
246 |     certified: Optional[bool] = None
247 | 
248 | 
249 | class EmployeeSkillRead(EmployeeSkillBase):
250 |     """Full EmployeeSkill response including id and timestamps."""
251 | 
252 |     model_config = ConfigDict(from_attributes=True)
253 | 
254 |     id: int
255 |     created_at: datetime
256 |     updated_at: datetime
257 | 
258 | 
259 | # ---------------------------------------------------------------------------
260 | # IndustryStandardSkill
261 | # ---------------------------------------------------------------------------
262 | 
263 | 
264 | class IndustryStandardSkillBase(BaseModel):
265 |     """Shared fields for IndustryStandardSkill."""
266 | 
267 |     business_unit_id: int
268 |     skill_id: int
269 |     importance: int = Field(..., ge=1, le=5)
270 |     trend: SkillTrend
271 | 
272 | 
273 | class IndustryStandardSkillCreate(IndustryStandardSkillBase):
274 |     """Fields required to create an IndustryStandardSkill."""
275 | 
276 | 
277 | class IndustryStandardSkillUpdate(BaseModel):
278 |     """All fields optional for partial update of IndustryStandardSkill."""
279 | 
280 |     business_unit_id: Optional[int] = None
281 |     skill_id: Optional[int] = None
282 |     importance: Optional[int] = Field(None, ge=1, le=5)
283 |     trend: Optional[SkillTrend] = None
284 | 
285 | 
286 | class IndustryStandardSkillRead(IndustryStandardSkillBase):
287 |     """Full IndustryStandardSkill response including id and timestamps."""
288 | 
289 |     model_config = ConfigDict(from_attributes=True)
290 | 
291 |     id: int
292 |     created_at: datetime
293 |     updated_at: datetime
294 | 
295 | 
296 | # ---------------------------------------------------------------------------
297 | # CareerPath
298 | # ---------------------------------------------------------------------------
299 | 
300 | 
301 | class CareerPathBase(BaseModel):
302 |     """Shared fields for CareerPath."""
303 | 
304 |     business_unit_id: int
305 |     from_role: str = Field(..., min_length=1, max_length=120)
306 |     to_role: str = Field(..., min_length=1, max_length=120)
307 |     description: Optional[str] = None
308 | 
309 | 
310 | class CareerPathCreate(CareerPathBase):
311 |     """Fields required to create a CareerPath."""
312 | 
313 | 
314 | class CareerPathUpdate(BaseModel):
315 |     """All fields optional for partial update of CareerPath."""
316 | 
317 |     business_unit_id: Optional[int] = None
318 |     from_role: Optional[str] = Field(None, min_length=1, max_length=120)
319 |     to_role: Optional[str] = Field(None, min_length=1, max_length=120)
320 |     description: Optional[str] = None
321 | 
322 | 
323 | class CareerPathRead(CareerPathBase):
324 |     """Full CareerPath response including id and timestamps."""
325 | 
326 |     model_config = ConfigDict(from_attributes=True)
327 | 
328 |     id: int
329 |     created_at: datetime
330 |     updated_at: datetime
331 | 
332 | 
333 | # ---------------------------------------------------------------------------
334 | # CareerPathSkillRequirement
335 | # ---------------------------------------------------------------------------
336 | 
337 | 
338 | class CareerPathSkillRequirementBase(BaseModel):
339 |     """Shared fields for CareerPathSkillRequirement."""
340 | 
341 |     career_path_id: int
342 |     skill_id: int
343 |     min_proficiency: int = Field(..., ge=1, le=5)
344 | 
345 | 
346 | class CareerPathSkillRequirementCreate(CareerPathSkillRequirementBase):
347 |     """Fields required to create a CareerPathSkillRequirement."""
348 | 
349 | 
350 | class CareerPathSkillRequirementUpdate(BaseModel):
351 |     """All fields optional for partial update of CareerPathSkillRequirement."""
352 | 
353 |     career_path_id: Optional[int] = None
354 |     skill_id: Optional[int] = None
355 |     min_proficiency: Optional[int] = Field(None, ge=1, le=5)
356 | 
357 | 
358 | class CareerPathSkillRequirementRead(CareerPathSkillRequirementBase):
359 |     """Full CareerPathSkillRequirement response including id and timestamps."""
360 | 
361 |     model_config = ConfigDict(from_attributes=True)
362 | 
363 |     id: int
364 |     created_at: datetime
365 |     updated_at: datetime
366 | 
367 | 
368 | # ---------------------------------------------------------------------------
369 | # LearningResource
370 | # ---------------------------------------------------------------------------
371 | 
372 | 
373 | class LearningResourceBase(BaseModel):
374 |     """Shared fields for LearningResource."""
375 | 
376 |     skill_id: int
377 |     title: str = Field(..., min_length=1, max_length=255)
378 |     type: LearningResourceType
379 |     url: Optional[str] = Field(None, max_length=500)
380 |     duration_hours: int = Field(..., gt=0)
381 | 
382 | 
383 | class LearningResourceCreate(LearningResourceBase):
384 |     """Fields required to create a LearningResource."""
385 | 
386 | 
387 | class LearningResourceUpdate(BaseModel):
388 |     """All fields optional for partial update of LearningResource."""
389 | 
390 |     skill_id: Optional[int] = None
391 |     title: Optional[str] = Field(None, min_length=1, max_length=255)
392 |     type: Optional[LearningResourceType] = None
393 |     url: Optional[str] = Field(None, max_length=500)
394 |     duration_hours: Optional[int] = Field(None, gt=0)
395 | 
396 | 
397 | class LearningResourceRead(LearningResourceBase):
398 |     """Full LearningResource response including id and timestamps."""
399 | 
400 |     model_config = ConfigDict(from_attributes=True)
401 | 
402 |     id: int
403 |     created_at: datetime
404 |     updated_at: datetime
405 | 
406 | 
407 | # ---------------------------------------------------------------------------
408 | # LearningEnrollment
409 | # ---------------------------------------------------------------------------
410 | 
411 | 
412 | class LearningEnrollmentBase(BaseModel):
413 |     """Shared fields for LearningEnrollment."""
414 | 
415 |     employee_id: int
416 |     resource_id: int
417 |     enrolled_at: datetime
418 |     completed_at: Optional[datetime] = None
419 |     status: EnrollmentStatus = EnrollmentStatus.ENROLLED
420 | 
421 | 
422 | class LearningEnrollmentCreate(LearningEnrollmentBase):
423 |     """Fields required to create a LearningEnrollment."""
424 | 
425 | 
426 | class LearningEnrollmentUpdate(BaseModel):
427 |     """All fields optional for partial update of LearningEnrollment."""
428 | 
429 |     employee_id: Optional[int] = None
430 |     resource_id: Optional[int] = None
431 |     enrolled_at: Optional[datetime] = None
432 |     completed_at: Optional[datetime] = None
433 |     status: Optional[EnrollmentStatus] = None
434 | 
435 | 
436 | class LearningEnrollmentRead(LearningEnrollmentBase):
437 |     """Full LearningEnrollment response including id and timestamps."""
438 | 
439 |     model_config = ConfigDict(from_attributes=True)
440 | 
441 |     id: int
442 |     created_at: datetime
443 |     updated_at: datetime
444 | 
445 | 
446 | 
447 | # ---------------------------------------------------------------------------
448 | # Analytics — Skill Gap Analysis
449 | # ---------------------------------------------------------------------------
450 | 
451 | 
452 | class RecommendedResourceRead(BaseModel):
453 |     """Minimal learning resource info for recommendations."""
454 |     model_config = ConfigDict(from_attributes=True)
455 |     
456 |     resource_id: int
457 |     title: str
458 |     type: LearningResourceType
459 |     duration_hours: int
460 | 
461 | 
462 | class SkillGapItem(BaseModel):
463 |     """Individual skill gap with recommendation."""
464 |     
465 |     skill_id: int
466 |     skill_name: str
467 |     current_proficiency: int  # 0-5, 0 means not possessed
468 |     required_proficiency: int  # 1-5
469 |     gap: int
470 |     is_critical: bool
471 |     recommended_resources: List[RecommendedResourceRead]
472 | 
473 | 
474 | class SkillGapAnalysisRead(BaseModel):
475 |     """Complete skill gap analysis for an employee."""
476 |     
477 |     employee_id: int
478 |     employee_name: str
479 |     current_role: str
480 |     business_unit_id: int
481 |     skill_gaps: List[SkillGapItem]
482 |     total_gaps: int
483 |     critical_gaps: int
</content>
</file>
<file><path>app/routers/analytics.py</path>
<content lines="1-185">
  1 | """Analytics router — intelligent endpoints reserved for IBM Bob.
  2 | 
  3 | This module is intentionally a stub. The following endpoints will be
  4 | implemented during the hackathon by IBM Bob:
  5 | 
  6 |   - GET /analytics/skill-gap/{employee_id}
  7 |   - GET /analytics/career-recommendations/{employee_id}
  8 |   - POST /analytics/trigger-bench-learning
  9 |   - GET /analytics/industry-trends/{business_unit_id}
 10 |   - GET /analytics/skill-heatmap
 11 | 
 12 | Until then, this router exposes a single health probe so the route is
 13 | registered and the smoke test can verify wiring.
 14 | """
 15 | 
 16 | import logging
 17 | from typing import Dict, List
 18 | 
 19 | from fastapi import APIRouter, Depends
 20 | from sqlalchemy.orm import Session
 21 | 
 22 | from app.database import get_db
 23 | from app.exceptions import NotFoundError, raise_http_from_app_exception
 24 | from app.models import (
 25 |     CareerPath,
 26 |     CareerPathSkillRequirement,
 27 |     Employee,
 28 |     EmployeeSkill,
 29 |     LearningResource,
 30 |     Skill,
 31 | )
 32 | from app.schemas import (
 33 |     RecommendedResourceRead,
 34 |     SkillGapAnalysisRead,
 35 |     SkillGapItem,
 36 | )
 37 | 
 38 | logger = logging.getLogger(__name__)
 39 | 
 40 | router = APIRouter(prefix="/analytics", tags=["analytics"])
 41 | 
 42 | 
 43 | @router.get("/health")
 44 | def analytics_health() -> dict[str, str]:
 45 |     """Health probe confirming the analytics router is mounted."""
 46 |     return {"status": "ok", "module": "analytics", "implemented": "pending-bob"}
 47 | 
 48 | 
 49 | @router.get("/skill-gap/{employee_id}", response_model=SkillGapAnalysisRead)
 50 | def get_skill_gap_analysis(
 51 |     employee_id: int, db: Session = Depends(get_db)
 52 | ) -> SkillGapAnalysisRead:
 53 |     """Analyze skill gaps for an employee based on career path requirements.
 54 |     
 55 |     Args:
 56 |         employee_id: Employee primary key
 57 |         db: Database session
 58 |         
 59 |     Returns:
 60 |         Skill gap analysis with recommendations
 61 |         
 62 |     Raises:
 63 |         HTTPException: 404 if employee not found
 64 |     """
 65 |     try:
 66 |         # Step 1: Fetch employee
 67 |         employee = db.query(Employee).filter(Employee.id == employee_id).first()
 68 |         if not employee:
 69 |             raise NotFoundError(
 70 |                 f"Employee with id {employee_id} not found",
 71 |                 {"employee_id": employee_id}
 72 |             )
 73 |         
 74 |         # Step 2: Build proficiency map for employee
 75 |         employee_skills = (
 76 |             db.query(EmployeeSkill)
 77 |             .filter(EmployeeSkill.employee_id == employee_id)
 78 |             .all()
 79 |         )
 80 |         proficiency_map: Dict[int, int] = {
 81 |             es.skill_id: es.proficiency for es in employee_skills
 82 |         }
 83 |         
 84 |         # Step 3: Find career paths from employee's current role
 85 |         career_paths = (
 86 |             db.query(CareerPath)
 87 |             .filter(
 88 |                 CareerPath.from_role == employee.role,
 89 |                 CareerPath.business_unit_id == employee.business_unit_id
 90 |             )
 91 |             .all()
 92 |         )
 93 |         
 94 |         # Step 4-7: Analyze skill gaps
 95 |         skill_gaps_dict: Dict[int, SkillGapItem] = {}
 96 |         
 97 |         for career_path in career_paths:
 98 |             requirements = (
 99 |                 db.query(CareerPathSkillRequirement)
100 |                 .filter(
101 |                     CareerPathSkillRequirement.career_path_id == career_path.id
102 |                 )
103 |                 .all()
104 |             )
105 |             
106 |             for req in requirements:
107 |                 current_prof = proficiency_map.get(req.skill_id, 0)
108 |                 gap = req.min_proficiency - current_prof
109 |                 
110 |                 if gap > 0:
111 |                     # Only process if not already in dict or if gap is larger
112 |                     if req.skill_id not in skill_gaps_dict:
113 |                         skill = (
114 |                             db.query(Skill)
115 |                             .filter(Skill.id == req.skill_id)
116 |                             .first()
117 |                         )
118 |                         
119 |                         # Fetch 1-3 learning resources for this skill
120 |                         resources = (
121 |                             db.query(LearningResource)
122 |                             .filter(LearningResource.skill_id == req.skill_id)
123 |                             .order_by(LearningResource.duration_hours)
124 |                             .limit(3)
125 |                             .all()
126 |                         )
127 |                         
128 |                         recommended = [
129 |                             RecommendedResourceRead(
130 |                                 resource_id=r.id,
131 |                                 title=r.title,
132 |                                 type=r.type,
133 |                                 duration_hours=r.duration_hours
134 |                             )
135 |                             for r in resources
136 |                         ]
137 |                         
138 |                         # Mark as critical if gap >= 3 or skill is emerging
139 |                         is_critical = gap >= 3 or skill.is_emerging
140 |                         
141 |                         skill_gaps_dict[req.skill_id] = SkillGapItem(
142 |                             skill_id=req.skill_id,
143 |                             skill_name=skill.name,
144 |                             current_proficiency=current_prof,
145 |                             required_proficiency=req.min_proficiency,
146 |                             gap=gap,
147 |                             is_critical=is_critical,
148 |                             recommended_resources=recommended
149 |                         )
150 |                     else:
151 |                         # Update if this requirement is higher
152 |                         existing = skill_gaps_dict[req.skill_id]
153 |                         if req.min_proficiency > existing.required_proficiency:
154 |                             new_gap = req.min_proficiency - current_prof
155 |                             skill = (
156 |                                 db.query(Skill)
157 |                                 .filter(Skill.id == req.skill_id)
158 |                                 .first()
159 |                             )
160 |                             is_critical = new_gap >= 3 or skill.is_emerging
161 |                             existing.required_proficiency = req.min_proficiency
162 |                             existing.gap = new_gap
163 |                             existing.is_critical = is_critical
164 |         
165 |         # Step 8: Build response
166 |         skill_gaps = list(skill_gaps_dict.values())
167 |         critical_gaps = sum(1 for gap in skill_gaps if gap.is_critical)
168 |         
169 |         logger.info(
170 |             "Skill gap analysis completed for employee_id=%d, gaps=%d",
171 |             employee_id, len(skill_gaps)
172 |         )
173 |         
174 |         return SkillGapAnalysisRead(
175 |             employee_id=employee.id,
176 |             employee_name=employee.name,
177 |             current_role=employee.role,
178 |             business_unit_id=employee.business_unit_id,
179 |             skill_gaps=skill_gaps,
180 |             total_gaps=len(skill_gaps),
181 |             critical_gaps=critical_gaps
182 |         )
183 |         
184 |     except NotFoundError as exc:
185 |         raise_http_from_app_exception(exc)
</content>
</file>
<file><path>tests/test_analytics.py</path>
<content lines="1-140">
  1 | """Tests for analytics endpoints.
  2 | 
  3 | Tests cover skill gap analysis, industry trends, skill heatmap,
  4 | career recommendations, and bench learning trigger functionality.
  5 | """
  6 | 
  7 | import pytest
  8 | from fastapi.testclient import TestClient
  9 | 
 10 | 
 11 | # ---------------------------------------------------------------------------
 12 | # Endpoint 1: GET /analytics/skill-gap/{employee_id}
 13 | # ---------------------------------------------------------------------------
 14 | 
 15 | 
 16 | def test_skill_gap_analysis_for_employee_with_gaps(client: TestClient) -> None:
 17 |     """Test skill gap analysis for employee with career path requirements."""
 18 |     # Arrange: Use employee_id=1 from seeded data
 19 |     employee_id = 1
 20 |     
 21 |     # Act
 22 |     response = client.get(f"/analytics/skill-gap/{employee_id}")
 23 |     
 24 |     # Assert
 25 |     assert response.status_code == 200
 26 |     data = response.json()
 27 |     
 28 |     # Verify response structure
 29 |     assert "employee_id" in data
 30 |     assert "employee_name" in data
 31 |     assert "current_role" in data
 32 |     assert "business_unit_id" in data
 33 |     assert "skill_gaps" in data
 34 |     assert "total_gaps" in data
 35 |     assert "critical_gaps" in data
 36 |     
 37 |     # Verify data types and values
 38 |     assert data["employee_id"] == employee_id
 39 |     assert isinstance(data["employee_name"], str)
 40 |     assert isinstance(data["current_role"], str)
 41 |     assert isinstance(data["business_unit_id"], int)
 42 |     assert isinstance(data["skill_gaps"], list)
 43 |     assert isinstance(data["total_gaps"], int)
 44 |     assert isinstance(data["critical_gaps"], int)
 45 |     assert data["total_gaps"] >= 0
 46 |     assert data["critical_gaps"] >= 0
 47 |     assert data["critical_gaps"] <= data["total_gaps"]
 48 |     
 49 |     # Verify skill gap items structure if any exist
 50 |     if data["skill_gaps"]:
 51 |         gap_item = data["skill_gaps"][0]
 52 |         assert "skill_id" in gap_item
 53 |         assert "skill_name" in gap_item
 54 |         assert "current_proficiency" in gap_item
 55 |         assert "required_proficiency" in gap_item
 56 |         assert "gap" in gap_item
 57 |         assert "is_critical" in gap_item
 58 |         assert "recommended_resources" in gap_item
 59 |         
 60 |         # Verify proficiency values are in valid range
 61 |         assert 0 <= gap_item["current_proficiency"] <= 5
 62 |         assert 1 <= gap_item["required_proficiency"] <= 5
 63 |         assert gap_item["gap"] > 0
 64 |         assert isinstance(gap_item["is_critical"], bool)
 65 |         assert isinstance(gap_item["recommended_resources"], list)
 66 | 
 67 | 
 68 | def test_skill_gap_analysis_employee_not_found(client: TestClient) -> None:
 69 |     """Test skill gap analysis with non-existent employee."""
 70 |     # Arrange: Use non-existent employee_id
 71 |     employee_id = 99999
 72 |     
 73 |     # Act
 74 |     response = client.get(f"/analytics/skill-gap/{employee_id}")
 75 |     
 76 |     # Assert
 77 |     assert response.status_code == 404
 78 |     data = response.json()
 79 |     assert "detail" in data
 80 |     assert "message" in data["detail"]
 81 |     assert "Employee" in data["detail"]["message"]
 82 | 
 83 | 
 84 | def test_skill_gap_analysis_employee_with_no_career_paths(
 85 |     client: TestClient
 86 | ) -> None:
 87 |     """Test skill gap analysis for employee with no defined career paths."""
 88 |     # Arrange: Find an employee whose role has no career paths
 89 |     # First, get all employees
 90 |     employees_response = client.get("/employees/?limit=100")
 91 |     assert employees_response.status_code == 200
 92 |     employees = employees_response.json()
 93 |     
 94 |     # Get all career paths to find roles without paths
 95 |     paths_response = client.get("/career-paths/?limit=100")
 96 |     assert paths_response.status_code == 200
 97 |     paths = paths_response.json()
 98 |     
 99 |     # Collect roles that have career paths defined
100 |     roles_with_paths = set()
101 |     for path in paths:
102 |         roles_with_paths.add(path["from_role"])
103 |     
104 |     # Find an employee whose role is not in roles_with_paths
105 |     employee_without_path = None
106 |     for emp in employees:
107 |         if emp["role"] not in roles_with_paths:
108 |             employee_without_path = emp
109 |             break
110 |     
111 |     # If all employees have career paths, create a test employee without one
112 |     if employee_without_path is None:
113 |         # Get a valid business_unit_id
114 |         bu_id = employees[0]["business_unit_id"]
115 |         payload = {
116 |             "name": "Test Employee No Path",
117 |             "email": "test.nopath.unique@example.com",
118 |             "role": "Unique Role With No Path",
119 |             "band": "B1",
120 |             "business_unit_id": bu_id,
121 |             "line_manager_id": None,
122 |             "current_status": "ACTIVE",
123 |             "hire_date": "2024-01-01",
124 |         }
125 |         create_response = client.post("/employees/", json=payload)
126 |         assert create_response.status_code == 201
127 |         employee_without_path = create_response.json()
128 |     
129 |     # Act
130 |     response = client.get(f"/analytics/skill-gap/{employee_without_path['id']}")
131 |     
132 |     # Assert
133 |     assert response.status_code == 200
134 |     data = response.json()
135 |     assert data["employee_id"] == employee_without_path["id"]
136 |     assert data["total_gaps"] == 0
137 |     assert data["critical_gaps"] == 0
138 |     assert data["skill_gaps"] == []
139 | 
140 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
demo-script.md

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:29:08.450Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.03

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[ ] Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py
[ ] Implement GET /analytics/industry-trends/{business_unit_id} endpoint
[ ] Add three new tests to tests/test_analytics.py
[ ] Run pytest -v to verify all 27 tests pass
[ ] Verify app imports cleanly with python -c "from app.main import app"
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
demo-script.md

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:29:14.996Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.08

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Pending |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | Pending |
| 3 | Add three new tests to tests/test_analytics.py | Pending |
| 4 | Run pytest -v to verify all 27 tests pass | Pending |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll start implementing Endpoint 2. First, let me add the two new Pydantic schemas to `app/schemas.py`. I'll place them logically after the existing analytics schemas.

<apply_diff>
<path>app/schemas.py</path>
<diff>
<<<<<<< SEARCH
:start_line:474
-------
class SkillGapAnalysisRead(BaseModel):
    """Complete skill gap analysis for an employee."""
    
    employee_id: int
    employee_name: str
    current_role: str
    business_unit_id: int
    skill_gaps: List[SkillGapItem]
    total_gaps: int
    critical_gaps: int
=======
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
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'app/schemas.py'] Result:
<file_write_result>
<path>app/schemas.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
app/schemas.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
app/schemas.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:29:30.439Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.13

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Pending |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | Pending |
| 3 | Add three new tests to tests/test_analytics.py | Pending |
| 4 | Run pytest -v to verify all 27 tests pass | Pending |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py
[-] Implement GET /analytics/industry-trends/{business_unit_id} endpoint
[ ] Add three new tests to tests/test_analytics.py
[ ] Run pytest -v to verify all 27 tests pass
[ ] Verify app imports cleanly with python -c "from app.main import app"
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
app/schemas.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:29:35.206Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.18

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | In Progress |
| 3 | Add three new tests to tests/test_analytics.py | Pending |
| 4 | Run pytest -v to verify all 27 tests pass | Pending |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll implement the endpoint in `app/routers/analytics.py`. I need to add the necessary imports and the endpoint function following the algorithm from PLAN.md.

<apply_diff>
<path>app/routers/analytics.py</path>
<diff>
<<<<<<< SEARCH
:start_line:16
-------
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
=======
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
    SkillTrend,
)
from app.schemas import (
    IndustryTrendsRead,
    RecommendedResourceRead,
    SkillGapAnalysisRead,
    SkillGapItem,
    TrendingSkillItem,
)
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'app/routers/analytics.py'] Result:
<file_write_result>
<path>app/routers/analytics.py</path>
<operation>modified</operation>
<problems>

New problems detected after saving the file:
app/routers/analytics.py
- [basedpyright Error] 58 | ) -&gt; SkillGapAnalysisRead: : Function with declared return type "SkillGapAnalysisRead" must return value on all code paths
  "None" is not assignable to "SkillGapAnalysisRead"
- [basedpyright Error] 86 |         proficiency_map: Dict[int, int] = { : Type "dict[Column[int], Column[int]]" is not assignable to declared type "Dict[int, int]"
- [basedpyright Error] 113 |                 current_prof = proficiency_map.get(req.skill_id, 0) : No overloads for "get" match the provided arguments
- [basedpyright Error] 113 |                 current_prof = proficiency_map.get(req.skill_id, 0) : Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "get"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 136 |                                 resource_id=r.id, : Argument of type "Column[int]" cannot be assigned to parameter "resource_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 137 |                                 title=r.title, : Argument of type "Column[str]" cannot be assigned to parameter "title" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 138 |                                 type=r.type, : Argument of type "Column[str]" cannot be assigned to parameter "type" of type "LearningResourceType" in function "__init__"
  "Column[str]" is not assignable to "LearningResourceType"
- [basedpyright Error] 139 |                                 duration_hours=r.duration_hours : Argument of type "Column[int]" cannot be assigned to parameter "duration_hours" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 145 |                         is_critical = gap &gt;= 3 or skill.is_emerging : "is_emerging" is not a known attribute of "None"
- [basedpyright Error] 147 |                         skill_gaps_dict[req.skill_id] = SkillGapItem( : Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "__setitem__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 148 |                             skill_id=req.skill_id, : Argument of type "Column[int]" cannot be assigned to parameter "skill_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 149 |                             skill_name=skill.name, : Argument of type "Column[str]" cannot be assigned to parameter "skill_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 149 |                             skill_name=skill.name, : "name" is not a known attribute of "None"
- [basedpyright Error] 151 |                             required_proficiency=req.min_proficiency, : Argument of type "Column[int]" cannot be assigned to parameter "required_proficiency" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 153 |                             is_critical=is_critical, : Argument of type "Unknown | Column[bool]" cannot be assigned to parameter "is_critical" of type "bool" in function "__init__"
  Type "Unknown | Column[bool]" is not assignable to type "bool"
    "Column[bool]" is not assignable to "bool"
- [basedpyright Error] 158 |                         existing = skill_gaps_dict[req.skill_id] : Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "__getitem__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 159 |                         if req.min_proficiency &gt; existing.required_proficiency: : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 166 |                             is_critical = new_gap &gt;= 3 or skill.is_emerging : "is_emerging" is not a known attribute of "None"
- [basedpyright Error] 167 |                             existing.required_proficiency = req.min_proficiency : Cannot assign to attribute "required_proficiency" for class "SkillGapItem"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 169 |                             existing.is_critical = is_critical : Cannot assign to attribute "is_critical" for class "SkillGapItem"
  Type "Unknown | Column[bool]" is not assignable to type "bool"
    "Column[bool]" is not assignable to "bool"
- [basedpyright Error] 181 |             employee_id=employee.id, : Argument of type "Column[int]" cannot be assigned to parameter "employee_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 182 |             employee_name=employee.name, : Argument of type "Column[str]" cannot be assigned to parameter "employee_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 183 |             current_role=employee.role, : Argument of type "Column[str]" cannot be assigned to parameter "current_role" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 184 |             business_unit_id=employee.business_unit_id, : Argument of type "Column[int]" cannot be assigned to parameter "business_unit_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"</problems>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
app/routers/analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
app/routers/analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:29:45.180Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.24

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | In Progress |
| 3 | Add three new tests to tests/test_analytics.py | Pending |
| 4 | Run pytest -v to verify all 27 tests pass | Pending |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll add the industry trends endpoint implementation at the end of the file, after the skill-gap endpoint:

<apply_diff>
<path>app/routers/analytics.py</path>
<diff>
<<<<<<< SEARCH
:start_line:183
-------
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
=======
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
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'app/routers/analytics.py'] Result:
<file_write_result>
<path>app/routers/analytics.py</path>
<operation>modified</operation>
<problems>

New problems detected after saving the file:
app/routers/analytics.py
- [basedpyright Error] 203 | ) -&gt; IndustryTrendsRead: : Function with declared return type "IndustryTrendsRead" must return value on all code paths
  "None" is not assignable to "IndustryTrendsRead"
- [basedpyright Error] 279 |                     skill_id=skill.id, : Argument of type "Column[int]" cannot be assigned to parameter "skill_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 280 |                     skill_name=skill.name, : Argument of type "Column[str]" cannot be assigned to parameter "skill_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 281 |                     category=skill.category, : Argument of type "Column[str]" cannot be assigned to parameter "category" of type "SkillCategory" in function "__init__"
  "Column[str]" is not assignable to "SkillCategory"
- [basedpyright Error] 282 |                     is_emerging=skill.is_emerging, : Argument of type "Column[bool]" cannot be assigned to parameter "is_emerging" of type "bool" in function "__init__"
  "Column[bool]" is not assignable to "bool"
- [basedpyright Error] 283 |                     importance=ind_std.importance, : Argument of type "Column[int]" cannot be assigned to parameter "importance" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 284 |                     trend=ind_std.trend, : Argument of type "Column[str]" cannot be assigned to parameter "trend" of type "SkillTrend" in function "__init__"
  "Column[str]" is not assignable to "SkillTrend"
- [basedpyright Error] 300 |             1 for std in industry_standards if std.trend == SkillTrend.RISING : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 303 |             1 for std in industry_standards if std.trend == SkillTrend.STABLE : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 306 |             1 for std in industry_standards if std.trend == SkillTrend.DECLINING : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 315 |             business_unit_id=business_unit.id, : Argument of type "Column[int]" cannot be assigned to parameter "business_unit_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 316 |             business_unit_name=business_unit.name, : Argument of type "Column[str]" cannot be assigned to parameter "business_unit_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"</problems>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
app/routers/analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:30:07.456Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.30

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | In Progress |
| 3 | Add three new tests to tests/test_analytics.py | Pending |
| 4 | Run pytest -v to verify all 27 tests pass | Pending |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

The type errors are expected from the linter but won't affect runtime. Now let me add the three new tests to `tests/test_analytics.py`:

<insert_content>
<path>tests/test_analytics.py</path>
<line>0</line>
<content>


# ---------------------------------------------------------------------------
# Endpoint 2: GET /analytics/industry-trends/{business_unit_id}
# ---------------------------------------------------------------------------


def test_industry_trends_for_business_unit(client: TestClient) -> None:
    """Test industry trends for a business unit with seeded data."""
    # Arrange: Use business_unit_id=1 from seeded data
    business_unit_id = 1
    
    # Act
    response = client.get(f"/analytics/industry-trends/{business_unit_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "business_unit_id" in data
    assert "business_unit_name" in data
    assert "trending_skills" in data
    assert "total_skills" in data
    assert "rising_count" in data
    assert "stable_count" in data
    assert "declining_count" in data
    
    # Verify data types and values
    assert data["business_unit_id"] == business_unit_id
    assert isinstance(data["business_unit_name"], str)
    assert isinstance(data["trending_skills"], list)
    assert isinstance(data["total_skills"], int)
    assert isinstance(data["rising_count"], int)
    assert isinstance(data["stable_count"], int)
    assert isinstance(data["declining_count"], int)
    
    # Verify trend counts sum correctly
    assert (
        data["rising_count"] + data["stable_count"] + data["declining_count"]
        == data["total_skills"]
    )
    
    # Verify trending skills structure if any exist
    if data["trending_skills"]:
        skill_item = data["trending_skills"][0]
        assert "skill_id" in skill_item
        assert "skill_name" in skill_item
        assert "category" in skill_item
        assert "is_emerging" in skill_item
        assert "importance" in skill_item
        assert "trend" in skill_item
        assert "employee_count" in skill_item
        assert "avg_proficiency" in skill_item
        
        # Verify value ranges
        assert 1 <= skill_item["importance"] <= 5
        assert skill_item["trend"] in ["RISING", "STABLE", "DECLINING"]
        assert skill_item["employee_count"] >= 0
        assert 0.0 <= skill_item["avg_proficiency"] <= 5.0
        assert isinstance(skill_item["is_emerging"], bool)


def test_industry_trends_business_unit_not_found(client: TestClient) -> None:
    """Test industry trends with non-existent business unit."""
    # Arrange: Use non-existent business_unit_id
    business_unit_id = 99999
    
    # Act
    response = client.get(f"/analytics/industry-trends/{business_unit_id}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "BusinessUnit" in data["detail"]["message"]


def test_industry_trends_with_trend_filter_rising(client: TestClient) -> None:
    """Test industry trends with RISING trend filter."""
    # Arrange: Use business_unit_id=1 with trend_filter=RISING
    business_unit_id = 1
    
    # Act
    response = client.get(
        f"/analytics/industry-trends/{business_unit_id}?trend_filter=RISING"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify all returned skills have trend="RISING"
    for skill_item in data["trending_skills"]:
        assert skill_item["trend"] == "RISING"
    
    # Verify total_skills reflects the filtered count
    assert data["total_skills"] == data["rising_count"]

# Made with Bob
</content>
</insert_content>

---

**User:**

[insert_content for 'tests/test_analytics.py'] Result:
<file_write_result>
<path>tests/test_analytics.py</path>
<operation>modified</operation>
<user_edits>@@ -239,4 +239,4 @@
     # Verify total_skills reflects the filtered count
     assert data["total_skills"] == data["rising_count"]
 
-# Made with Bob
\ No newline at end of file
+# Made with Bob
</user_edits>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
<i>If the user's edits have addressed part of the task or changed the requirements, adjust your approach accordingly.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:30:23.848Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.37

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | In Progress |
| 3 | Add three new tests to tests/test_analytics.py | Pending |
| 4 | Run pytest -v to verify all 27 tests pass | Pending |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py
[x] Implement GET /analytics/industry-trends/{business_unit_id} endpoint
[x] Add three new tests to tests/test_analytics.py
[-] Run pytest -v to verify all 27 tests pass
[ ] Verify app imports cleanly with python -c "from app.main import app"
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:30:30.337Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.45

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | Completed |
| 3 | Add three new tests to tests/test_analytics.py | Completed |
| 4 | Run pytest -v to verify all 27 tests pass | In Progress |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me run the tests to verify all 27 tests pass:

<execute_command>
<command>cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && pytest -v</command>
</execute_command>

---

**User:**

[execute_command for 'cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && pytest -v'] Result:
Command executed in terminal  within working directory '/Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob'. Command execution was not successful, inspect the cause and adjust as needed.
Exit code: 127
Output:
/bin/sh: pytest: command not found

<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:30:35.956Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.52

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | Completed |
| 3 | Add three new tests to tests/test_analytics.py | Completed |
| 4 | Run pytest -v to verify all 27 tests pass | In Progress |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I need to activate the virtual environment first. Let me run the tests using the proper method:

<execute_command>
<command>cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && source .venv/bin/activate && pytest -v</command>
</execute_command>

---

**User:**

[execute_command for 'cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && source .venv/bin/activate && pytest -v'] Result:
Command executed in terminal  within working directory '/Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob'. Exit code: 0
Output:
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.3.4, pluggy-1.6.0 -- /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob
configfile: pyproject.toml
plugins: anyio-4.12.1
collecting ... collected 27 items

tests/test_analytics.py::test_skill_gap_analysis_for_employee_with_gaps PASSED [  3%]
tests/test_analytics.py::test_skill_gap_analysis_employee_not_found PASSED [  7%]
tests/test_analytics.py::test_skill_gap_analysis_employee_with_no_career_paths PASSED [ 11%]
tests/test_analytics.py::test_industry_trends_for_business_unit PASSED   [ 14%]
tests/test_analytics.py::test_industry_trends_business_unit_not_found PASSED [ 18%]
tests/test_analytics.py::test_industry_trends_with_trend_filter_rising PASSED [ 22%]
tests/test_smoke.py::test_health_endpoint PASSED                         [ 25%]
tests/test_smoke.py::test_root_redirects_to_dashboard PASSED             [ 29%]
tests/test_smoke.py::test_static_index_served PASSED                     [ 33%]
tests/test_smoke.py::test_analytics_router_is_mounted PASSED             [ 37%]
tests/test_smoke.py::test_list_business_units_returns_8 PASSED           [ 40%]
tests/test_smoke.py::test_list_employees_returns_30 PASSED               [ 44%]
tests/test_smoke.py::test_filter_employees_by_status_bench_returns_6 PASSED [ 48%]
tests/test_smoke.py::test_filter_employees_by_status_learning_returns_4 PASSED [ 51%]
tests/test_smoke.py::test_filter_employees_by_business_unit PASSED       [ 55%]
tests/test_smoke.py::test_get_employee_by_id_includes_line_manager_id PASSED [ 59%]
tests/test_smoke.py::test_get_nonexistent_employee_returns_404 PASSED    [ 62%]
tests/test_smoke.py::test_create_employee_then_delete PASSED             [ 66%]
tests/test_smoke.py::test_create_duplicate_email_returns_409 PASSED      [ 70%]
tests/test_smoke.py::test_list_projects_with_status_filter PASSED        [ 74%]
tests/test_smoke.py::test_list_skills_returns_50 PASSED                  [ 77%]
tests/test_smoke.py::test_emerging_skills_are_flagged_correctly PASSED   [ 81%]
tests/test_smoke.py::test_industry_standards_filtered_by_bu PASSED       [ 85%]
tests/test_smoke.py::test_career_paths_have_skill_requirements PASSED    [ 88%]
tests/test_smoke.py::test_employee_skills_proficiency_in_range_1_to_5 PASSED [ 92%]
tests/test_smoke.py::test_enrollments_only_for_bench_or_learning_employees PASSED [ 96%]
tests/test_smoke.py::test_pagination_skip_and_limit_work PASSED          [100%]

============================== 27 passed in 0.20s ==============================

<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:30:47.100Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.60

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | Completed |
| 3 | Add three new tests to tests/test_analytics.py | Completed |
| 4 | Run pytest -v to verify all 27 tests pass | In Progress |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! All 27 tests passed. Now let me verify the app imports cleanly:

<execute_command>
<command>cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && source .venv/bin/activate && python -c "from app.main import app"</command>
</execute_command>

---

**User:**

[execute_command for 'cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && source .venv/bin/activate && python -c "from app.main import app"'] Result:
Command executed in terminal  within working directory '/Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob'. Exit code: 0
Output:

<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:30:52.475Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.68

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | Completed |
| 3 | Add three new tests to tests/test_analytics.py | Completed |
| 4 | Run pytest -v to verify all 27 tests pass | In Progress |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py
[x] Implement GET /analytics/industry-trends/{business_unit_id} endpoint
[x] Add three new tests to tests/test_analytics.py
[x] Run pytest -v to verify all 27 tests pass
[x] Verify app imports cleanly with python -c "from app.main import app"
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T17:30:57.719Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.76

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .env
- .env.*
- secrets/
- *.key
- *.pem
- config/credentials.json
- node_modules/
- dist/
- build/
- .next/

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add TrendingSkillItem and IndustryTrendsRead schemas to app/schemas.py | Completed |
| 2 | Implement GET /analytics/industry-trends/{business_unit_id} endpoint | Completed |
| 3 | Add three new tests to tests/test_analytics.py | Completed |
| 4 | Run pytest -v to verify all 27 tests pass | Completed |
| 5 | Verify app imports cleanly with python -c "from app.main import app" | Completed |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
✅ Endpoint 2 implementation complete!

**Modified Files:**
1. `app/schemas.py` - Added `TrendingSkillItem` and `IndustryTrendsRead` schemas
2. `app/routers/analytics.py` - Implemented `GET /analytics/industry-trends/{business_unit_id}` endpoint
3. `tests/test_analytics.py` - Added 3 new tests for the endpoint

**Test Results:**
- All 27 tests passing (21 smoke + 3 skill-gap + 3 industry-trends)
- App imports cleanly with exit code 0

**Endpoint Features:**
- Fetches industry skill trends for a business unit
- Supports optional `trend_filter` query parameter (RISING/STABLE/DECLINING)
- Supports `limit` query parameter (default 20, max 100)
- Returns trending skills with employee counts and average proficiency
- Aggregates trend statistics (rising/stable/declining counts)
- Follows same exception handling pattern as Endpoint 1
- Sorts results by importance DESC, then by trend priority

**Tests Added:**
1. `test_industry_trends_for_business_unit` - Happy path with business_unit_id=1
2. `test_industry_trends_business_unit_not_found` - Error case with 404
3. `test_industry_trends_with_trend_filter_rising` - Edge case with RISING filter
</result>
</attempt_completion>

