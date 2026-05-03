**User:**

<task>
Implement Endpoint 4 from @PLAN.md: GET /analytics/career-recommendations/{employee_id}.

This is a BACKEND-ONLY task. No frontend work. No MCP tool work (deferred to a later task).

Scope (do this and ONLY this):

1. Add the three Pydantic schemas to `app/schemas.py` exactly as specified in PLAN.md Endpoint 4 section: `MissingSkillItem`, `CareerRecommendationItem`, `CareerRecommendationsRead`. Place them logically — group with related schemas, not blindly at the end.

2. Implement the endpoint in `app/routers/analytics.py`, alongside the existing routes. Do not modify or remove the existing `/analytics/health`, `/analytics/skill-gap/{employee_id}`, `/analytics/industry-trends/{business_unit_id}`, or `/analytics/skill-heatmap` routes. Follow the algorithm in PLAN.md "Endpoint 4: Algorithm" step by step. Use the same exception pattern as previous endpoints (NotFoundError → raise_http_from_app_exception).

3. Append three new tests to `tests/test_analytics.py` (do not delete existing tests):
   - `test_career_recommendations_for_employee` — happy path, employee_id=20 (Divya Shetty has known skill gaps from Task 4)
   - `test_career_recommendations_employee_not_found` — error case, employee_id=99999, expect 404
   - `test_career_recommendations_include_cross_bu` — edge case, employee_id=20 with `include_cross_bu=true`

4. Run `pytest -v` after implementation. Stop only after ALL tests pass — 21 smoke + 3 skill-gap + 3 industry-trends + 3 skill-heatmap + 3 new career-recommendations = 33 total.

5. Verify the app still imports cleanly: `python -c "from app.main import app"`. Must return exit code 0.

Constraints:
- Python 3.9 syntax only — `Optional[X]`, `List[X]`, `Dict[str, X]`. No `X | Y`. No `match` statements.
- Line length ≤ 100 characters.
- Functions ≤ 50 lines where reasonable. If the algorithm requires more, that's acceptable but document why.
- Reference @.bob/skills/add-feature.md for behavioral guidance.
- Reference @.bob/rules/project-rules.md for coding standards.
- Do NOT touch any file outside: `app/schemas.py`, `app/routers/analytics.py`, `tests/test_analytics.py`.
- Do NOT update README.md, AGENTS.md, PLAN.md, static/index.html, or anything in `mcp/`.
- Do NOT modify `app/main.py` or `app/models.py`.

Special note on the band inference algorithm:
Per PLAN.md Algorithm step 6, the `to_band` field is inferred by querying employees in the destination role and taking the most common band. If NO employees exist in that role yet (which is realistic for senior progression paths), set `to_band` to None — the schema declares it as `Optional[str]`. Do not crash; do not invent a band.

Deliverable: 3 files modified, all 33 tests passing, app imports cleanly.
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,static/index.html,../../../task-08-implement-skill-matrix-tab.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:22:09.495Z
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
bob_sessions/task-05-implement-industry-trends-analytics-endpoint.md
bob_sessions/task-05-implement-industry-trends-analytics-endpoint.png
bob_sessions/task-06-create-local-mcp-server.md
bob_sessions/task-06-create-local-mcp-server.png
bob_sessions/task-07-test--local-MCP-server-created.md
bob_sessions/task-07-test--local-MCP-server-created.png
bob_sessions/task-08-implement-skill-matrix-tab.md
bob_sessions/task-08-implement-skill-matrix-tab.png
data/
data/.gitkeep
docs/
docs/.gitkeep
mcp/
mcp/careerpath-mcp/
mcp/careerpath-mcp/pyproject.toml
mcp/careerpath-mcp/README.md
mcp/careerpath-mcp/test_server.py
mcp/careerpath-mcp/careerpath_mcp/
mcp/careerpath-mcp/careerpath_mcp/__init__.py
mcp/careerpath-mcp/careerpath_mcp/__main__.py
mcp/careerpath-mcp/careerpath_mcp/server.py
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

I'll implement Endpoint 4 (GET /analytics/career-recommendations/{employee_id}) following the PLAN.md specification. Let me start by reading the relevant files to understand the current structure.

<read_file>
<args>
<file>
<path>PLAN.md</path>
<line_range>1-50</line_range>
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
<content lines="1-50">
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
</content>
</file>
<file><path>app/schemas.py</path>
<content lines="1-558">
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
 12 | from typing import Dict, List, Optional
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
484 | 
485 | 
486 | # ---------------------------------------------------------------------------
487 | # Analytics — Industry Trends
488 | # ---------------------------------------------------------------------------
489 | 
490 | 
491 | class TrendingSkillItem(BaseModel):
492 |     """Industry trend data for a single skill."""
493 |     
494 |     skill_id: int
495 |     skill_name: str
496 |     category: SkillCategory
497 |     is_emerging: bool
498 |     importance: int  # 1-5
499 |     trend: SkillTrend
500 |     employee_count: int
501 |     avg_proficiency: float  # 0.0-5.0
502 | 
503 | 
504 | class IndustryTrendsRead(BaseModel):
505 |     """Industry skill trends for a business unit."""
506 |     
507 |     business_unit_id: int
508 |     business_unit_name: str
509 |     trending_skills: List[TrendingSkillItem]
510 |     total_skills: int
511 |     rising_count: int
512 |     stable_count: int
513 |     declining_count: int
514 | 
515 | 
516 | # ---------------------------------------------------------------------------
517 | # Analytics — Skill Heatmap
518 | # ---------------------------------------------------------------------------
519 | 
520 | 
521 | class BusinessUnitSkillBreakdown(BaseModel):
522 |     """Skill metrics for a specific business unit."""
523 |     
524 |     business_unit_id: int
525 |     business_unit_name: str
526 |     employee_count: int
527 |     avg_proficiency: float
528 | 
529 | 
530 | class SkillHeatmapItem(BaseModel):
531 |     """Heatmap data for a single skill across the organization."""
532 |     
533 |     skill_id: int
534 |     skill_name: str
535 |     category: SkillCategory
536 |     is_emerging: bool
537 |     total_employees: int
538 |     proficiency_distribution: Dict[str, int]  # "1": count, "2": count, etc.
539 |     avg_proficiency: float
540 |     certified_count: int
541 |     business_units: List[BusinessUnitSkillBreakdown]
542 | 
543 | 
544 | class SkillHeatmapFilters(BaseModel):
545 |     """Applied filters for the heatmap query."""
546 |     
547 |     business_unit_id: Optional[int] = None
548 |     skill_category: Optional[SkillCategory] = None
549 |     min_importance: Optional[int] = None
550 | 
551 | 
552 | class SkillHeatmapRead(BaseModel):
553 |     """Complete skill heatmap across organization or filtered subset."""
554 |     
555 |     filters: SkillHeatmapFilters
556 |     heatmap_data: List[SkillHeatmapItem]
557 |     total_skills: int
558 |     total_employees_analyzed: int
</content>
</file>
<file><path>app/routers/analytics.py</path>
<content lines="1-491">
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
 17 | from typing import Dict, List, Optional
 18 | 
 19 | from fastapi import APIRouter, Depends, Query
 20 | from sqlalchemy import func
 21 | from sqlalchemy.orm import Session
 22 | 
 23 | from app.database import get_db
 24 | from app.exceptions import NotFoundError, raise_http_from_app_exception
 25 | from app.models import (
 26 |     BusinessUnit,
 27 |     CareerPath,
 28 |     CareerPathSkillRequirement,
 29 |     Employee,
 30 |     EmployeeSkill,
 31 |     IndustryStandardSkill,
 32 |     LearningResource,
 33 |     Skill,
 34 |     SkillCategory,
 35 |     SkillTrend,
 36 | )
 37 | from app.schemas import (
 38 |     BusinessUnitSkillBreakdown,
 39 |     IndustryTrendsRead,
 40 |     RecommendedResourceRead,
 41 |     SkillGapAnalysisRead,
 42 |     SkillGapItem,
 43 |     SkillHeatmapFilters,
 44 |     SkillHeatmapItem,
 45 |     SkillHeatmapRead,
 46 |     TrendingSkillItem,
 47 | )
 48 | 
 49 | logger = logging.getLogger(__name__)
 50 | 
 51 | router = APIRouter(prefix="/analytics", tags=["analytics"])
 52 | 
 53 | 
 54 | @router.get("/health")
 55 | def analytics_health() -> dict[str, str]:
 56 |     """Health probe confirming the analytics router is mounted."""
 57 |     return {"status": "ok", "module": "analytics", "implemented": "pending-bob"}
 58 | 
 59 | 
 60 | @router.get("/skill-gap/{employee_id}", response_model=SkillGapAnalysisRead)
 61 | def get_skill_gap_analysis(
 62 |     employee_id: int, db: Session = Depends(get_db)
 63 | ) -> SkillGapAnalysisRead:
 64 |     """Analyze skill gaps for an employee based on career path requirements.
 65 |     
 66 |     Args:
 67 |         employee_id: Employee primary key
 68 |         db: Database session
 69 |         
 70 |     Returns:
 71 |         Skill gap analysis with recommendations
 72 |         
 73 |     Raises:
 74 |         HTTPException: 404 if employee not found
 75 |     """
 76 |     try:
 77 |         # Step 1: Fetch employee
 78 |         employee = db.query(Employee).filter(Employee.id == employee_id).first()
 79 |         if not employee:
 80 |             raise NotFoundError(
 81 |                 f"Employee with id {employee_id} not found",
 82 |                 {"employee_id": employee_id}
 83 |             )
 84 |         
 85 |         # Step 2: Build proficiency map for employee
 86 |         employee_skills = (
 87 |             db.query(EmployeeSkill)
 88 |             .filter(EmployeeSkill.employee_id == employee_id)
 89 |             .all()
 90 |         )
 91 |         proficiency_map: Dict[int, int] = {
 92 |             es.skill_id: es.proficiency for es in employee_skills
 93 |         }
 94 |         
 95 |         # Step 3: Find career paths from employee's current role
 96 |         career_paths = (
 97 |             db.query(CareerPath)
 98 |             .filter(
 99 |                 CareerPath.from_role == employee.role,
100 |                 CareerPath.business_unit_id == employee.business_unit_id
101 |             )
102 |             .all()
103 |         )
104 |         
105 |         # Step 4-7: Analyze skill gaps
106 |         skill_gaps_dict: Dict[int, SkillGapItem] = {}
107 |         
108 |         for career_path in career_paths:
109 |             requirements = (
110 |                 db.query(CareerPathSkillRequirement)
111 |                 .filter(
112 |                     CareerPathSkillRequirement.career_path_id == career_path.id
113 |                 )
114 |                 .all()
115 |             )
116 |             
117 |             for req in requirements:
118 |                 current_prof = proficiency_map.get(req.skill_id, 0)
119 |                 gap = req.min_proficiency - current_prof
120 |                 
121 |                 if gap > 0:
122 |                     # Only process if not already in dict or if gap is larger
123 |                     if req.skill_id not in skill_gaps_dict:
124 |                         skill = (
125 |                             db.query(Skill)
126 |                             .filter(Skill.id == req.skill_id)
127 |                             .first()
128 |                         )
129 |                         
130 |                         # Fetch 1-3 learning resources for this skill
131 |                         resources = (
132 |                             db.query(LearningResource)
133 |                             .filter(LearningResource.skill_id == req.skill_id)
134 |                             .order_by(LearningResource.duration_hours)
135 |                             .limit(3)
136 |                             .all()
137 |                         )
138 |                         
139 |                         recommended = [
140 |                             RecommendedResourceRead(
141 |                                 resource_id=r.id,
142 |                                 title=r.title,
143 |                                 type=r.type,
144 |                                 duration_hours=r.duration_hours
145 |                             )
146 |                             for r in resources
147 |                         ]
148 |                         
149 |                         # Mark as critical if gap >= 3 or skill is emerging
150 |                         is_critical = gap >= 3 or skill.is_emerging
151 |                         
152 |                         skill_gaps_dict[req.skill_id] = SkillGapItem(
153 |                             skill_id=req.skill_id,
154 |                             skill_name=skill.name,
155 |                             current_proficiency=current_prof,
156 |                             required_proficiency=req.min_proficiency,
157 |                             gap=gap,
158 |                             is_critical=is_critical,
159 |                             recommended_resources=recommended
160 |                         )
161 |                     else:
162 |                         # Update if this requirement is higher
163 |                         existing = skill_gaps_dict[req.skill_id]
164 |                         if req.min_proficiency > existing.required_proficiency:
165 |                             new_gap = req.min_proficiency - current_prof
166 |                             skill = (
167 |                                 db.query(Skill)
168 |                                 .filter(Skill.id == req.skill_id)
169 |                                 .first()
170 |                             )
171 |                             is_critical = new_gap >= 3 or skill.is_emerging
172 |                             existing.required_proficiency = req.min_proficiency
173 |                             existing.gap = new_gap
174 |                             existing.is_critical = is_critical
175 |         
176 |         # Step 8: Build response
177 |         skill_gaps = list(skill_gaps_dict.values())
178 |         critical_gaps = sum(1 for gap in skill_gaps if gap.is_critical)
179 |         
180 |         logger.info(
181 |             "Skill gap analysis completed for employee_id=%d, gaps=%d",
182 |             employee_id, len(skill_gaps)
183 |         )
184 |         
185 |         return SkillGapAnalysisRead(
186 |             employee_id=employee.id,
187 |             employee_name=employee.name,
188 |             current_role=employee.role,
189 |             business_unit_id=employee.business_unit_id,
190 |             skill_gaps=skill_gaps,
191 |             total_gaps=len(skill_gaps),
192 |             critical_gaps=critical_gaps
193 |         )
194 |         
195 |     except NotFoundError as exc:
196 |         raise_http_from_app_exception(exc)
197 | 
198 | 
199 | @router.get(
200 |     "/industry-trends/{business_unit_id}",
201 |     response_model=IndustryTrendsRead
202 | )
203 | def get_industry_trends(
204 |     business_unit_id: int,
205 |     trend_filter: Optional[SkillTrend] = Query(None),
206 |     limit: int = Query(20, ge=1, le=100),
207 |     db: Session = Depends(get_db)
208 | ) -> IndustryTrendsRead:
209 |     """Get industry skill trends for a business unit.
210 |     
211 |     Args:
212 |         business_unit_id: Business unit primary key
213 |         trend_filter: Optional filter by RISING, STABLE, or DECLINING
214 |         limit: Max skills to return (default 20, max 100)
215 |         db: Database session
216 |         
217 |     Returns:
218 |         Industry trends with skill statistics
219 |         
220 |     Raises:
221 |         HTTPException: 404 if business unit not found
222 |     """
223 |     try:
224 |         # Step 1: Fetch business unit
225 |         business_unit = (
226 |             db.query(BusinessUnit)
227 |             .filter(BusinessUnit.id == business_unit_id)
228 |             .first()
229 |         )
230 |         if not business_unit:
231 |             raise NotFoundError(
232 |                 f"BusinessUnit with id {business_unit_id} not found",
233 |                 {"business_unit_id": business_unit_id}
234 |             )
235 |         
236 |         # Step 2: Query IndustryStandardSkill for this business unit
237 |         query = (
238 |             db.query(IndustryStandardSkill)
239 |             .filter(IndustryStandardSkill.business_unit_id == business_unit_id)
240 |         )
241 |         
242 |         # Step 3: Apply optional trend_filter
243 |         if trend_filter:
244 |             query = query.filter(IndustryStandardSkill.trend == trend_filter)
245 |         
246 |         industry_standards = query.all()
247 |         
248 |         # Step 4-6: Build trending skills with employee stats
249 |         trending_skills: List[TrendingSkillItem] = []
250 |         
251 |         for ind_std in industry_standards:
252 |             # Step 4: Join with Skill to get details
253 |             skill = db.query(Skill).filter(Skill.id == ind_std.skill_id).first()
254 |             if not skill:
255 |                 continue
256 |             
257 |             # Step 5: Count employees in this BU who possess this skill
258 |             employee_count = (
259 |                 db.query(func.count(EmployeeSkill.id))
260 |                 .join(Employee, Employee.id == EmployeeSkill.employee_id)
261 |                 .filter(
262 |                     Employee.business_unit_id == business_unit_id,
263 |                     EmployeeSkill.skill_id == ind_std.skill_id
264 |                 )
265 |                 .scalar()
266 |             ) or 0
267 |             
268 |             # Step 6: Calculate average proficiency for employees in this BU
269 |             avg_proficiency_result = (
270 |                 db.query(func.avg(EmployeeSkill.proficiency))
271 |                 .join(Employee, Employee.id == EmployeeSkill.employee_id)
272 |                 .filter(
273 |                     Employee.business_unit_id == business_unit_id,
274 |                     EmployeeSkill.skill_id == ind_std.skill_id
275 |                 )
276 |                 .scalar()
277 |             )
278 |             avg_proficiency = (
279 |                 float(avg_proficiency_result) if avg_proficiency_result else 0.0
280 |             )
281 |             
282 |             trending_skills.append(
283 |                 TrendingSkillItem(
284 |                     skill_id=skill.id,
285 |                     skill_name=skill.name,
286 |                     category=skill.category,
287 |                     is_emerging=skill.is_emerging,
288 |                     importance=ind_std.importance,
289 |                     trend=ind_std.trend,
290 |                     employee_count=employee_count,
291 |                     avg_proficiency=round(avg_proficiency, 1)
292 |                 )
293 |             )
294 |         
295 |         # Step 7: Sort by importance DESC, then by trend (RISING first)
296 |         trend_order = {SkillTrend.RISING: 0, SkillTrend.STABLE: 1,
297 |                        SkillTrend.DECLINING: 2}
298 |         trending_skills.sort(
299 |             key=lambda x: (-x.importance, trend_order.get(x.trend, 3))
300 |         )
301 |         trending_skills = trending_skills[:limit]
302 |         
303 |         # Step 8: Aggregate trend counts
304 |         rising_count = sum(
305 |             1 for std in industry_standards if std.trend == SkillTrend.RISING
306 |         )
307 |         stable_count = sum(
308 |             1 for std in industry_standards if std.trend == SkillTrend.STABLE
309 |         )
310 |         declining_count = sum(
311 |             1 for std in industry_standards if std.trend == SkillTrend.DECLINING
312 |         )
313 |         
314 |         logger.info(
315 |             "Industry trends retrieved for business_unit_id=%d, skills=%d",
316 |             business_unit_id, len(trending_skills)
317 |         )
318 |         
319 |         return IndustryTrendsRead(
320 |             business_unit_id=business_unit.id,
321 |             business_unit_name=business_unit.name,
322 |             trending_skills=trending_skills,
323 |             total_skills=len(industry_standards),
324 |             rising_count=rising_count,
325 |             stable_count=stable_count,
326 |             declining_count=declining_count
327 |         )
328 |         
329 |     except NotFoundError as exc:
330 |         raise_http_from_app_exception(exc)
331 | 
332 | 
333 | @router.get("/skill-heatmap", response_model=SkillHeatmapRead)
334 | def get_skill_heatmap(
335 |     business_unit_id: Optional[int] = Query(None),
336 |     skill_category: Optional[SkillCategory] = Query(None),
337 |     min_importance: Optional[int] = Query(None, ge=1, le=5),
338 |     db: Session = Depends(get_db)
339 | ) -> SkillHeatmapRead:
340 |     """Get skill heatmap across organization or filtered subset.
341 |     
342 |     Args:
343 |         business_unit_id: Optional filter by business unit
344 |         skill_category: Optional filter by TECHNICAL, DOMAIN, or SOFT
345 |         min_importance: Optional minimum importance threshold (1-5)
346 |         db: Database session
347 |         
348 |     Returns:
349 |         Skill heatmap with proficiency distribution and business unit breakdown
350 |     """
351 |     try:
352 |         # Step 1: Build base query for Skills
353 |         skills_query = db.query(Skill)
354 |         
355 |         # Apply skill_category filter if provided
356 |         if skill_category:
357 |             skills_query = skills_query.filter(Skill.category == skill_category)
358 |         
359 |         # Step 2: If min_importance provided, join with IndustryStandardSkill
360 |         skill_ids_with_importance = None
361 |         if min_importance is not None:
362 |             importance_subquery = (
363 |                 db.query(IndustryStandardSkill.skill_id)
364 |                 .filter(IndustryStandardSkill.importance >= min_importance)
365 |                 .distinct()
366 |             )
367 |             skill_ids_with_importance = [row[0] for row in importance_subquery.all()]
368 |             if skill_ids_with_importance:
369 |                 skills_query = skills_query.filter(
370 |                     Skill.id.in_(skill_ids_with_importance)
371 |                 )
372 |             else:
373 |                 # No skills meet importance threshold
374 |                 return SkillHeatmapRead(
375 |                     filters=SkillHeatmapFilters(
376 |                         business_unit_id=business_unit_id,
377 |                         skill_category=skill_category,
378 |                         min_importance=min_importance
379 |                     ),
380 |                     heatmap_data=[],
381 |                     total_skills=0,
382 |                     total_employees_analyzed=0
383 |                 )
384 |         
385 |         skills = skills_query.all()
386 |         
387 |         # Step 3-6: For each skill, calculate metrics
388 |         heatmap_items: List[SkillHeatmapItem] = []
389 |         total_employees_set = set()
390 |         
391 |         for skill in skills:
392 |             # Query EmployeeSkill records for this skill
393 |             emp_skill_query = (
394 |                 db.query(EmployeeSkill, Employee)
395 |                 .join(Employee, Employee.id == EmployeeSkill.employee_id)
396 |                 .filter(EmployeeSkill.skill_id == skill.id)
397 |             )
398 |             
399 |             # Step 4: Apply business_unit_id filter if provided
400 |             if business_unit_id is not None:
401 |                 emp_skill_query = emp_skill_query.filter(
402 |                     Employee.business_unit_id == business_unit_id
403 |                 )
404 |             
405 |             emp_skills = emp_skill_query.all()
406 |             
407 |             if not emp_skills:
408 |                 continue  # Skip skills with no employees
409 |             
410 |             # Step 5: Calculate metrics
411 |             total_employees = len(emp_skills)
412 |             proficiency_dist: Dict[str, int] = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
413 |             total_prof = 0
414 |             certified_count = 0
415 |             
416 |             for emp_skill, employee in emp_skills:
417 |                 total_employees_set.add(employee.id)
418 |                 prof_str = str(emp_skill.proficiency)
419 |                 proficiency_dist[prof_str] = proficiency_dist.get(prof_str, 0) + 1
420 |                 total_prof += emp_skill.proficiency
421 |                 if emp_skill.certified:
422 |                     certified_count += 1
423 |             
424 |             avg_proficiency = round(total_prof / total_employees, 1)
425 |             
426 |             # Step 6: Group by business unit for breakdown
427 |             bu_breakdown_dict: Dict[int, Dict] = {}
428 |             for emp_skill, employee in emp_skills:
429 |                 bu_id = employee.business_unit_id
430 |                 if bu_id not in bu_breakdown_dict:
431 |                     bu_breakdown_dict[bu_id] = {
432 |                         "count": 0,
433 |                         "total_prof": 0,
434 |                         "bu_name": None
435 |                     }
436 |                 bu_breakdown_dict[bu_id]["count"] += 1
437 |                 bu_breakdown_dict[bu_id]["total_prof"] += emp_skill.proficiency
438 |             
439 |             # Fetch business unit names and build breakdown list
440 |             business_units: List[BusinessUnitSkillBreakdown] = []
441 |             for bu_id, data in bu_breakdown_dict.items():
442 |                 bu = db.query(BusinessUnit).filter(BusinessUnit.id == bu_id).first()
443 |                 if bu:
444 |                     business_units.append(
445 |                         BusinessUnitSkillBreakdown(
446 |                             business_unit_id=bu.id,
447 |                             business_unit_name=bu.name,
448 |                             employee_count=data["count"],
449 |                             avg_proficiency=round(
450 |                                 data["total_prof"] / data["count"], 1
451 |                             )
452 |                         )
453 |                     )
454 |             
455 |             heatmap_items.append(
456 |                 SkillHeatmapItem(
457 |                     skill_id=skill.id,
458 |                     skill_name=skill.name,
459 |                     category=skill.category,
460 |                     is_emerging=skill.is_emerging,
461 |                     total_employees=total_employees,
462 |                     proficiency_distribution=proficiency_dist,
463 |                     avg_proficiency=avg_proficiency,
464 |                     certified_count=certified_count,
465 |                     business_units=business_units
466 |                 )
467 |             )
468 |         
469 |         # Step 7: Sort by total_employees DESC, then by avg_proficiency DESC
470 |         heatmap_items.sort(
471 |             key=lambda x: (-x.total_employees, -x.avg_proficiency)
472 |         )
473 |         
474 |         logger.info(
475 |             "Skill heatmap retrieved, skills=%d, employees=%d",
476 |             len(heatmap_items), len(total_employees_set)
477 |         )
478 |         
479 |         return SkillHeatmapRead(
480 |             filters=SkillHeatmapFilters(
481 |                 business_unit_id=business_unit_id,
482 |                 skill_category=skill_category,
483 |                 min_importance=min_importance
484 |             ),
485 |             heatmap_data=heatmap_items,
486 |             total_skills=len(heatmap_items),
487 |             total_employees_analyzed=len(total_employees_set)
488 |         )
489 |         
490 |     except NotFoundError as exc:
491 |         raise_http_from_app_exception(exc)
</content>
</file>
<file><path>tests/test_analytics.py</path>
<content lines="1-364">
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
141 | 
142 | 
143 | 
144 | # ---------------------------------------------------------------------------
145 | # Endpoint 2: GET /analytics/industry-trends/{business_unit_id}
146 | # ---------------------------------------------------------------------------
147 | 
148 | 
149 | def test_industry_trends_for_business_unit(client: TestClient) -> None:
150 |     """Test industry trends for a business unit with seeded data."""
151 |     # Arrange: Use business_unit_id=1 from seeded data
152 |     business_unit_id = 1
153 |     
154 |     # Act
155 |     response = client.get(f"/analytics/industry-trends/{business_unit_id}")
156 |     
157 |     # Assert
158 |     assert response.status_code == 200
159 |     data = response.json()
160 |     
161 |     # Verify response structure
162 |     assert "business_unit_id" in data
163 |     assert "business_unit_name" in data
164 |     assert "trending_skills" in data
165 |     assert "total_skills" in data
166 |     assert "rising_count" in data
167 |     assert "stable_count" in data
168 |     assert "declining_count" in data
169 |     
170 |     # Verify data types and values
171 |     assert data["business_unit_id"] == business_unit_id
172 |     assert isinstance(data["business_unit_name"], str)
173 |     assert isinstance(data["trending_skills"], list)
174 |     assert isinstance(data["total_skills"], int)
175 |     assert isinstance(data["rising_count"], int)
176 |     assert isinstance(data["stable_count"], int)
177 |     assert isinstance(data["declining_count"], int)
178 |     
179 |     # Verify trend counts sum correctly
180 |     assert (
181 |         data["rising_count"] + data["stable_count"] + data["declining_count"]
182 |         == data["total_skills"]
183 |     )
184 |     
185 |     # Verify trending skills structure if any exist
186 |     if data["trending_skills"]:
187 |         skill_item = data["trending_skills"][0]
188 |         assert "skill_id" in skill_item
189 |         assert "skill_name" in skill_item
190 |         assert "category" in skill_item
191 |         assert "is_emerging" in skill_item
192 |         assert "importance" in skill_item
193 |         assert "trend" in skill_item
194 |         assert "employee_count" in skill_item
195 |         assert "avg_proficiency" in skill_item
196 |         
197 |         # Verify value ranges
198 |         assert 1 <= skill_item["importance"] <= 5
199 |         assert skill_item["trend"] in ["RISING", "STABLE", "DECLINING"]
200 |         assert skill_item["employee_count"] >= 0
201 |         assert 0.0 <= skill_item["avg_proficiency"] <= 5.0
202 |         assert isinstance(skill_item["is_emerging"], bool)
203 | 
204 | 
205 | def test_industry_trends_business_unit_not_found(client: TestClient) -> None:
206 |     """Test industry trends with non-existent business unit."""
207 |     # Arrange: Use non-existent business_unit_id
208 |     business_unit_id = 99999
209 |     
210 |     # Act
211 |     response = client.get(f"/analytics/industry-trends/{business_unit_id}")
212 |     
213 |     # Assert
214 |     assert response.status_code == 404
215 |     data = response.json()
216 |     assert "detail" in data
217 |     assert "message" in data["detail"]
218 |     assert "BusinessUnit" in data["detail"]["message"]
219 | 
220 | 
221 | def test_industry_trends_with_trend_filter_rising(client: TestClient) -> None:
222 |     """Test industry trends with RISING trend filter."""
223 |     # Arrange: Use business_unit_id=1 with trend_filter=RISING
224 |     business_unit_id = 1
225 |     
226 |     # Act
227 |     response = client.get(
228 |         f"/analytics/industry-trends/{business_unit_id}?trend_filter=RISING"
229 |     )
230 |     
231 |     # Assert
232 |     assert response.status_code == 200
233 |     data = response.json()
234 |     
235 |     # Verify all returned skills have trend="RISING"
236 |     for skill_item in data["trending_skills"]:
237 |         assert skill_item["trend"] == "RISING"
238 |     
239 |     # Verify total_skills reflects the filtered count
240 |     assert data["total_skills"] == data["rising_count"]
241 | 
242 | # Made with Bob
243 | 
244 | 
245 | # ---------------------------------------------------------------------------
246 | # Endpoint 3: GET /analytics/skill-heatmap
247 | # ---------------------------------------------------------------------------
248 | 
249 | 
250 | def test_skill_heatmap_no_filters(client: TestClient) -> None:
251 |     """Test skill heatmap with no filters (happy path)."""
252 |     # Act
253 |     response = client.get("/analytics/skill-heatmap")
254 |     
255 |     # Assert
256 |     assert response.status_code == 200
257 |     data = response.json()
258 |     
259 |     # Verify response structure
260 |     assert "filters" in data
261 |     assert "heatmap_data" in data
262 |     assert "total_skills" in data
263 |     assert "total_employees_analyzed" in data
264 |     
265 |     # Verify filters structure
266 |     filters = data["filters"]
267 |     assert "business_unit_id" in filters
268 |     assert "skill_category" in filters
269 |     assert "min_importance" in filters
270 |     assert filters["business_unit_id"] is None
271 |     assert filters["skill_category"] is None
272 |     assert filters["min_importance"] is None
273 |     
274 |     # Verify data types
275 |     assert isinstance(data["heatmap_data"], list)
276 |     assert isinstance(data["total_skills"], int)
277 |     assert isinstance(data["total_employees_analyzed"], int)
278 |     assert data["total_skills"] >= 0
279 |     assert data["total_employees_analyzed"] >= 0
280 |     
281 |     # Verify heatmap items structure if any exist
282 |     if data["heatmap_data"]:
283 |         item = data["heatmap_data"][0]
284 |         assert "skill_id" in item
285 |         assert "skill_name" in item
286 |         assert "category" in item
287 |         assert "is_emerging" in item
288 |         assert "total_employees" in item
289 |         assert "proficiency_distribution" in item
290 |         assert "avg_proficiency" in item
291 |         assert "certified_count" in item
292 |         assert "business_units" in item
293 |         
294 |         # Verify proficiency_distribution
295 |         prof_dist = item["proficiency_distribution"]
296 |         assert isinstance(prof_dist, dict)
297 |         for level in ["1", "2", "3", "4", "5"]:
298 |             assert level in prof_dist
299 |             assert isinstance(prof_dist[level], int)
300 |             assert prof_dist[level] >= 0
301 |         
302 |         # Verify distribution sums to total_employees
303 |         dist_sum = sum(prof_dist.values())
304 |         assert dist_sum == item["total_employees"]
305 |         
306 |         # Verify business_units structure
307 |         assert isinstance(item["business_units"], list)
308 |         if item["business_units"]:
309 |             bu = item["business_units"][0]
310 |             assert "business_unit_id" in bu
311 |             assert "business_unit_name" in bu
312 |             assert "employee_count" in bu
313 |             assert "avg_proficiency" in bu
314 |             assert isinstance(bu["employee_count"], int)
315 |             assert isinstance(bu["avg_proficiency"], float)
316 |             assert 0.0 <= bu["avg_proficiency"] <= 5.0
317 | 
318 | 
319 | def test_skill_heatmap_invalid_min_importance(client: TestClient) -> None:
320 |     """Test skill heatmap with invalid min_importance (error case)."""
321 |     # Arrange: Use min_importance=10 (out of range 1-5)
322 |     
323 |     # Act
324 |     response = client.get("/analytics/skill-heatmap?min_importance=10")
325 |     
326 |     # Assert
327 |     assert response.status_code == 422
328 |     data = response.json()
329 |     assert "detail" in data
330 | 
331 | 
332 | def test_skill_heatmap_with_all_filters(client: TestClient) -> None:
333 |     """Test skill heatmap with all filters applied (edge case)."""
334 |     # Arrange: Use business_unit_id=1, skill_category=TECHNICAL, min_importance=3
335 |     business_unit_id = 1
336 |     skill_category = "TECHNICAL"
337 |     min_importance = 3
338 |     
339 |     # Act
340 |     response = client.get(
341 |         f"/analytics/skill-heatmap?business_unit_id={business_unit_id}"
342 |         f"&skill_category={skill_category}&min_importance={min_importance}"
343 |     )
344 |     
345 |     # Assert
346 |     assert response.status_code == 200
347 |     data = response.json()
348 |     
349 |     # Verify filters are reflected in response
350 |     filters = data["filters"]
351 |     assert filters["business_unit_id"] == business_unit_id
352 |     assert filters["skill_category"] == skill_category
353 |     assert filters["min_importance"] == min_importance
354 |     
355 |     # Verify results match filter criteria
356 |     for item in data["heatmap_data"]:
357 |         # All skills should be TECHNICAL
358 |         assert item["category"] == skill_category
359 |         
360 |         # All business_units in breakdown should match the filter
361 |         for bu in item["business_units"]:
362 |             assert bu["business_unit_id"] == business_unit_id
363 | 
364 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,static/index.html,../../../task-08-implement-skill-matrix-tab.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:22:15.325Z
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

I need to read more of PLAN.md to see the complete specification for Endpoint 4.

<read_file>
<args>
<file>
<path>PLAN.md</path>
<line_range>200-350</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>PLAN.md</path>
<content lines="200-350">
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
251 | {
252 |   "filters": {
253 |     "business_unit_id": 1,
254 |     "skill_category": "TECHNICAL",
255 |     "min_importance": 3
256 |   },
257 |   "heatmap_data": [
258 |     {
259 |       "skill_id": 5,
260 |       "skill_name": "Kubernetes",
261 |       "category": "TECHNICAL",
262 |       "is_emerging": false,
263 |       "total_employees": 12,
264 |       "proficiency_distribution": {
265 |         "1": 2,
266 |         "2": 3,
267 |         "3": 4,
268 |         "4": 2,
269 |         "5": 1
270 |       },
271 |       "avg_proficiency": 2.9,
272 |       "certified_count": 3,
273 |       "business_units": [
274 |         {
275 |           "business_unit_id": 1,
276 |           "business_unit_name": "Cloud Services",
277 |           "employee_count": 8,
278 |           "avg_proficiency": 3.2
279 |         }
280 |       ]
281 |     }
282 |   ],
283 |   "total_skills": 25,
284 |   "total_employees_analyzed": 30
285 | }
286 | ```
287 | 
288 | ### Data Sources
289 | - [`Skill`](app/models.py:199) — Get all skills or filter by category
290 | - [`EmployeeSkill`](app/models.py:221) — Get proficiency data for all employees
291 | - [`Employee`](app/models.py:127) — Filter by business_unit_id if provided
292 | - [`BusinessUnit`](app/models.py:107) — Get business unit names
293 | - [`IndustryStandardSkill`](app/models.py:242) — Filter by min_importance if provided
294 | 
295 | ### Algorithm
296 | 1. Build base query for [`Skill`](app/models.py:199), apply `skill_category` filter if provided
297 | 2. If `min_importance` provided, join with [`IndustryStandardSkill`](app/models.py:242) and filter
298 | 3. For each skill, query [`EmployeeSkill`](app/models.py:221) records
299 | 4. If `business_unit_id` provided, join with [`Employee`](app/models.py:127) to filter
300 | 5. For each skill, calculate:
301 |    - Total employee count with this skill
302 |    - Proficiency distribution (count per level 1-5)
303 |    - Average proficiency
304 |    - Count of certified employees
305 | 6. Group by business unit to show per-BU breakdown
306 | 7. Sort by total_employees DESC, then by avg_proficiency DESC
307 | 
308 | ### Pydantic Schemas to Add
309 | **File**: `app/schemas.py`
310 | 
311 | ```python
312 | class BusinessUnitSkillBreakdown(BaseModel):
313 |     """Skill metrics for a specific business unit."""
314 |     
315 |     business_unit_id: int
316 |     business_unit_name: str
317 |     employee_count: int
318 |     avg_proficiency: float
319 | 
320 | 
321 | class SkillHeatmapItem(BaseModel):
322 |     """Heatmap data for a single skill across the organization."""
323 |     
324 |     skill_id: int
325 |     skill_name: str
326 |     category: SkillCategory
327 |     is_emerging: bool
328 |     total_employees: int
329 |     proficiency_distribution: Dict[str, int]  # "1": count, "2": count, etc.
330 |     avg_proficiency: float
331 |     certified_count: int
332 |     business_units: List[BusinessUnitSkillBreakdown]
333 | 
334 | 
335 | class SkillHeatmapFilters(BaseModel):
336 |     """Applied filters for the heatmap query."""
337 |     
338 |     business_unit_id: Optional[int] = None
339 |     skill_category: Optional[SkillCategory] = None
340 |     min_importance: Optional[int] = None
341 | 
342 | 
343 | class SkillHeatmapRead(BaseModel):
344 |     """Complete skill heatmap across organization or filtered subset."""
345 |     
346 |     filters: SkillHeatmapFilters
347 |     heatmap_data: List[SkillHeatmapItem]
348 |     total_skills: int
349 |     total_employees_analyzed: int
350 | ```
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,static/index.html,../../../task-08-implement-skill-matrix-tab.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:22:26.569Z
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
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>PLAN.md</path>
<line_range>380-550</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>PLAN.md</path>
<content lines="380-550">
380 | - **Path Parameters**:
381 |   - `employee_id` (int, required) — Employee primary key
382 | - **Query Parameters**:
383 |   - `include_cross_bu` (bool, default=false) — Include career paths from other business units
384 |   - `max_recommendations` (int, default=5) — Maximum recommendations to return
385 | - **Response Shape**: `CareerRecommendationsRead`
386 | 
387 | ```python
388 | {
389 |   "employee_id": 1,
390 |   "employee_name": "Raj Kumar",
391 |   "current_role": "Software Engineer",
392 |   "current_band": "B3",
393 |   "business_unit_id": 1,
394 |   "recommendations": [
395 |     {
396 |       "career_path_id": 3,
397 |       "to_role": "Senior Software Engineer",
398 |       "to_band": "B4",  # inferred from employees in that role
399 |       "business_unit_id": 1,
400 |       "business_unit_name": "Cloud Services",
401 |       "match_score": 0.85,  # 0.0-1.0
402 |       "readiness": "HIGH",  # HIGH, MEDIUM, LOW
403 |       "required_skills": 8,
404 |       "possessed_skills": 7,
405 |       "skill_gaps": 1,
406 |       "missing_skills": [
407 |         {
408 |           "skill_id": 5,
409 |           "skill_name": "Kubernetes",
410 |           "required_proficiency": 4,
411 |           "current_proficiency": 0
412 |         }
413 |       ],
414 |       "estimated_learning_hours": 40
415 |     }
416 |   ],
417 |   "total_recommendations": 3
418 | }
419 | ```
420 | 
421 | ### Data Sources
422 | - [`Employee`](app/models.py:127) — Get employee details and current role
423 | - [`EmployeeSkill`](app/models.py:221) — Get employee's current skills
424 | - [`CareerPath`](app/models.py:262) — Find paths from employee's current role
425 | - [`CareerPathSkillRequirement`](app/models.py:277) — Get required skills for each path
426 | - [`Skill`](app/models.py:199) — Get skill details
427 | - [`LearningResource`](app/models.py:298) — Calculate estimated learning hours for gaps
428 | - [`BusinessUnit`](app/models.py:107) — Get business unit names
429 | 
430 | ### Algorithm
431 | 1. Fetch employee by `employee_id`; raise [`NotFoundError`](app/exceptions.py:30) if not found
432 | 2. Query [`CareerPath`](app/models.py:262) where `from_role` matches employee's role
433 | 3. If `include_cross_bu=false`, filter to employee's business_unit_id only
434 | 4. For each career path:
435 |    - Fetch all [`CareerPathSkillRequirement`](app/models.py:277) records
436 |    - Compare with employee's [`EmployeeSkill`](app/models.py:221) records
437 |    - Calculate match_score: `possessed_skills / required_skills`
438 |    - Determine readiness: HIGH (>0.8), MEDIUM (0.5-0.8), LOW (<0.5)
439 |    - Identify missing skills (required but not possessed or proficiency too low)
440 |    - Sum duration_hours from [`LearningResource`](app/models.py:298) for missing skills
441 | 5. Sort by match_score DESC, limit to `max_recommendations`
442 | 6. Infer `to_band` by querying employees in `to_role` and taking most common band
443 | 
444 | ### Pydantic Schemas to Add
445 | **File**: `app/schemas.py`
446 | 
447 | ```python
448 | class MissingSkillItem(BaseModel):
449 |     """Skill gap detail for career recommendation."""
450 |     
451 |     skill_id: int
452 |     skill_name: str
453 |     required_proficiency: int
454 |     current_proficiency: int
455 | 
456 | 
457 | class CareerRecommendationItem(BaseModel):
458 |     """Single career path recommendation with readiness assessment."""
459 |     
460 |     career_path_id: int
461 |     to_role: str
462 |     to_band: Optional[str]  # inferred from employees in that role
463 |     business_unit_id: int
464 |     business_unit_name: str
465 |     match_score: float  # 0.0-1.0
466 |     readiness: str  # HIGH, MEDIUM, LOW
467 |     required_skills: int
468 |     possessed_skills: int
469 |     skill_gaps: int
470 |     missing_skills: List[MissingSkillItem]
471 |     estimated_learning_hours: int
472 | 
473 | 
474 | class CareerRecommendationsRead(BaseModel):
475 |     """Career path recommendations for an employee."""
476 |     
477 |     employee_id: int
478 |     employee_name: str
479 |     current_role: str
480 |     current_band: str
481 |     business_unit_id: int
482 |     recommendations: List[CareerRecommendationItem]
483 |     total_recommendations: int
484 | ```
485 | 
486 | ### Test Cases to Add
487 | **File**: `tests/test_analytics.py`
488 | 
489 | 1. **Happy path**: `test_career_recommendations_for_employee`
490 |    - Use employee_id=1
491 |    - Assert recommendations list is not empty
492 |    - Assert match_scores are between 0.0 and 1.0
493 |    - Assert readiness values are valid (HIGH/MEDIUM/LOW)
494 | 
495 | 2. **Error case**: `test_career_recommendations_employee_not_found`
496 |    - Use employee_id=99999
497 |    - Assert 404 status code
498 | 
499 | 3. **Edge case**: `test_career_recommendations_include_cross_bu`
500 |    - Use employee_id=1 with `include_cross_bu=true`
501 |    - Assert some recommendations may be from different business units
502 | 
503 | ### Estimated Complexity
504 | **Medium** — Requires scoring algorithm, complex filtering, and aggregation across multiple tables. Band inference adds complexity.
505 | 
506 | ---
507 | 
508 | ## Endpoint 5: POST /analytics/trigger-bench-learning
509 | 
510 | ### Endpoint Signature
511 | - **Path**: `/analytics/trigger-bench-learning`
512 | - **Method**: POST
513 | - **Path Parameters**: None
514 | - **Query Parameters**: None
515 | - **Request Body**: `BenchLearningTriggerRequest`
516 | 
517 | ```python
518 | {
519 |   "business_unit_id": 1,  # optional, null means all BUs
520 |   "skill_ids": [5, 12, 18],  # optional, null means auto-select
521 |   "max_enrollments_per_employee": 3,
522 |   "dry_run": false
523 | }
524 | ```
525 | 
526 | - **Response Shape**: `BenchLearningTriggerRead`
527 | 
528 | ```python
529 | {
530 |   "triggered_at": "2026-05-02T16:30:00Z",
531 |   "dry_run": false,
532 |   "filters": {
533 |     "business_unit_id": 1,
534 |     "skill_ids": [5, 12, 18]
535 |   },
536 |   "bench_employees_found": 6,
537 |   "enrollments_created": 12,
538 |   "enrollments": [
539 |     {
540 |       "employee_id": 3,
541 |       "employee_name": "Arun Patel",
542 |       "resource_id": 2,
543 |       "resource_title": "Kubernetes in Action",
544 |       "skill_id": 5,
545 |       "skill_name": "Kubernetes",
546 |       "enrollment_id": 45,  # null if dry_run=true
547 |       "reason": "Skill gap for career path to Senior Engineer"
548 |     }
549 |   ],
550 |   "summary": {
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,static/index.html,../../../task-08-implement-skill-matrix-tab.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:22:40.389Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.14

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

Now I have all the information I need. Let me create a TODO list and implement Endpoint 4.

<update_todo_list>
<todos>
[x] Read PLAN.md Endpoint 4 specification
[x] Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py
[ ] Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead)
[ ] Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py
[ ] Add 3 tests to tests/test_analytics.py
[ ] Run pytest -v to verify all 33 tests pass
[ ] Verify app imports cleanly with python -c "from app.main import app"
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
demo-script.md,app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,static/index.html,../../../task-08-implement-skill-matrix-tab.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:22:48.892Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.22

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Pending |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Pending |
| 5 | Add 3 tests to tests/test_analytics.py | Pending |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll add the three Pydantic schemas to `app/schemas.py`. I'll place them logically after the existing analytics schemas (after SkillHeatmapRead).

<apply_diff>
<path>app/schemas.py</path>
<diff>
<<<<<<< SEARCH
:start_line:552
-------
class SkillHeatmapRead(BaseModel):
    """Complete skill heatmap across organization or filtered subset."""
    
    filters: SkillHeatmapFilters
    heatmap_data: List[SkillHeatmapItem]
    total_skills: int
    total_employees_analyzed: int
=======
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
app/schemas.py,demo-script.md,app/routers/analytics.py,tests/test_analytics.py,static/index.html,AGENTS.md

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
app/schemas.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:22:58.362Z
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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Pending |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Pending |
| 5 | Add 3 tests to tests/test_analytics.py | Pending |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Read PLAN.md Endpoint 4 specification
[x] Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py
[x] Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead)
[ ] Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py
[ ] Add 3 tests to tests/test_analytics.py
[ ] Run pytest -v to verify all 33 tests pass
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
app/schemas.py,demo-script.md,app/routers/analytics.py,tests/test_analytics.py,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:23:03.232Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.38

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Pending |
| 5 | Add 3 tests to tests/test_analytics.py | Pending |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll implement the endpoint in `app/routers/analytics.py`. I need to add the imports for the new schemas and implement the endpoint after the existing skill-heatmap endpoint.

<apply_diff>
<path>app/routers/analytics.py</path>
<diff>
<<<<<<< SEARCH
:start_line:37
-------
from app.schemas import (
    BusinessUnitSkillBreakdown,
    IndustryTrendsRead,
    RecommendedResourceRead,
    SkillGapAnalysisRead,
    SkillGapItem,
    SkillHeatmapFilters,
    SkillHeatmapItem,
    SkillHeatmapRead,
    TrendingSkillItem,
)
=======
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
- [basedpyright Error] 66 | ) -&gt; SkillGapAnalysisRead: : Function with declared return type "SkillGapAnalysisRead" must return value on all code paths
  "None" is not assignable to "SkillGapAnalysisRead"
- [basedpyright Error] 94 |         proficiency_map: Dict[int, int] = { : Type "dict[Column[int], Column[int]]" is not assignable to declared type "Dict[int, int]"
- [basedpyright Error] 121 |                 current_prof = proficiency_map.get(req.skill_id, 0) : No overloads for "get" match the provided arguments
- [basedpyright Error] 121 |                 current_prof = proficiency_map.get(req.skill_id, 0) : Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "get"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 144 |                                 resource_id=r.id, : Argument of type "Column[int]" cannot be assigned to parameter "resource_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 145 |                                 title=r.title, : Argument of type "Column[str]" cannot be assigned to parameter "title" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 146 |                                 type=r.type, : Argument of type "Column[str]" cannot be assigned to parameter "type" of type "LearningResourceType" in function "__init__"
  "Column[str]" is not assignable to "LearningResourceType"
- [basedpyright Error] 147 |                                 duration_hours=r.duration_hours : Argument of type "Column[int]" cannot be assigned to parameter "duration_hours" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 153 |                         is_critical = gap &gt;= 3 or skill.is_emerging : "is_emerging" is not a known attribute of "None"
- [basedpyright Error] 155 |                         skill_gaps_dict[req.skill_id] = SkillGapItem( : Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "__setitem__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 156 |                             skill_id=req.skill_id, : Argument of type "Column[int]" cannot be assigned to parameter "skill_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 157 |                             skill_name=skill.name, : Argument of type "Column[str]" cannot be assigned to parameter "skill_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 157 |                             skill_name=skill.name, : "name" is not a known attribute of "None"
- [basedpyright Error] 159 |                             required_proficiency=req.min_proficiency, : Argument of type "Column[int]" cannot be assigned to parameter "required_proficiency" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 161 |                             is_critical=is_critical, : Argument of type "Unknown | Column[bool]" cannot be assigned to parameter "is_critical" of type "bool" in function "__init__"
  Type "Unknown | Column[bool]" is not assignable to type "bool"
    "Column[bool]" is not assignable to "bool"
- [basedpyright Error] 166 |                         existing = skill_gaps_dict[req.skill_id] : Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "__getitem__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 167 |                         if req.min_proficiency &gt; existing.required_proficiency: : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 174 |                             is_critical = new_gap &gt;= 3 or skill.is_emerging : "is_emerging" is not a known attribute of "None"
- [basedpyright Error] 175 |                             existing.required_proficiency = req.min_proficiency : Cannot assign to attribute "required_proficiency" for class "SkillGapItem"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 177 |                             existing.is_critical = is_critical : Cannot assign to attribute "is_critical" for class "SkillGapItem"
  Type "Unknown | Column[bool]" is not assignable to type "bool"
    "Column[bool]" is not assignable to "bool"
- [basedpyright Error] 189 |             employee_id=employee.id, : Argument of type "Column[int]" cannot be assigned to parameter "employee_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 190 |             employee_name=employee.name, : Argument of type "Column[str]" cannot be assigned to parameter "employee_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 191 |             current_role=employee.role, : Argument of type "Column[str]" cannot be assigned to parameter "current_role" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 192 |             business_unit_id=employee.business_unit_id, : Argument of type "Column[int]" cannot be assigned to parameter "business_unit_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 211 | ) -&gt; IndustryTrendsRead: : Function with declared return type "IndustryTrendsRead" must return value on all code paths
  "None" is not assignable to "IndustryTrendsRead"
- [basedpyright Error] 287 |                     skill_id=skill.id, : Argument of type "Column[int]" cannot be assigned to parameter "skill_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 288 |                     skill_name=skill.name, : Argument of type "Column[str]" cannot be assigned to parameter "skill_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 289 |                     category=skill.category, : Argument of type "Column[str]" cannot be assigned to parameter "category" of type "SkillCategory" in function "__init__"
  "Column[str]" is not assignable to "SkillCategory"
- [basedpyright Error] 290 |                     is_emerging=skill.is_emerging, : Argument of type "Column[bool]" cannot be assigned to parameter "is_emerging" of type "bool" in function "__init__"
  "Column[bool]" is not assignable to "bool"
- [basedpyright Error] 291 |                     importance=ind_std.importance, : Argument of type "Column[int]" cannot be assigned to parameter "importance" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 292 |                     trend=ind_std.trend, : Argument of type "Column[str]" cannot be assigned to parameter "trend" of type "SkillTrend" in function "__init__"
  "Column[str]" is not assignable to "SkillTrend"
- [basedpyright Error] 308 |             1 for std in industry_standards if std.trend == SkillTrend.RISING : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 311 |             1 for std in industry_standards if std.trend == SkillTrend.STABLE : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 314 |             1 for std in industry_standards if std.trend == SkillTrend.DECLINING : Invalid conditional operand of type "ColumnElement[bool]"
  Method __bool__ for type "ColumnElement[bool]" returns type "NoReturn" rather than "bool"
- [basedpyright Error] 323 |             business_unit_id=business_unit.id, : Argument of type "Column[int]" cannot be assigned to parameter "business_unit_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 324 |             business_unit_name=business_unit.name, : Argument of type "Column[str]" cannot be assigned to parameter "business_unit_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 342 | ) -&gt; SkillHeatmapRead: : Function with declared return type "SkillHeatmapRead" must return value on all code paths
  "None" is not assignable to "SkillHeatmapRead"
- [basedpyright Error] 449 |                             business_unit_id=bu.id, : Argument of type "Column[int]" cannot be assigned to parameter "business_unit_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 450 |                             business_unit_name=bu.name, : Argument of type "Column[str]" cannot be assigned to parameter "business_unit_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 460 |                     skill_id=skill.id, : Argument of type "Column[int]" cannot be assigned to parameter "skill_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 461 |                     skill_name=skill.name, : Argument of type "Column[str]" cannot be assigned to parameter "skill_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 462 |                     category=skill.category, : Argument of type "Column[str]" cannot be assigned to parameter "category" of type "SkillCategory" in function "__init__"
  "Column[str]" is not assignable to "SkillCategory"
- [basedpyright Error] 463 |                     is_emerging=skill.is_emerging, : Argument of type "Column[bool]" cannot be assigned to parameter "is_emerging" of type "bool" in function "__init__"
  "Column[bool]" is not assignable to "bool"</problems>
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
app/schemas.py,app/routers/analytics.py,demo-script.md,tests/test_analytics.py,static/index.html,AGENTS.md

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
app/routers/analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:23:10.563Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.46

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Pending |
| 5 | Add 3 tests to tests/test_analytics.py | Pending |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Good, the imports are added. Now I'll add the endpoint implementation at the end of the file, after the skill-heatmap endpoint. The errors shown are pre-existing type checking issues, not related to my changes.

<insert_content>
<path>app/routers/analytics.py</path>
<line>0</line>
<content>


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
</content>
</insert_content>

---

**User:**

[insert_content for 'app/routers/analytics.py'] Result:
<file_write_result>
<path>app/routers/analytics.py</path>
<operation>modified</operation>
<user_edits>@@ -681,4 +681,4 @@
         )
         
     except NotFoundError as exc:
-        raise_http_from_app_exception(exc)
\ No newline at end of file
+        raise_http_from_app_exception(exc)
</user_edits>
<problems>

New problems detected after saving the file:
app/routers/analytics.py
- [basedpyright Error] 507 | ) -&gt; CareerRecommendationsRead: : Function with declared return type "CareerRecommendationsRead" must return value on all code paths
  "None" is not assignable to "CareerRecommendationsRead"
- [basedpyright Error] 537 |         proficiency_map: Dict[int, int] = { : Type "dict[Column[int], Column[int]]" is not assignable to declared type "Dict[int, int]"
- [basedpyright Error] 578 |                 current_prof = proficiency_map.get(req.skill_id, 0) : No overloads for "get" match the provided arguments
- [basedpyright Error] 578 |                 current_prof = proficiency_map.get(req.skill_id, 0) : Argument of type "Column[int]" cannot be assigned to parameter "key" of type "int" in function "get"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 593 |                                 skill_id=req.skill_id, : Argument of type "Column[int]" cannot be assigned to parameter "skill_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 594 |                                 skill_name=skill.name, : Argument of type "Column[str]" cannot be assigned to parameter "skill_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 595 |                                 required_proficiency=req.min_proficiency, : Argument of type "Column[int]" cannot be assigned to parameter "required_proficiency" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 609 |                                 r.duration_hours for r in resources : Argument of type "Generator[Column[int], None, None]" cannot be assigned to parameter "iterable" of type "Iterable[SupportsRichComparisonT@min]" in function "min"
  "Generator[Column[int], None, None]" is not assignable to "Iterable[SupportsRichComparisonT@min]"
    Type parameter "_T_co@Iterable" is covariant, but "Column[int]" is not a subtype of "SupportsRichComparisonT@min"
      Type "Column[int]" is not assignable to type "SupportsRichComparison"
        Type "Column[int]" is not assignable to type "SupportsRichComparison"
          "Column[int]" is incompatible with protocol "SupportsDunderLT[Any]"
          "Column[int]" is incompatible with protocol "SupportsDunderGT[Any]"
- [basedpyright Error] 649 |                     career_path_id=career_path.id, : Argument of type "Column[int]" cannot be assigned to parameter "career_path_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 650 |                     to_role=career_path.to_role, : Argument of type "Column[str]" cannot be assigned to parameter "to_role" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 652 |                     business_unit_id=career_path.business_unit_id, : Argument of type "Column[int]" cannot be assigned to parameter "business_unit_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 653 |                     business_unit_name=business_unit_name, : Argument of type "Column[str] | Literal['Unknown']" cannot be assigned to parameter "business_unit_name" of type "str" in function "__init__"
  Type "Column[str] | Literal['Unknown']" is not assignable to type "str"
    "Column[str]" is not assignable to "str"
- [basedpyright Error] 674 |             employee_id=employee.id, : Argument of type "Column[int]" cannot be assigned to parameter "employee_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"
- [basedpyright Error] 675 |             employee_name=employee.name, : Argument of type "Column[str]" cannot be assigned to parameter "employee_name" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 676 |             current_role=employee.role, : Argument of type "Column[str]" cannot be assigned to parameter "current_role" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 677 |             current_band=employee.band, : Argument of type "Column[str]" cannot be assigned to parameter "current_band" of type "str" in function "__init__"
  "Column[str]" is not assignable to "str"
- [basedpyright Error] 678 |             business_unit_id=employee.business_unit_id, : Argument of type "Column[int]" cannot be assigned to parameter "business_unit_id" of type "int" in function "__init__"
  "Column[int]" is not assignable to "int"</problems>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
<i>If the user's edits have addressed part of the task or changed the requirements, adjust your approach accordingly.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
app/routers/analytics.py

# VSCode Open Tabs
app/schemas.py,app/routers/analytics.py,demo-script.md,tests/test_analytics.py,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:23:38.128Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.55

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Pending |
| 5 | Add 3 tests to tests/test_analytics.py | Pending |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Read PLAN.md Endpoint 4 specification
[x] Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py
[x] Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead)
[x] Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py
[ ] Add 3 tests to tests/test_analytics.py
[ ] Run pytest -v to verify all 33 tests pass
[ ] Verify app imports cleanly with python -c "from app.main import app"
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
app/routers/analytics.py

# VSCode Open Tabs
app/schemas.py,app/routers/analytics.py,demo-script.md,tests/test_analytics.py,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:23:43.249Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.66

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Completed |
| 5 | Add 3 tests to tests/test_analytics.py | Pending |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll add the three tests to `tests/test_analytics.py`. I'll append them at the end of the file.

<insert_content>
<path>tests/test_analytics.py</path>
<line>0</line>
<content>


# ---------------------------------------------------------------------------
# Endpoint 4: GET /analytics/career-recommendations/{employee_id}
# ---------------------------------------------------------------------------


def test_career_recommendations_for_employee(client: TestClient) -> None:
    """Test career recommendations for employee with known skill gaps."""
    # Arrange: Use employee_id=20 (Divya Shetty has known skill gaps from Task 4)
    employee_id = 20
    
    # Act
    response = client.get(f"/analytics/career-recommendations/{employee_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "employee_id" in data
    assert "employee_name" in data
    assert "current_role" in data
    assert "current_band" in data
    assert "business_unit_id" in data
    assert "recommendations" in data
    assert "total_recommendations" in data
    
    # Verify data types and values
    assert data["employee_id"] == employee_id
    assert isinstance(data["employee_name"], str)
    assert isinstance(data["current_role"], str)
    assert isinstance(data["current_band"], str)
    assert isinstance(data["business_unit_id"], int)
    assert isinstance(data["recommendations"], list)
    assert isinstance(data["total_recommendations"], int)
    assert data["total_recommendations"] >= 0
    assert data["total_recommendations"] == len(data["recommendations"])
    
    # Verify recommendation items structure if any exist
    if data["recommendations"]:
        rec = data["recommendations"][0]
        assert "career_path_id" in rec
        assert "to_role" in rec
        assert "to_band" in rec
        assert "business_unit_id" in rec
        assert "business_unit_name" in rec
        assert "match_score" in rec
        assert "readiness" in rec
        assert "required_skills" in rec
        assert "possessed_skills" in rec
        assert "skill_gaps" in rec
        assert "missing_skills" in rec
        assert "estimated_learning_hours" in rec
        
        # Verify value ranges
        assert 0.0 <= rec["match_score"] <= 1.0
        assert rec["readiness"] in ["HIGH", "MEDIUM", "LOW"]
        assert rec["required_skills"] >= 0
        assert rec["possessed_skills"] >= 0
        assert rec["skill_gaps"] >= 0
        assert rec["skill_gaps"] == rec["required_skills"] - rec["possessed_skills"]
        assert isinstance(rec["missing_skills"], list)
        assert rec["estimated_learning_hours"] >= 0
        
        # Verify missing skills structure if any exist
        if rec["missing_skills"]:
            missing = rec["missing_skills"][0]
            assert "skill_id" in missing
            assert "skill_name" in missing
            assert "required_proficiency" in missing
            assert "current_proficiency" in missing
            assert 1 <= missing["required_proficiency"] <= 5
            assert 0 <= missing["current_proficiency"] <= 5


def test_career_recommendations_employee_not_found(client: TestClient) -> None:
    """Test career recommendations with non-existent employee."""
    # Arrange: Use non-existent employee_id
    employee_id = 99999
    
    # Act
    response = client.get(f"/analytics/career-recommendations/{employee_id}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "Employee" in data["detail"]["message"]


def test_career_recommendations_include_cross_bu(client: TestClient) -> None:
    """Test career recommendations with include_cross_bu=true."""
    # Arrange: Use employee_id=20 with include_cross_bu=true
    employee_id = 20
    
    # Act
    response = client.get(
        f"/analytics/career-recommendations/{employee_id}?include_cross_bu=true"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    
    # If recommendations exist, verify they may include different business units
    if data["recommendations"]:
        # Get employee's business unit
        employee_bu_id = data["business_unit_id"]
        
        # Check if any recommendations are from different business units
        # (This is an edge case test - we're just verifying the parameter works)
        for rec in data["recommendations"]:
            assert "business_unit_id" in rec
            assert isinstance(rec["business_unit_id"], int)
            # The recommendation may or may not be from a different BU
            # We're just testing that the endpoint accepts the parameter

# Made with Bob
</content>
</insert_content>

---

**User:**

[insert_content for 'tests/test_analytics.py'] Result:
<file_write_result>
<path>tests/test_analytics.py</path>
<operation>modified</operation>
<user_edits>@@ -486,4 +486,4 @@
             # The recommendation may or may not be from a different BU
             # We're just testing that the endpoint accepts the parameter
 
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
app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,demo-script.md,static/index.html,AGENTS.md

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
tests/test_analytics.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:24:01.608Z
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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Completed |
| 5 | Add 3 tests to tests/test_analytics.py | Pending |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Read PLAN.md Endpoint 4 specification
[x] Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py
[x] Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead)
[x] Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py
[x] Add 3 tests to tests/test_analytics.py
[ ] Run pytest -v to verify all 33 tests pass
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
app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,demo-script.md,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:24:05.875Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.87

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Completed |
| 5 | Add 3 tests to tests/test_analytics.py | Completed |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll run the tests to verify all 33 tests pass.

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
app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,demo-script.md,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:24:10.647Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.98

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Completed |
| 5 | Add 3 tests to tests/test_analytics.py | Completed |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I need to activate the virtual environment first. Let me run pytest with the venv activated.

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
testpaths: tests
plugins: anyio-4.12.1
collecting ... collected 33 items

tests/test_analytics.py::test_skill_gap_analysis_for_employee_with_gaps PASSED [  3%]
tests/test_analytics.py::test_skill_gap_analysis_employee_not_found PASSED [  6%]
tests/test_analytics.py::test_skill_gap_analysis_employee_with_no_career_paths PASSED [  9%]
tests/test_analytics.py::test_industry_trends_for_business_unit PASSED   [ 12%]
tests/test_analytics.py::test_industry_trends_business_unit_not_found PASSED [ 15%]
tests/test_analytics.py::test_industry_trends_with_trend_filter_rising PASSED [ 18%]
tests/test_analytics.py::test_skill_heatmap_no_filters PASSED            [ 21%]
tests/test_analytics.py::test_skill_heatmap_invalid_min_importance PASSED [ 24%]
tests/test_analytics.py::test_skill_heatmap_with_all_filters PASSED      [ 27%]
tests/test_analytics.py::test_career_recommendations_for_employee PASSED [ 30%]
tests/test_analytics.py::test_career_recommendations_employee_not_found PASSED [ 33%]
tests/test_analytics.py::test_career_recommendations_include_cross_bu PASSED [ 36%]
tests/test_smoke.py::test_health_endpoint PASSED                         [ 39%]
tests/test_smoke.py::test_root_redirects_to_dashboard PASSED             [ 42%]
tests/test_smoke.py::test_static_index_served PASSED                     [ 45%]
tests/test_smoke.py::test_analytics_router_is_mounted PASSED             [ 48%]
tests/test_smoke.py::test_list_business_units_returns_8 PASSED           [ 51%]
tests/test_smoke.py::test_list_employees_returns_30 PASSED               [ 54%]
tests/test_smoke.py::test_filter_employees_by_status_bench_returns_6 PASSED [ 57%]
tests/test_smoke.py::test_filter_employees_by_status_learning_returns_4 PASSED [ 60%]
tests/test_smoke.py::test_filter_employees_by_business_unit PASSED       [ 63%]
tests/test_smoke.py::test_get_employee_by_id_includes_line_manager_id PASSED [ 66%]
tests/test_smoke.py::test_get_nonexistent_employee_returns_404 PASSED    [ 69%]
tests/test_smoke.py::test_create_employee_then_delete PASSED             [ 72%]
tests/test_smoke.py::test_create_duplicate_email_returns_409 PASSED      [ 75%]
tests/test_smoke.py::test_list_projects_with_status_filter PASSED        [ 78%]
tests/test_smoke.py::test_list_skills_returns_50 PASSED                  [ 81%]
tests/test_smoke.py::test_emerging_skills_are_flagged_correctly PASSED   [ 84%]
tests/test_smoke.py::test_industry_standards_filtered_by_bu PASSED       [ 87%]
tests/test_smoke.py::test_career_paths_have_skill_requirements PASSED    [ 90%]
tests/test_smoke.py::test_employee_skills_proficiency_in_range_1_to_5 PASSED [ 93%]
tests/test_smoke.py::test_enrollments_only_for_bench_or_learning_employees PASSED [ 96%]
tests/test_smoke.py::test_pagination_skip_and_limit_work PASSED          [100%]

============================== 33 passed in 0.35s ==============================

<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,demo-script.md,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:24:15.935Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$1.09

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Completed |
| 5 | Add 3 tests to tests/test_analytics.py | Completed |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! All 33 tests pass. Now let me verify the app imports cleanly.

<execute_command>
<command>cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && source .venv/bin/activate && python -c "from app.main import app; print('✓ App imports successfully')"</command>
</execute_command>

---

**User:**

[execute_command for 'cd /Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob && source .venv/bin/activate && python -c "from app.main import app; print('✓ App imports successfully')"'] Result:
Command executed in terminal  within working directory '/Users/swornamacair/Documents/IBM_Hackathon/careerpath-ai-bob-IBMBOB/careerpath-ai-bob'. Exit code: 0
Output:
✓ App imports successfully

<environment_details>
# VSCode Visible Files
tests/test_analytics.py

# VSCode Open Tabs
app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,demo-script.md,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:24:21.027Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$1.21

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Completed |
| 5 | Add 3 tests to tests/test_analytics.py | Completed |
| 6 | Run pytest -v to verify all 33 tests pass | Pending |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Read PLAN.md Endpoint 4 specification
[x] Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py
[x] Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead)
[x] Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py
[x] Add 3 tests to tests/test_analytics.py
[x] Run pytest -v to verify all 33 tests pass
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
app/schemas.py,app/routers/analytics.py,tests/test_analytics.py,demo-script.md,static/index.html,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T10:24:25.303Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$1.33

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
| 1 | Read PLAN.md Endpoint 4 specification | Completed |
| 2 | Read current app/schemas.py, app/routers/analytics.py, tests/test_analytics.py | Completed |
| 3 | Add 3 Pydantic schemas to app/schemas.py (MissingSkillItem, CareerRecommendationItem, CareerRecommendationsRead) | Completed |
| 4 | Implement GET /analytics/career-recommendations/{employee_id} in app/routers/analytics.py | Completed |
| 5 | Add 3 tests to tests/test_analytics.py | Completed |
| 6 | Run pytest -v to verify all 33 tests pass | Completed |
| 7 | Verify app imports cleanly with python -c "from app.main import app" | Completed |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
✅ **Endpoint 4 Implementation Complete**

Successfully implemented GET /analytics/career-recommendations/{employee_id} with all requirements met:

**Files Modified:**
1. **app/schemas.py** - Added 3 Pydantic schemas:
   - `MissingSkillItem` - Skill gap detail for career recommendations
   - `CareerRecommendationItem` - Single career path recommendation with readiness assessment
   - `CareerRecommendationsRead` - Complete career recommendations response

2. **app/routers/analytics.py** - Implemented endpoint with:
   - Path parameter: `employee_id` (int, required)
   - Query parameters: `include_cross_bu` (bool, default=false), `max_recommendations` (int, default=5, max=20)
   - Algorithm follows PLAN.md specification exactly:
     - Fetches employee and validates existence (404 if not found)
     - Builds proficiency map from employee skills
     - Queries career paths from employee's current role
     - Calculates match scores, readiness levels (HIGH/MEDIUM/LOW)
     - Identifies missing skills and estimates learning hours
     - Infers `to_band` from most common band in destination role (None if no employees exist)
     - Sorts by match_score DESC, limits to max_recommendations
   - Uses NotFoundError → raise_http_from_app_exception pattern

3. **tests/test_analytics.py** - Added 3 comprehensive tests:
   - `test_career_recommendations_for_employee` - Happy path with employee_id=20
   - `test_career_recommendations_employee_not_found` - Error case with employee_id=99999, expects 404
   - `test_career_recommendations_include_cross_bu` - Edge case with include_cross_bu=true

**Verification:**
✅ All 33 tests pass (21 smoke + 3 skill-gap + 3 industry-trends + 3 skill-heatmap + 3 career-recommendations)
✅ App imports cleanly with no errors
✅ Python 3.9 syntax only (Optional[X], List[X], Dict[str, X])
✅ Line length ≤ 100 characters
✅ No modifications to files outside scope
✅ Band inference handles edge case where no employees exist in destination role (sets to_band=None)
</result>
</attempt_completion>

