"""Chat API routes."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.core.ai_engine import AIEngine
from src.database.models import db, Chat

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')
ai_engine = AIEngine()


@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message(current_user_id):
    """Send chat message and get AI response.
    
    Request JSON:
        {
            "question": "Your question",
            "language": "th" or "en",
            "context": "Optional context"
        }
    """
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        language = data.get('language', 'th')
        context = data.get('context', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # Get AI response
        answer = ai_engine.chat(question, context=context, language=language)
        
        # Save to database
        chat = Chat(
            user_id=current_user_id,
            question=question,
            answer=answer,
            language=language,
            context=context
        )
        db.session.add(chat)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'chat_id': chat.id,
            'question': question,
            'answer': answer,
            'language': language
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history(current_user_id):
    """Get user's chat history.
    
    Query parameters:
        ?limit=20&offset=0
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        chats = Chat.query.filter_by(user_id=current_user_id) \
                   .order_by(Chat.created_at.desc()) \
                   .limit(limit) \
                   .offset(offset) \
                   .all()
        
        total = Chat.query.filter_by(user_id=current_user_id).count()
        
        return jsonify({
            'status': 'success',
            'chats': [chat.to_dict() for chat in chats],
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/<int:chat_id>', methods=['GET'])
@jwt_required()
def get_chat(current_user_id, chat_id):
    """Get specific chat message."""
    try:
        chat = Chat.query.filter_by(id=chat_id, user_id=current_user_id).first()
        
        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        
        return jsonify({'status': 'success', 'chat': chat.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/<int:chat_id>', methods=['DELETE'])
@jwt_required()
def delete_chat(current_user_id, chat_id):
    """Delete chat message."""
    try:
        chat = Chat.query.filter_by(id=chat_id, user_id=current_user_id).first()
        
        if not chat:
            return jsonify({'error': 'Chat not found'}), 404
        
        db.session.delete(chat)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Chat deleted'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
