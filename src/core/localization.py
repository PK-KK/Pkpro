"""Localization system for Thai and English support."""

import os
import json
from typing import Dict, Any


class Localization:
    """Handle multilingual support for the application."""

    def __init__(self, default_language: str = "th"):
        """Initialize localization system.
        
        Args:
            default_language: Default language code ('th' or 'en')
        """
        self.default_language = default_language
        self.supported_languages = ["th", "en"]
        self.translations = self._load_translations()

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translations from JSON files.
        
        Returns:
            Dictionary of translations by language
        """
        translations = {
            "th": {},
            "en": {}
        }
        
        # Load from files if they exist
        translations_dir = os.path.join(os.path.dirname(__file__), "translations")
        
        for lang in self.supported_languages:
            filepath = os.path.join(translations_dir, f"{lang}.json")
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    translations[lang] = json.load(f)
        
        return translations

    def get(self, key: str, language: str = None, **kwargs) -> str:
        """Get translated string.
        
        Args:
            key: Translation key
            language: Language code (defaults to default_language)
            **kwargs: Variables for string formatting
            
        Returns:
            Translated string
        """
        if language is None:
            language = self.default_language
        
        if language not in self.supported_languages:
            language = self.default_language
        
        text = self.translations.get(language, {}).get(key, key)
        
        # Format with provided variables
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text

    def set_language(self, language: str) -> bool:
        """Set default language.
        
        Args:
            language: Language code
            
        Returns:
            True if language is supported, False otherwise
        """
        if language in self.supported_languages:
            self.default_language = language
            return True
        return False

    def list_supported_languages(self) -> list:
        """Get list of supported languages.
        
        Returns:
            List of language codes
        """
        return self.supported_languages
