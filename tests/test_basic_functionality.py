import pytest
import requests
import os

class TestDocumentPortal:
    """Test suite for Document Portal basic functionality"""
    
    @pytest.fixture
    def base_url(self):
        """Get base URL from environment or use default"""
        return os.getenv('DOCUMENT_PORTAL_URL', 'http://localhost:8000')
    
    def test_health_endpoint(self, base_url):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'ok'
            assert 'service' in data
            print(f"✅ Health check passed: {data}")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Service not accessible: {e}")
    
    def test_main_page(self, base_url):
        """Test main application page"""
        try:
            response = requests.get(f"{base_url}/", timeout=10)
            assert response.status_code == 200
            assert 'text/html' in response.headers.get('content-type', '')
            print(f"✅ Main page accessible: {response.status_code}")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Service not accessible: {e}")
    
    def test_api_docs(self, base_url):
        """Test API documentation endpoint"""
        try:
            response = requests.get(f"{base_url}/docs", timeout=10)
            assert response.status_code == 200
            assert 'text/html' in response.headers.get('content-type', '')
            print(f"✅ API docs accessible: {response.status_code}")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Service not accessible: {e}")
    
    def test_redoc_endpoint(self, base_url):
        """Test ReDoc endpoint"""
        try:
            response = requests.get(f"{base_url}/redoc", timeout=10)
            assert response.status_code == 200
            assert 'text/html' in response.headers.get('content-type', '')
            print(f"✅ ReDoc accessible: {response.status_code}")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Service not accessible: {e}")
    
    def test_openapi_schema(self, base_url):
        """Test OpenAPI schema endpoint"""
        try:
            response = requests.get(f"{base_url}/openapi.json", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert 'openapi' in data
            assert 'info' in data
            print(f"✅ OpenAPI schema accessible: {response.status_code}")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Service not accessible: {e}")

class TestLoadBalancer:
    """Test suite for Load Balancer functionality"""
    
    @pytest.fixture
    def alb_url(self):
        """Get ALB URL from environment"""
        return os.getenv('ALB_URL')
    
    @pytest.mark.skipif(not os.getenv('ALB_URL'), reason="ALB URL not configured")
    def test_alb_health_check(self, alb_url):
        """Test ALB health check"""
        response = requests.get(f"{alb_url}/health", timeout=10)
        assert response.status_code == 200
        print(f"✅ ALB health check passed: {response.status_code}")
    
    @pytest.mark.skipif(not os.getenv('ALB_URL'), reason="ALB URL not configured")
    def test_alb_main_page(self, alb_url):
        """Test ALB main page"""
        response = requests.get(f"{alb_url}/", timeout=10)
        assert response.status_code == 200
        print(f"✅ ALB main page accessible: {response.status_code}")

if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"])
