"""Knowledge Base API routes."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database.models import db, KBArticle, User

kb_bp = Blueprint('kb', __name__, url_prefix='/api/knowledge-base')


@kb_bp.route('/search', methods=['GET'])
def search_articles():
    """Search knowledge base articles.
    
    Query parameters:
        ?query=search_term&category=windows_server&language=th&limit=20
    """
    try:
        query = request.args.get('query', '').strip()
        category = request.args.get('category', None)
        language = request.args.get('language', None)
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Build query
        articles_query = KBArticle.query
        
        # Search in title and content
        articles_query = articles_query.filter(
            (KBArticle.title.ilike(f'%{query}%')) |
            (KBArticle.content.ilike(f'%{query}%')) |
            (KBArticle.tags.ilike(f'%{query}%'))
        )
        
        if category:
            articles_query = articles_query.filter_by(category=category)
        
        if language:
            articles_query = articles_query.filter_by(language=language)
        
        articles = articles_query.limit(limit).all()
        
        # Increment view count
        for article in articles:
            article.views += 1
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'query': query,
            'results': [article.to_dict() for article in articles],
            'count': len(articles)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kb_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all knowledge base categories."""
    try:
        categories = db.session.query(KBArticle.category).distinct().all()
        category_list = [cat[0] for cat in categories]
        
        return jsonify({
            'status': 'success',
            'categories': category_list
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kb_bp.route('/featured', methods=['GET'])
def get_featured():
    """Get featured articles."""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        articles = KBArticle.query.filter_by(is_featured=True) \
                             .order_by(KBArticle.views.desc()) \
                             .limit(limit) \
                             .all()
        
        return jsonify({
            'status': 'success',
            'articles': [article.to_dict() for article in articles],
            'count': len(articles)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kb_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Get specific article."""
    try:
        article = KBArticle.query.get(article_id)
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Increment view count
        article.views += 1
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'article': article.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kb_bp.route('/add', methods=['POST'])
@jwt_required()
def add_article(current_user_id):
    """Add new knowledge base article (admin only).
    
    Request JSON:
        {
            "category": "windows_server",
            "title": "Article Title",
            "content": "Article content",
            "tags": "tag1, tag2",
            "language": "th",
            "is_featured": false
        }
    """
    try:
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        category = data.get('category', '').strip()
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        tags = data.get('tags', '')
        language = data.get('language', 'th')
        is_featured = data.get('is_featured', False)
        
        if not all([category, title, content]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        article = KBArticle(
            category=category,
            title=title,
            content=content,
            tags=tags,
            language=language,
            is_featured=is_featured
        )
        db.session.add(article)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'article': article.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kb_bp.route('/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(current_user_id, article_id):
    """Update knowledge base article (admin only)."""
    try:
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        article = KBArticle.query.get(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            article.title = data['title']
        if 'content' in data:
            article.content = data['content']
        if 'tags' in data:
            article.tags = data['tags']
        if 'is_featured' in data:
            article.is_featured = data['is_featured']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'article': article.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kb_bp.route('/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(current_user_id, article_id):
    """Delete knowledge base article (admin only)."""
    try:
        # Check if user is admin
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        article = KBArticle.query.get(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        db.session.delete(article)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Article deleted'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
