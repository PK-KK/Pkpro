"""Authentication module."""

import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.database.models import db, User


class AuthService:
    """Authentication service."""
    
    @staticmethod
    def register(username, email, password):
        """Register new user."""
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 400
        
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}, 400
        
        user = User(
            username=username,
            email=email,
            role='user',
            is_active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return {'message': 'User registered successfully', 'user': user.to_dict()}, 201
    
    @staticmethod
    def login(username, password):
        """Login user and return token."""
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return {'error': 'Invalid username or password'}, 401
        
        if not user.is_active:
            return {'error': 'User account is inactive'}, 401
        
        # Create JWT token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        
        return {
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def get_user(user_id):
        """Get user by ID."""
        user = User.query.get(user_id)
        return user.to_dict() if user else None
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user information."""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        allowed_fields = ['email']
        for field in allowed_fields:
            if field in kwargs:
                setattr(user, field, kwargs[field])
        
        db.session.commit()
        return user.to_dict(), 200
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password."""
        user = User.query.get(user_id)
        
        if not user or not user.check_password(old_password):
            return {'error': 'Invalid password'}, 401
        
        user.set_password(new_password)
        db.session.commit()
        
        return {'message': 'Password changed successfully'}, 200


def token_required(f):
    """Decorator for routes that require authentication."""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        return f(current_user_id, *args, **kwargs)
    return decorated
