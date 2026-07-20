"""API Routes for the web interface."""

import os
import logging
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

from src.core.ai_engine import AIEngine
from src.core.localization import Localization
from src.core.knowledge_base import KnowledgeBase

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize components
ai_engine = AIEngine()
localization = Localization()
knowledge_base = KnowledgeBase()

api_bp = Blueprint("api", __name__)


@api_bp.route("/chat", methods=["POST"])
def chat():
    """Chat endpoint for Q&A.
    
    Request JSON:
        {
            "question": "Your question",
            "language": "th" or "en",
            "context": "Optional context"
        }
    """
    try:
        data = request.get_json()
        question = data.get("question", "")
        language = data.get("language", "th")
        context = data.get("context", "")
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        # Get AI response
        response = ai_engine.chat(question, context=context, language=language)
        
        return jsonify({
            "status": "success",
            "question": question,
            "answer": response,
            "language": language
        })
    
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


@api_bp.route("/analyze-log", methods=["POST"])
def analyze_log():
    """Analyze logs and error messages.
    
    Request JSON:
        {
            "log_content": "Log content to analyze",
            "language": "th" or "en"
        }
    """
    try:
        data = request.get_json()
        log_content = data.get("log_content", "")
        language = data.get("language", "th")
        
        if not log_content:
            return jsonify({"error": "Log content is required"}), 400
        
        # Analyze log
        result = ai_engine.analyze_log(log_content, language=language)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in /analyze-log: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


@api_bp.route("/generate-script", methods=["POST"])
def generate_script():
    """Generate PowerShell or Python scripts.
    
    Request JSON:
        {
            "description": "What the script should do",
            "script_language": "powershell" or "python",
            "language": "th" or "en"
        }
    """
    try:
        data = request.get_json()
        description = data.get("description", "")
        script_language = data.get("script_language", "powershell")
        language = data.get("language", "th")
        
        if not description:
            return jsonify({"error": "Description is required"}), 400
        
        # Generate script
        script = ai_engine.generate_script(description, script_language, language)
        
        return jsonify({
            "status": "success",
            "description": description,
            "script_language": script_language,
            "script": script,
            "language": language
        })
    
    except Exception as e:
        logger.error(f"Error in /generate-script: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


@api_bp.route("/knowledge-base/search", methods=["GET"])
def search_knowledge_base():
    """Search knowledge base.
    
    Query parameters:
        ?query=search_term&category=category_name
    """
    try:
        query = request.args.get("query", "")
        category = request.args.get("category", None)
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        results = knowledge_base.search(query, category=category)
        
        return jsonify({
            "status": "success",
            "query": query,
            "category": category,
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in /knowledge-base/search: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


@api_bp.route("/knowledge-base/categories", methods=["GET"])
def get_categories():
    """Get all knowledge base categories."""
    try:
        categories = knowledge_base.list_categories()
        return jsonify({
            "status": "success",
            "categories": categories
        })
    
    except Exception as e:
        logger.error(f"Error in /knowledge-base/categories: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


@api_bp.route("/knowledge-base/add", methods=["POST"])
def add_article():
    """Add article to knowledge base.
    
    Request JSON:
        {
            "category": "category_name",
            "title": "Article title",
            "content": "Article content",
            "tags": ["tag1", "tag2"],
            "language": "th" or "en"
        }
    """
    try:
        data = request.get_json()
        category = data.get("category", "")
        title = data.get("title", "")
        content = data.get("content", "")
        tags = data.get("tags", [])
        language = data.get("language", "th")
        
        if not all([category, title, content]):
            return jsonify({"error": "Category, title, and content are required"}), 400
        
        article = knowledge_base.add_article(category, title, content, tags, language)
        
        if "error" in article:
            return jsonify(article), 400
        
        return jsonify({
            "status": "success",
            "article": article
        })
    
    except Exception as e:
        logger.error(f"Error in /knowledge-base/add: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


@api_bp.route("/model-info", methods=["GET"])
def model_info():
    """Get AI model information."""
    try:
        info = ai_engine.get_model_info()
        return jsonify({
            "status": "success",
            "model": info
        })
    
    except Exception as e:
        logger.error(f"Error in /model-info: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500
