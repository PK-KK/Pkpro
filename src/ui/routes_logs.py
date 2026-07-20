"""Log analysis API routes."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.modules.log_analyzer import LogAnalyzer
from src.core.ai_engine import AIEngine
from src.database.models import db, LogAnalysis

log_bp = Blueprint('logs', __name__, url_prefix='/api/logs')
ai_engine = AIEngine()


@log_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_log(current_user_id):
    """Analyze log content.
    
    Request JSON:
        {
            "log_content": "[log content here]",
            "log_type": "event_viewer" or "error_log",
            "language": "th" or "en"
        }
    """
    try:
        data = request.get_json()
        log_content = data.get('log_content', '').strip()
        log_type = data.get('log_type', 'error_log')
        language = data.get('language', 'th')
        
        if not log_content:
            return jsonify({'error': 'Log content is required'}), 400
        
        # Analyze with LogAnalyzer
        analysis = LogAnalyzer.analyze(log_content, ai_engine=ai_engine, language=language)
        
        # Determine severity
        severity = analysis.get('severity', 'info')
        
        # Save to database
        log_record = LogAnalysis(
            user_id=current_user_id,
            log_type=log_type,
            log_content=log_content,
            analysis=str(analysis),
            language=language,
            severity=severity
        )
        db.session.add(log_record)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'analysis_id': log_record.id,
            'analysis': analysis,
            'severity': severity
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@log_bp.route('/history', methods=['GET'])
@jwt_required()
def get_log_history(current_user_id):
    """Get user's log analysis history.
    
    Query parameters:
        ?limit=20&offset=0&severity=critical
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        severity = request.args.get('severity', None)
        
        query = LogAnalysis.query.filter_by(user_id=current_user_id)
        
        if severity:
            query = query.filter_by(severity=severity)
        
        logs = query.order_by(LogAnalysis.created_at.desc()) \
                   .limit(limit) \
                   .offset(offset) \
                   .all()
        
        total = LogAnalysis.query.filter_by(user_id=current_user_id).count()
        
        return jsonify({
            'status': 'success',
            'logs': [log.to_dict() for log in logs],
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@log_bp.route('/<int:log_id>', methods=['GET'])
@jwt_required()
def get_log(current_user_id, log_id):
    """Get specific log analysis."""
    try:
        log = LogAnalysis.query.filter_by(id=log_id, user_id=current_user_id).first()
        
        if not log:
            return jsonify({'error': 'Log not found'}), 404
        
        return jsonify({'status': 'success', 'log': log.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
