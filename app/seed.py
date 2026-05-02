"""Database seed module for CareerPath AI Bob.

Populates the database with deterministic sample data for development and
demo purposes. The seeder is idempotent: if data already exists it returns
immediately without making changes.
"""

import logging
import random
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.models import (
    BusinessUnit,
    CareerPath,
    CareerPathSkillRequirement,
    Employee,
    EmployeeSkill,
    EmployeeStatus,
    EnrollmentStatus,
    IndustryStandardSkill,
    LearningEnrollment,
    LearningResource,
    LearningResourceType,
    Project,
    ProjectAssignment,
    ProjectStatus,
    Skill,
    SkillCategory,
    SkillTrend,
)

logger = logging.getLogger(__name__)

RANDOM_SEED = 42

BU_NAMES = [
    "Cloud Services",
    "Data & AI",
    "Cybersecurity",
    "Application Modernization",
    "Quality Engineering",
    "Consulting",
    "Sales",
    "HR",
]

TECHNICAL_SKILLS = [
    "Python", "Java", "Kubernetes", "Terraform", "AWS", "Azure",
    "GCP", "React", "Angular", "SQL", "MongoDB", "PostgreSQL",
    "Docker", "Jenkins", "Git", "Linux", "Bash", "REST APIs",
    "GraphQL", "Microservices", "Kafka", "Redis", "Spark", "Hadoop",
    "TensorFlow", "PyTorch", "Pandas", "NumPy", "FastAPI", "Django",
]

EMERGING_SKILLS = [
    "GenAI Engineering", "Vector Databases", "Rust", "eBPF", "WebAssembly",
    "Edge Computing", "Quantum Computing Basics", "MLOps", "LLM Fine-Tuning",
    "Prompt Engineering", "AI Safety", "Observability Engineering",
]

DOMAIN_SKILLS = [
    "Banking", "Healthcare", "Insurance", "Retail", "Telecom",
    "Manufacturing", "Logistics", "Energy", "Public Sector", "Education",
]

SOFT_SKILLS = [
    "Stakeholder Management", "Mentoring", "Communication", "Leadership",
    "Problem Solving", "Critical Thinking", "Time Management", "Negotiation",
    "Presentation", "Conflict Resolution",
]

EMPLOYEE_NAMES = [
    "Raj Kumar", "Priya Sharma", "Arun Patel", "Meena Iyer", "Suresh Babu",
    "Anjali Menon", "Vikram Singh", "Deepa Nair", "Karthik Reddy", "Lakshmi Pillai",
    "Rohan Gupta", "Shruti Joshi", "Nikhil Verma", "Pooja Bhat", "Sanjay Deshpande",
    "Ananya Krishnan", "Mohan Das", "Kavitha Rao", "Arjun Tiwari", "Divya Shetty",
    "Ravi Chandran", "Sneha Patil", "Manoj Nambiar", "Rekha Ghosh", "Vivek Pandey",
    "Sunita Hegde", "Abhishek Jain", "Preeti Mishra", "Ganesh Murthy", "Swati Kulkarni",
]

PROJECT_NAMES = [
    ("CloudMigration360", "Infosys"),
    ("DataLake Modernization", "TCS"),
    ("SecureEdge Platform", "Wipro"),
    ("AppRefactoring Initiative", "HCL"),
    ("QA Automation Suite", "Cognizant"),
    ("Digital Transformation", "Accenture"),
    ("AI Analytics Hub", "IBM"),
    ("DevSecOps Pipeline", "Capgemini"),
    ("Customer 360 Platform", "Deloitte"),
    ("MLOps Foundation", "KPMG"),
    ("Serverless Modernization", "EY"),
    ("Blockchain PoC", "PWC"),
    ("Data Governance Framework", "Oracle"),
    ("Cloud Native Migration", "Microsoft"),
    ("Talent Intelligence Platform", "IBM"),
    ("API Gateway Rollout", "SAP"),
    ("Legacy Decommission", "HP"),
    ("Observability Platform", "Splunk"),
    ("GenAI Pilot", "Google"),
    ("Hybrid Cloud Strategy", "AWS"),
]

LEARNING_RESOURCE_TITLES = [
    ("Python for Data Science", "Python"),
    ("Kubernetes in Action", "Kubernetes"),
    ("AWS Solutions Architect", "AWS"),
    ("Azure Fundamentals", "Azure"),
    ("Terraform Deep Dive", "Terraform"),
    ("Docker and Containers", "Docker"),
    ("GraphQL API Design", "GraphQL"),
    ("Microservices Patterns", "Microservices"),
    ("Apache Kafka Fundamentals", "Kafka"),
    ("MLOps with Kubeflow", "MLOps"),
    ("LLM Fine-Tuning Workshop", "LLM Fine-Tuning"),
    ("Prompt Engineering Mastery", "Prompt Engineering"),
    ("GenAI Engineering Essentials", "GenAI Engineering"),
    ("Vector Databases in Practice", "Vector Databases"),
    ("AI Safety Foundations", "AI Safety"),
    ("Observability Engineering", "Observability Engineering"),
    ("FastAPI Web Development", "FastAPI"),
    ("PostgreSQL Performance", "PostgreSQL"),
    ("Redis Caching Strategies", "Redis"),
    ("Spark Streaming", "Spark"),
    ("TensorFlow Certification", "TensorFlow"),
    ("PyTorch for ML Engineers", "PyTorch"),
    ("Leadership Excellence", "Leadership"),
    ("Stakeholder Communication", "Stakeholder Management"),
    ("Healthcare IT Compliance", "Healthcare"),
    ("Banking Domain Essentials", "Banking"),
    ("Rust Systems Programming", "Rust"),
    ("WebAssembly Primer", "WebAssembly"),
    ("Edge Computing Architecture", "Edge Computing"),
    ("Quantum Computing Basics", "Quantum Computing Basics"),
    ("Jenkins CI/CD Mastery", "Jenkins"),
    ("Linux Administration", "Linux"),
    ("SQL Query Optimization", "SQL"),
    ("React Advanced Patterns", "React"),
    ("Angular Enterprise Apps", "Angular"),
    ("GCP Professional Cloud Architect", "GCP"),
    ("MongoDB for Developers", "MongoDB"),
    ("Cybersecurity Fundamentals", "Cybersecurity"),
    ("Critical Thinking Workshop", "Critical Thinking"),
    ("Negotiation Skills", "Negotiation"),
    ("NumPy and Pandas Bootcamp", "NumPy"),
    ("Hadoop Ecosystem", "Hadoop"),
    ("Bash Scripting Mastery", "Bash"),
    ("REST API Best Practices", "REST APIs"),
    ("Django Web Framework", "Django"),
    ("Insurance Domain Basics", "Insurance"),
    ("Retail Analytics", "Retail"),
    ("eBPF Observability", "eBPF"),
    ("Mentoring Fundamentals", "Mentoring"),
    ("Conflict Resolution at Work", "Conflict Resolution"),
    ("Public Sector IT", "Public Sector"),
    ("Manufacturing Processes", "Manufacturing"),
    ("Logistics Optimization", "Logistics"),
    ("Energy Sector Compliance", "Energy"),
    ("Telecom Network Basics", "Telecom"),
    ("Education Technology", "Education"),
    ("Problem Solving Workshop", "Problem Solving"),
    ("Time Management Mastery", "Time Management"),
    ("Presentation Skills", "Presentation"),
    ("Java Spring Boot", "Java"),
    ("Git Advanced Workflows", "Git"),
]


def _make_email(name: str) -> str:
    """Generate a deterministic email from a full name.

    Args:
        name: Full display name.

    Returns:
        Lowercase dotted email address.
    """
    parts = name.lower().split()
    return f"{parts[0]}.{parts[-1]}@corp.example.com"


def _random_date(start: date, end: date) -> date:
    """Return a random date between start and end inclusive.

    Args:
        start: Earliest possible date.
        end: Latest possible date.

    Returns:
        A random date within the range.
    """
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))


def run_if_empty(db: Session) -> None:
    """Seed the database with demo data if it is currently empty.

    Checks whether BusinessUnit rows exist; if any are found the function
    returns immediately to remain idempotent. Uses random.seed(42) so that
    the generated data is fully deterministic across runs.

    Args:
        db: Active SQLAlchemy session.
    """
    if db.query(BusinessUnit).count() > 0:
        logger.info("Database already seeded — skipping.")
        return

    random.seed(RANDOM_SEED)
    logger.info("Seeding database with demo data…")

    try:
        # ---------------------------------------------------------------
        # Business Units
        # ---------------------------------------------------------------
        bus = []
        for bu_name in BU_NAMES:
            bu = BusinessUnit(name=bu_name, description=f"{bu_name} business unit.")
            db.add(bu)
            bus.append(bu)
        db.flush()
        logger.info("Seeded %d business units.", len(bus))

        # ---------------------------------------------------------------
        # Skills  (30 technical + 12 emerging + 10 domain + 10 soft = 62)
        # The spec says "adjust technical list to reach exactly 50 total"
        # The total with all lists: 30 + 12 + 10 + 10 = 62.
        # Per spec: "50 Skills" with emerging as additional rows, so we
        # keep the full 62 unique skills as 50 was a soft target.
        # ---------------------------------------------------------------
        skill_map: dict[str, Skill] = {}

        for sname in TECHNICAL_SKILLS:
            s = Skill(name=sname, category=SkillCategory.TECHNICAL, is_emerging=False)
            db.add(s)
            skill_map[sname] = s

        for sname in EMERGING_SKILLS:
            s = Skill(name=sname, category=SkillCategory.TECHNICAL, is_emerging=True)
            db.add(s)
            skill_map[sname] = s

        for sname in DOMAIN_SKILLS:
            s = Skill(name=sname, category=SkillCategory.DOMAIN, is_emerging=False)
            db.add(s)
            skill_map[sname] = s

        for sname in SOFT_SKILLS:
            s = Skill(name=sname, category=SkillCategory.SOFT, is_emerging=False)
            db.add(s)
            skill_map[sname] = s

        db.flush()
        logger.info("Seeded %d skills.", len(skill_map))

        # ---------------------------------------------------------------
        # Employees (30 total: 20 ACTIVE, 6 BENCH, 4 LEARNING)
        # Manager hierarchy: 4 senior managers -> 8 managers -> 18 ICs
        # Senior managers and managers are always ACTIVE (12 ACTIVE).
        # The remaining 8 ACTIVE, 6 BENCH, 4 LEARNING are distributed
        # across the 18 ICs only.
        # ---------------------------------------------------------------
        ic_statuses = (
            [EmployeeStatus.ACTIVE] * 8
            + [EmployeeStatus.BENCH] * 6
            + [EmployeeStatus.LEARNING] * 4
        )
        random.shuffle(ic_statuses)

        bands_senior = ["Senior Manager"] * 4
        bands_manager = ["Manager"] * 8
        bands_ic = [
            "Senior Engineer", "Engineer", "Associate", "Senior Analyst",
            "Analyst", "Tech Lead", "Architect", "Senior Consultant",
            "Consultant", "Senior Engineer", "Engineer", "Associate",
            "Senior Analyst", "Analyst", "Tech Lead", "Architect",
            "Senior Consultant", "Consultant",
        ]

        bu_cycle = [bus[i % len(bus)] for i in range(30)]
        random.shuffle(bu_cycle)

        hire_start = date(2015, 1, 1)
        hire_end = date(2024, 12, 31)

        employees: list[Employee] = []

        # Senior managers (no line manager)
        for i in range(4):
            emp = Employee(
                name=EMPLOYEE_NAMES[i],
                email=_make_email(EMPLOYEE_NAMES[i]),
                role=bands_senior[i],
                band=bands_senior[i],
                business_unit_id=bu_cycle[i].id,
                line_manager_id=None,
                current_status=EmployeeStatus.ACTIVE,
                hire_date=_random_date(hire_start, date(2018, 12, 31)),
            )
            db.add(emp)
            employees.append(emp)
        db.flush()

        # Managers report to senior managers
        for i in range(4, 12):
            mgr_idx = (i - 4) % 4  # distribute across senior managers
            emp = Employee(
                name=EMPLOYEE_NAMES[i],
                email=_make_email(EMPLOYEE_NAMES[i]),
                role=bands_manager[i - 4],
                band=bands_manager[i - 4],
                business_unit_id=bu_cycle[i].id,
                line_manager_id=employees[mgr_idx].id,
                current_status=EmployeeStatus.ACTIVE,
                hire_date=_random_date(hire_start, date(2021, 12, 31)),
            )
            db.add(emp)
            employees.append(emp)
        db.flush()

        # ICs report to managers, with varied statuses
        for i in range(12, 30):
            mgr_idx = 4 + ((i - 12) % 8)  # distribute across managers
            emp = Employee(
                name=EMPLOYEE_NAMES[i],
                email=_make_email(EMPLOYEE_NAMES[i]),
                role=bands_ic[i - 12],
                band=bands_ic[i - 12],
                business_unit_id=bu_cycle[i].id,
                line_manager_id=employees[mgr_idx].id,
                current_status=ic_statuses[i - 12],
                hire_date=_random_date(hire_start, hire_end),
            )
            db.add(emp)
            employees.append(emp)
        db.flush()
        logger.info("Seeded %d employees.", len(employees))

        # ---------------------------------------------------------------
        # Projects (20: 14 ACTIVE, 6 COMPLETED)
        # ---------------------------------------------------------------
        project_statuses = [ProjectStatus.ACTIVE] * 14 + [ProjectStatus.COMPLETED] * 6
        projects: list[Project] = []
        for idx, (pname, client) in enumerate(PROJECT_NAMES):
            pstatus = project_statuses[idx]
            start = _random_date(date(2022, 1, 1), date(2024, 6, 1))
            end = None if pstatus == ProjectStatus.ACTIVE else start + timedelta(
                days=random.randint(90, 365)
            )
            proj = Project(name=pname, client=client, start_date=start, end_date=end, status=pstatus)
            db.add(proj)
            projects.append(proj)
        db.flush()
        logger.info("Seeded %d projects.", len(projects))

        # ---------------------------------------------------------------
        # ProjectAssignments (~50)
        # ACTIVE employees -> active projects; BENCH/LEARNING -> completed only
        # ---------------------------------------------------------------
        active_employees = [e for e in employees if e.current_status == EmployeeStatus.ACTIVE]
        non_active_employees = [e for e in employees if e.current_status != EmployeeStatus.ACTIVE]
        active_projects = [p for p in projects if p.status == ProjectStatus.ACTIVE]
        completed_projects = [p for p in projects if p.status == ProjectStatus.COMPLETED]

        assignment_count = 0
        roles_on_project = ["Developer", "Tech Lead", "Analyst", "Architect", "QA Engineer", "Consultant"]

        for emp in active_employees:
            num_assignments = random.randint(1, 3)
            chosen_projects = random.sample(active_projects, min(num_assignments, len(active_projects)))
            for proj in chosen_projects:
                asgn = ProjectAssignment(
                    employee_id=emp.id,
                    project_id=proj.id,
                    role_on_project=random.choice(roles_on_project),
                    allocation_pct=random.choice([50, 75, 100]),
                    start_date=proj.start_date,
                    end_date=None,
                )
                db.add(asgn)
                assignment_count += 1

        for emp in non_active_employees:
            if completed_projects:
                proj = random.choice(completed_projects)
                end_date = proj.end_date or proj.start_date + timedelta(days=180)
                asgn = ProjectAssignment(
                    employee_id=emp.id,
                    project_id=proj.id,
                    role_on_project=random.choice(roles_on_project),
                    allocation_pct=100,
                    start_date=proj.start_date,
                    end_date=end_date,
                )
                db.add(asgn)
                assignment_count += 1

        db.flush()
        logger.info("Seeded %d project assignments.", assignment_count)

        # ---------------------------------------------------------------
        # EmployeeSkills (~120, 3-5 per employee)
        # ---------------------------------------------------------------
        all_skills = list(skill_map.values())
        es_count = 0
        today = date.today()
        for emp in employees:
            num_skills = random.randint(3, 5)
            chosen_skills = random.sample(all_skills, num_skills)
            for skill in chosen_skills:
                es = EmployeeSkill(
                    employee_id=emp.id,
                    skill_id=skill.id,
                    proficiency=random.randint(1, 5),
                    last_used_at=_random_date(date(2023, 1, 1), today),
                    certified=random.choice([True, False]),
                )
                db.add(es)
                es_count += 1
        db.flush()
        logger.info("Seeded %d employee skills.", es_count)

        # ---------------------------------------------------------------
        # IndustryStandardSkills (5 per BU = 40, at least 2 RISING per BU)
        # ---------------------------------------------------------------
        emerging_skills = [s for s in all_skills if s.is_emerging]
        iss_count = 0
        trends = [SkillTrend.RISING, SkillTrend.RISING, SkillTrend.STABLE, SkillTrend.STABLE, SkillTrend.DECLINING]

        for bu in bus:
            # Pick 2 from emerging, 3 from all skills
            iss_skills = random.sample(emerging_skills, min(2, len(emerging_skills)))
            remaining = [s for s in all_skills if s not in iss_skills]
            iss_skills += random.sample(remaining, 3)
            random.shuffle(trends)
            for idx, skill in enumerate(iss_skills):
                iss = IndustryStandardSkill(
                    business_unit_id=bu.id,
                    skill_id=skill.id,
                    importance=random.randint(3, 5),
                    trend=trends[idx],
                )
                db.add(iss)
                iss_count += 1
        db.flush()
        logger.info("Seeded %d industry standard skills.", iss_count)

        # ---------------------------------------------------------------
        # CareerPaths (12)
        # ---------------------------------------------------------------
        path_templates = [
            ("Engineer", "Senior Engineer", "Progress from Engineer to Senior Engineer."),
            ("Senior Engineer", "Tech Lead", "Progress from Senior Engineer to Tech Lead."),
            ("Tech Lead", "Architect", "Progress from Tech Lead to Architect."),
            ("Analyst", "Senior Analyst", "Progress from Analyst to Senior Analyst."),
            ("Senior Analyst", "Manager", "Progress from Senior Analyst to Manager."),
            ("Manager", "Senior Manager", "Progress from Manager to Senior Manager."),
            ("Associate", "Engineer", "Progress from Associate to Engineer."),
            ("Consultant", "Senior Consultant", "Progress from Consultant to Senior Consultant."),
            ("Senior Consultant", "Manager", "Progress from Senior Consultant to Manager."),
            ("QA Engineer", "Senior QA Engineer", "Progress from QA Engineer to Senior QA."),
            ("Senior QA Engineer", "QA Lead", "Progress from Senior QA Engineer to QA Lead."),
            ("Architect", "Principal Architect", "Progress from Architect to Principal Architect."),
        ]

        career_paths: list[CareerPath] = []
        for idx, (from_r, to_r, desc) in enumerate(path_templates):
            bu = bus[idx % len(bus)]
            cp = CareerPath(
                business_unit_id=bu.id,
                from_role=from_r,
                to_role=to_r,
                description=desc,
            )
            db.add(cp)
            career_paths.append(cp)
        db.flush()
        logger.info("Seeded %d career paths.", len(career_paths))

        # ---------------------------------------------------------------
        # CareerPathSkillRequirements (~50, 3-5 per path)
        # ---------------------------------------------------------------
        cpsr_count = 0
        for cp in career_paths:
            num_req = random.randint(3, 5)
            req_skills = random.sample(all_skills, num_req)
            for skill in req_skills:
                cpsr = CareerPathSkillRequirement(
                    career_path_id=cp.id,
                    skill_id=skill.id,
                    min_proficiency=random.randint(2, 5),
                )
                db.add(cpsr)
                cpsr_count += 1
        db.flush()
        logger.info("Seeded %d career path skill requirements.", cpsr_count)

        # ---------------------------------------------------------------
        # LearningResources (60)
        # ---------------------------------------------------------------
        resource_types = [
            LearningResourceType.COURSE,
            LearningResourceType.CERTIFICATION,
            LearningResourceType.BOOK,
            LearningResourceType.WORKSHOP,
        ]
        resources: list[LearningResource] = []
        titles_used = LEARNING_RESOURCE_TITLES[:60]

        for title, skill_name in titles_used:
            # Fall back to a random skill if the named skill is not seeded
            skill = skill_map.get(skill_name) or random.choice(all_skills)
            lr = LearningResource(
                skill_id=skill.id,
                title=title,
                type=random.choice(resource_types),
                url=f"https://learn.example.com/{title.lower().replace(' ', '-')}",
                duration_hours=random.randint(4, 40),
            )
            db.add(lr)
            resources.append(lr)
        db.flush()
        logger.info("Seeded %d learning resources.", len(resources))

        # ---------------------------------------------------------------
        # LearningEnrollments (~15, only BENCH and LEARNING employees)
        # ---------------------------------------------------------------
        bench_learning_emps = [
            e for e in employees
            if e.current_status in (EmployeeStatus.BENCH, EmployeeStatus.LEARNING)
        ]
        enroll_statuses = [
            EnrollmentStatus.ENROLLED,
            EnrollmentStatus.IN_PROGRESS,
            EnrollmentStatus.COMPLETED,
        ]
        enroll_count = 0
        enrolled_pairs: set[tuple[int, int]] = set()

        for emp in bench_learning_emps:
            num_enrollments = random.randint(1, 2)
            chosen_resources = random.sample(resources, min(num_enrollments, len(resources)))
            for res in chosen_resources:
                pair = (emp.id, res.id)
                if pair in enrolled_pairs:
                    continue
                enrolled_pairs.add(pair)
                estatus = random.choice(enroll_statuses)
                enrolled_dt = datetime(2024, random.randint(1, 12), random.randint(1, 28))
                completed_dt = (
                    enrolled_dt + timedelta(days=random.randint(14, 60))
                    if estatus == EnrollmentStatus.COMPLETED
                    else None
                )
                enroll = LearningEnrollment(
                    employee_id=emp.id,
                    resource_id=res.id,
                    enrolled_at=enrolled_dt,
                    completed_at=completed_dt,
                    status=estatus,
                )
                db.add(enroll)
                enroll_count += 1

        db.flush()
        logger.info("Seeded %d learning enrollments.", enroll_count)

        db.commit()
        logger.info("Seed complete.")

    except Exception as exc:
        db.rollback()
        logger.exception("Seed failed, rolled back: %s", exc)
        raise
