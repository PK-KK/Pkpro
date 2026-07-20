"""Script generation API routes."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.modules.script_generator import ScriptGenerator
from src.core.ai_engine import AIEngine
from src.database.models import db, Script

script_bp = Blueprint('scripts', __name__, url_prefix='/api/scripts')
ai_engine = AIEngine()


@script_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_script(current_user_id):
    """Generate PowerShell or Python script.
    
    Request JSON:
        {
            "description": "What the script should do",
            "script_type": "powershell" or "python" or "bash",
            "language": "th" or "en",
            "title": "Optional script title"
        }
    """
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        script_type = data.get('script_type', 'powershell')
        language = data.get('language', 'th')
        title = data.get('title', description[:50])
        
        if not description:
            return jsonify({'error': 'Description is required'}), 400
        
        if script_type not in ['powershell', 'python', 'bash']:
            return jsonify({'error': 'Invalid script type'}), 400
        
        # Generate script
        result = ScriptGenerator.generate(
            description,
            script_type=script_type,
            ai_engine=ai_engine,
            language=language
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        code = result.get('code', '')
        
        # Validate syntax
        validation = ScriptGenerator.validate_syntax(code, script_type)
        
        # Save to database
        script = Script(
            user_id=current_user_id,
            title=title,
            description=description,
            script_type=script_type,
            code=code,
            language=language
        )
        db.session.add(script)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'script_id': script.id,
            'code': code,
            'script_type': script_type,
            'validation': validation,
            'template_used': result.get('template_used', False)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@script_bp.route('/library', methods=['GET'])
@jwt_required()
def get_script_library(current_user_id):
    """Get user's script library.
    
    Query parameters:
        ?limit=20&offset=0&type=powershell&favorites=true
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        script_type = request.args.get('type', None)
        favorites_only = request.args.get('favorites', 'false').lower() == 'true'
        
        query = Script.query.filter_by(user_id=current_user_id)
        
        if script_type:
            query = query.filter_by(script_type=script_type)
        
        if favorites_only:
            query = query.filter_by(is_favorite=True)
        
        scripts = query.order_by(Script.created_at.desc()) \
                      .limit(limit) \
                      .offset(offset) \
                      .all()
        
        total = Script.query.filter_by(user_id=current_user_id).count()
        
        return jsonify({
            'status': 'success',
            'scripts': [script.to_dict() for script in scripts],
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@script_bp.route('/<int:script_id>', methods=['GET'])
@jwt_required()
def get_script(current_user_id, script_id):
    """Get specific script."""
    try:
        script = Script.query.filter_by(id=script_id, user_id=current_user_id).first()
        
        if not script:
            return jsonify({'error': 'Script not found'}), 404
        
        return jsonify({'status': 'success', 'script': script.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@script_bp.route('/<int:script_id>/favorite', methods=['PUT'])
@jwt_required()
def toggle_favorite(current_user_id, script_id):
    """Toggle script as favorite."""
    try:
        script = Script.query.filter_by(id=script_id, user_id=current_user_id).first()
        
        if not script:
            return jsonify({'error': 'Script not found'}), 404
        
        script.is_favorite = not script.is_favorite
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'is_favorite': script.is_favorite
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@script_bp.route('/<int:script_id>', methods=['DELETE'])
@jwt_required()
def delete_script(current_user_id, script_id):
    """Delete script."""
    try:
        script = Script.query.filter_by(id=script_id, user_id=current_user_id).first()
        
        if not script:
            return jsonify({'error': 'Script not found'}), 404
        
        db.session.delete(script)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Script deleted'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@script_bp.route('/templates/<script_type>', methods=['GET'])
def get_templates(script_type):
    """Get available templates for script type."""
    try:
        templates = ScriptGenerator.get_templates(script_type)
        
        if not templates:
            return jsonify({'error': 'Invalid script type'}), 400
        
        return jsonify({
            'status': 'success',
            'script_type': script_type,
            'templates': templates
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
