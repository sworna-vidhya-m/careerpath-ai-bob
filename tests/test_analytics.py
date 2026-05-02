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
