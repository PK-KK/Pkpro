"""Unit tests for API endpoints."""

import pytest
import json
from src.ui.app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns 200."""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'


class TestIndexEndpoint:
    """Test index endpoint."""

    def test_index(self, client):
        """Test index page."""
        response = client.get('/')
        assert response.status_code == 200
        assert 'app' in response.json
        assert 'endpoints' in response.json


class TestChatEndpoint:
    """Test chat endpoint."""

    def test_chat_with_question(self, client):
        """Test chat with valid question."""
        data = {
            'question': 'Test question',
            'language': 'th'
        }
        response = client.post('/api/chat',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert 'answer' in response.json

    def test_chat_without_question(self, client):
        """Test chat without question."""
        data = {'language': 'th'}
        response = client.post('/api/chat',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 400
        assert 'error' in response.json


class TestKnowledgeBase:
    """Test knowledge base endpoints."""

    def test_get_categories(self, client):
        """Test getting KB categories."""
        response = client.get('/api/knowledge-base/categories')
        assert response.status_code == 200
        assert 'categories' in response.json

    def test_add_article(self, client):
        """Test adding article."""
        data = {
            'category': 'faq',
            'title': 'Test Article',
            'content': 'Test content',
            'tags': ['test'],
            'language': 'th'
        }
        response = client.post('/api/knowledge-base/add',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 200
        assert response.json['status'] == 'success'

    def test_search_knowledge_base(self, client):
        """Test searching knowledge base."""
        response = client.get('/api/knowledge-base/search?query=test')
        assert response.status_code == 200
        assert 'results' in response.json
