"""Knowledge Base system for storing and retrieving IT documentation."""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class KnowledgeBase:
    """Manage knowledge base for IT documentation."""

    def __init__(self, storage_path: str = "knowledge_base"):
        """Initialize Knowledge Base.
        
        Args:
            storage_path: Path to store knowledge base files
        """
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.categories = {
            "windows_server": "Windows Server Tips & Tricks",
            "active_directory": "Active Directory Management",
            "networking": "Network Diagnostics",
            "security": "Security & Firewall",
            "databases": "Database Administration",
            "troubleshooting": "Troubleshooting Guides",
            "sop": "Standard Operating Procedures",
            "scripts": "Useful Scripts",
            "faq": "Frequently Asked Questions",
        }

    def add_article(self, category: str, title: str, content: str, 
                   tags: List[str] = None, language: str = "th") -> Dict[str, Any]:
        """Add a new article to knowledge base.
        
        Args:
            category: Article category
            title: Article title
            content: Article content
            tags: List of tags for categorization
            language: Language of content ('th' or 'en')
            
        Returns:
            Article metadata
        """
        if category not in self.categories:
            return {"error": f"Category '{category}' not found"}
        
        article_id = f"{category}_{datetime.now().timestamp()}"
        article = {
            "id": article_id,
            "category": category,
            "title": title,
            "content": content,
            "tags": tags or [],
            "language": language,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save to file
        filepath = os.path.join(self.storage_path, f"{article_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        
        return article

    def search(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Search knowledge base.
        
        Args:
            query: Search query
            category: Limit search to specific category
            
        Returns:
            List of matching articles
        """
        results = []
        query_lower = query.lower()
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self.storage_path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                
                # Filter by category if specified
                if category and article.get("category") != category:
                    continue
                
                # Search in title, content, and tags
                if (query_lower in article.get("title", "").lower() or
                    query_lower in article.get("content", "").lower() or
                    query_lower in " ".join(article.get("tags", [])).lower()):
                    results.append(article)
        
        return results

    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Get specific article by ID.
        
        Args:
            article_id: Article ID
            
        Returns:
            Article data or None if not found
        """
        filepath = os.path.join(self.storage_path, f"{article_id}.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def list_categories(self) -> Dict[str, str]:
        """List all available categories.
        
        Returns:
            Dictionary of categories and their descriptions
        """
        return self.categories

    def get_category_articles(self, category: str) -> List[Dict[str, Any]]:
        """Get all articles in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            List of articles in category
        """
        articles = []
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self.storage_path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                
                if article.get("category") == category:
                    articles.append(article)
        
        return articles
