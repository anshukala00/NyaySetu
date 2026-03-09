"""
Tests for CORS middleware configuration
Validates NFR2.5: CORS shall be configured to allow only frontend origin
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_cors_headers_present_on_options_request():
    """Test that CORS headers are present on OPTIONS preflight request"""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        }
    )
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"


def test_cors_headers_present_on_get_request():
    """Test that CORS headers are present on actual GET request"""
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"}
    )
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"


def test_cors_allows_all_methods():
    """Test that CORS allows all HTTP methods"""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        }
    )
    
    assert response.status_code == 200
    assert "access-control-allow-methods" in response.headers
    # FastAPI CORS middleware returns the requested method or "*"
    allowed_methods = response.headers["access-control-allow-methods"]
    assert "POST" in allowed_methods or "*" in allowed_methods


def test_cors_allows_all_headers():
    """Test that CORS allows all headers"""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization,Content-Type",
        }
    )
    
    assert response.status_code == 200
    assert "access-control-allow-headers" in response.headers
    allowed_headers = response.headers["access-control-allow-headers"].lower()
    assert "authorization" in allowed_headers or "*" in allowed_headers


def test_cors_credentials_enabled():
    """Test that CORS credentials are enabled (NFR2.5)"""
    response = client.get(
        "/",
        headers={"Origin": "http://localhost:3000"}
    )
    
    assert response.status_code == 200
    assert response.headers["access-control-allow-credentials"] == "true"


def test_health_endpoint_accessible():
    """Test that health endpoint is accessible and returns correct response"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint_accessible():
    """Test that root endpoint is accessible and returns correct response"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Nyaysetu" in response.json()["message"]
