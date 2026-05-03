"""Tests for analytics endpoints.

Tests cover skill gap analysis, industry trends, skill heatmap,
career recommendations, and bench learning trigger functionality.
"""

import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Endpoint 1: GET /analytics/skill-gap/{employee_id}
# ---------------------------------------------------------------------------


def test_skill_gap_analysis_for_employee_with_gaps(client: TestClient) -> None:
    """Test skill gap analysis for employee with career path requirements."""
    # Arrange: Use employee_id=1 from seeded data
    employee_id = 1
    
    # Act
    response = client.get(f"/analytics/skill-gap/{employee_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "employee_id" in data
    assert "employee_name" in data
    assert "current_role" in data
    assert "business_unit_id" in data
    assert "skill_gaps" in data
    assert "total_gaps" in data
    assert "critical_gaps" in data
    
    # Verify data types and values
    assert data["employee_id"] == employee_id
    assert isinstance(data["employee_name"], str)
    assert isinstance(data["current_role"], str)
    assert isinstance(data["business_unit_id"], int)
    assert isinstance(data["skill_gaps"], list)
    assert isinstance(data["total_gaps"], int)
    assert isinstance(data["critical_gaps"], int)
    assert data["total_gaps"] >= 0
    assert data["critical_gaps"] >= 0
    assert data["critical_gaps"] <= data["total_gaps"]
    
    # Verify skill gap items structure if any exist
    if data["skill_gaps"]:
        gap_item = data["skill_gaps"][0]
        assert "skill_id" in gap_item
        assert "skill_name" in gap_item
        assert "current_proficiency" in gap_item
        assert "required_proficiency" in gap_item
        assert "gap" in gap_item
        assert "is_critical" in gap_item
        assert "recommended_resources" in gap_item
        
        # Verify proficiency values are in valid range
        assert 0 <= gap_item["current_proficiency"] <= 5
        assert 1 <= gap_item["required_proficiency"] <= 5
        assert gap_item["gap"] > 0
        assert isinstance(gap_item["is_critical"], bool)
        assert isinstance(gap_item["recommended_resources"], list)


def test_skill_gap_analysis_employee_not_found(client: TestClient) -> None:
    """Test skill gap analysis with non-existent employee."""
    # Arrange: Use non-existent employee_id
    employee_id = 99999
    
    # Act
    response = client.get(f"/analytics/skill-gap/{employee_id}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "Employee" in data["detail"]["message"]


def test_skill_gap_analysis_employee_with_no_career_paths(
    client: TestClient
) -> None:
    """Test skill gap analysis for employee with no defined career paths."""
    # Arrange: Find an employee whose role has no career paths
    # First, get all employees
    employees_response = client.get("/employees/?limit=100")
    assert employees_response.status_code == 200
    employees = employees_response.json()
    
    # Get all career paths to find roles without paths
    paths_response = client.get("/career-paths/?limit=100")
    assert paths_response.status_code == 200
    paths = paths_response.json()
    
    # Collect roles that have career paths defined
    roles_with_paths = set()
    for path in paths:
        roles_with_paths.add(path["from_role"])
    
    # Find an employee whose role is not in roles_with_paths
    employee_without_path = None
    for emp in employees:
        if emp["role"] not in roles_with_paths:
            employee_without_path = emp
            break
    
    # If all employees have career paths, create a test employee without one
    if employee_without_path is None:
        # Get a valid business_unit_id
        bu_id = employees[0]["business_unit_id"]
        payload = {
            "name": "Test Employee No Path",
            "email": "test.nopath.unique@example.com",
            "role": "Unique Role With No Path",
            "band": "B1",
            "business_unit_id": bu_id,
            "line_manager_id": None,
            "current_status": "ACTIVE",
            "hire_date": "2024-01-01",
        }
        create_response = client.post("/employees/", json=payload)
        assert create_response.status_code == 201
        employee_without_path = create_response.json()
    
    # Act
    response = client.get(f"/analytics/skill-gap/{employee_without_path['id']}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == employee_without_path["id"]
    assert data["total_gaps"] == 0
    assert data["critical_gaps"] == 0
    assert data["skill_gaps"] == []

# Made with Bob



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


# ---------------------------------------------------------------------------
# Endpoint 3: GET /analytics/skill-heatmap
# ---------------------------------------------------------------------------


def test_skill_heatmap_no_filters(client: TestClient) -> None:
    """Test skill heatmap with no filters (happy path)."""
    # Act
    response = client.get("/analytics/skill-heatmap")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "filters" in data
    assert "heatmap_data" in data
    assert "total_skills" in data
    assert "total_employees_analyzed" in data
    
    # Verify filters structure
    filters = data["filters"]
    assert "business_unit_id" in filters
    assert "skill_category" in filters
    assert "min_importance" in filters
    assert filters["business_unit_id"] is None
    assert filters["skill_category"] is None
    assert filters["min_importance"] is None
    
    # Verify data types
    assert isinstance(data["heatmap_data"], list)
    assert isinstance(data["total_skills"], int)
    assert isinstance(data["total_employees_analyzed"], int)
    assert data["total_skills"] >= 0
    assert data["total_employees_analyzed"] >= 0
    
    # Verify heatmap items structure if any exist
    if data["heatmap_data"]:
        item = data["heatmap_data"][0]
        assert "skill_id" in item
        assert "skill_name" in item
        assert "category" in item
        assert "is_emerging" in item
        assert "total_employees" in item
        assert "proficiency_distribution" in item
        assert "avg_proficiency" in item
        assert "certified_count" in item
        assert "business_units" in item
        
        # Verify proficiency_distribution
        prof_dist = item["proficiency_distribution"]
        assert isinstance(prof_dist, dict)
        for level in ["1", "2", "3", "4", "5"]:
            assert level in prof_dist
            assert isinstance(prof_dist[level], int)
            assert prof_dist[level] >= 0
        
        # Verify distribution sums to total_employees
        dist_sum = sum(prof_dist.values())
        assert dist_sum == item["total_employees"]
        
        # Verify business_units structure
        assert isinstance(item["business_units"], list)
        if item["business_units"]:
            bu = item["business_units"][0]
            assert "business_unit_id" in bu
            assert "business_unit_name" in bu
            assert "employee_count" in bu
            assert "avg_proficiency" in bu
            assert isinstance(bu["employee_count"], int)
            assert isinstance(bu["avg_proficiency"], float)
            assert 0.0 <= bu["avg_proficiency"] <= 5.0


def test_skill_heatmap_invalid_min_importance(client: TestClient) -> None:
    """Test skill heatmap with invalid min_importance (error case)."""
    # Arrange: Use min_importance=10 (out of range 1-5)
    
    # Act
    response = client.get("/analytics/skill-heatmap?min_importance=10")
    
    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_skill_heatmap_with_all_filters(client: TestClient) -> None:
    """Test skill heatmap with all filters applied (edge case)."""
    # Arrange: Use business_unit_id=1, skill_category=TECHNICAL, min_importance=3
    business_unit_id = 1
    skill_category = "TECHNICAL"
    min_importance = 3
    
    # Act
    response = client.get(
        f"/analytics/skill-heatmap?business_unit_id={business_unit_id}"
        f"&skill_category={skill_category}&min_importance={min_importance}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify filters are reflected in response
    filters = data["filters"]
    assert filters["business_unit_id"] == business_unit_id
    assert filters["skill_category"] == skill_category
    assert filters["min_importance"] == min_importance
    
    # Verify results match filter criteria
    for item in data["heatmap_data"]:
        # All skills should be TECHNICAL
        assert item["category"] == skill_category
        
        # All business_units in breakdown should match the filter
        for bu in item["business_units"]:
            assert bu["business_unit_id"] == business_unit_id

# Made with Bob



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



# ---------------------------------------------------------------------------
# Endpoint 5: POST /analytics/trigger-bench-learning
# ---------------------------------------------------------------------------


def test_trigger_bench_learning_dry_run(client: TestClient) -> None:
    """Test bench learning trigger with dry_run=true (happy path)."""
    # Arrange: Use existing seeded bench employees (seeder creates 6 BENCH employees)
    # Get a valid business unit with bench employees
    bu_response = client.get("/business-units/?limit=1")
    assert bu_response.status_code == 200
    business_unit_id = bu_response.json()[0]["id"]
    
    # Arrange: Trigger request with dry_run=true
    trigger_payload = {
        "business_unit_id": None,  # Use all business units to find bench employees
        "skill_ids": None,
        "max_enrollments_per_employee": 3,
        "dry_run": True
    }
    
    # Act
    response = client.post("/analytics/trigger-bench-learning", json=trigger_payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "triggered_at" in data
    assert "dry_run" in data
    assert "filters" in data
    assert "bench_employees_found" in data
    assert "enrollments_created" in data
    assert "enrollments" in data
    assert "summary" in data
    
    # Verify dry_run flag
    assert data["dry_run"] is True
    
    # Verify bench employees found (seeder creates 6 BENCH employees)
    assert data["bench_employees_found"] >= 1
    
    # Verify all enrollment_id values are None (dry_run mode)
    for enrollment in data["enrollments"]:
        assert enrollment["enrollment_id"] is None
        assert "employee_id" in enrollment
        assert "employee_name" in enrollment
        assert "resource_id" in enrollment
        assert "resource_title" in enrollment
        assert "skill_id" in enrollment
        assert "skill_name" in enrollment
        assert "reason" in enrollment
    
    # Verify summary structure
    summary = data["summary"]
    assert "total_hours_allocated" in summary
    assert "skills_targeted" in summary
    assert "avg_enrollments_per_employee" in summary
    assert isinstance(summary["total_hours_allocated"], int)
    assert isinstance(summary["skills_targeted"], int)
    assert isinstance(summary["avg_enrollments_per_employee"], float)


def test_trigger_bench_learning_invalid_business_unit(client: TestClient) -> None:
    """Test bench learning trigger with non-existent business unit (error case)."""
    # Arrange: Use non-existent business_unit_id
    trigger_payload = {
        "business_unit_id": 99999,
        "skill_ids": None,
        "max_enrollments_per_employee": 3,
        "dry_run": True
    }
    
    # Act
    response = client.post("/analytics/trigger-bench-learning", json=trigger_payload)
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "BusinessUnit" in data["detail"]["message"]


def test_trigger_bench_learning_with_skill_filter(client: TestClient) -> None:
    """Test bench learning trigger with skill_ids filter (edge case)."""
    # Arrange: Get valid skill IDs
    skills_response = client.get("/skills/?limit=3")
    assert skills_response.status_code == 200
    skills = skills_response.json()
    
    if len(skills) < 2:
        # Skip test if not enough skills in database
        return
    
    skill_ids = [skills[0]["id"], skills[1]["id"]]
    
    # Trigger with skill filter
    trigger_payload = {
        "business_unit_id": None,
        "skill_ids": skill_ids,
        "max_enrollments_per_employee": 3,
        "dry_run": True
    }
    
    # Act
    response = client.post("/analytics/trigger-bench-learning", json=trigger_payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify filters are reflected
    assert data["filters"]["skill_ids"] == skill_ids
    
    # Verify all enrollments target only the specified skills
    for enrollment in data["enrollments"]:
        assert enrollment["skill_id"] in skill_ids
    
    # Verify enrollments_created constraint
    if data["bench_employees_found"] > 0:
        max_possible = (
            data["bench_employees_found"] * 
            trigger_payload["max_enrollments_per_employee"]
        )
        assert data["enrollments_created"] <= max_possible


def test_trigger_bench_learning_creates_enrollments(client: TestClient) -> None:
    """Test bench learning trigger with dry_run=false (integration test)."""
    # Arrange: Use existing seeded bench employees
    # Get count of enrollments before trigger
    enrollments_before_response = client.get("/enrollments/?limit=1000")
    assert enrollments_before_response.status_code == 200
    enrollments_before_count = len(enrollments_before_response.json())
    
    # Get existing bench employees to verify later
    bench_employees_response = client.get("/employees/?status=BENCH&limit=100")
    assert bench_employees_response.status_code == 200
    bench_employees = bench_employees_response.json()
    
    # Skip test if no bench employees exist
    if len(bench_employees) == 0:
        return
    
    # Trigger with dry_run=false, limit to 1 enrollment per employee
    trigger_payload = {
        "business_unit_id": None,
        "skill_ids": None,
        "max_enrollments_per_employee": 1,
        "dry_run": False
    }
    
    # Act
    response = client.post("/analytics/trigger-bench-learning", json=trigger_payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Verify dry_run is false
    assert data["dry_run"] is False
    
    # If enrollments were created, verify enrollment_id values are NOT None
    if data["enrollments_created"] > 0:
        for enrollment in data["enrollments"]:
            assert enrollment["enrollment_id"] is not None
            assert isinstance(enrollment["enrollment_id"], int)
        
        # Verify enrollments were actually created in database
        enrollments_after_response = client.get("/enrollments/?limit=1000")
        assert enrollments_after_response.status_code == 200
        enrollments_after = enrollments_after_response.json()
        enrollments_after_count = len(enrollments_after)
        
        # Should have more enrollments now
        assert enrollments_after_count > enrollments_before_count
        
        # Verify the new enrollments count matches
        new_enrollments_count = enrollments_after_count - enrollments_before_count
        assert new_enrollments_count == data["enrollments_created"]

# Made with Bob
