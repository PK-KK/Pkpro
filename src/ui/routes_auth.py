"""Authentication API routes."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.auth import AuthService
from src.database.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user.
    
    Request JSON:
        {
            "username": "username",
            "email": "user@example.com",
            "password": "password123"
        }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not all([username, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        if '@' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        result, status_code = AuthService.register(username, email, password)
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user.
    
    Request JSON:
        {
            "username": "username",
            "password": "password"
        }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        result, status_code = AuthService.login(username, password)
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user(current_user_id):
    """Get current user information."""
    try:
        user_data = AuthService.get_user(current_user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user_data}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_user(current_user_id):
    """Update user information."""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if email and '@' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        result, status_code = AuthService.update_user(current_user_id, email=email)
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password(current_user_id):
    """Change user password.
    
    Request JSON:
        {
            "old_password": "old_pass",
            "new_password": "new_pass"
        }
    """
    try:
        data = request.get_json()
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        if not old_password or not new_password:
            return jsonify({'error': 'Both passwords required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': 'New password must be at least 6 characters'}), 400
        
        result, status_code = AuthService.change_password(current_user_id, old_password, new_password)
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users(current_user_id):
    """List all users (admin only)."""
    try:
        # Check if current user is admin
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        users = User.query.all()
        return jsonify({
            'status': 'success',
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
