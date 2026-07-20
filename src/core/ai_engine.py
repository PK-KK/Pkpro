"""AI Engine using Google Gemini API."""

import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai


logger = logging.getLogger(__name__)


class AIEngine:
    """AI Engine for processing requests using Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        """Initialize AI Engine.
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model name (default: gemini-2.0-flash)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"AI Engine initialized with model: {self.model_name}")

    def chat(self, prompt: str, context: str = "", language: str = "th") -> str:
        """Send a chat message to Gemini.
        
        Args:
            prompt: User's question or request
            context: Additional context information
            language: Response language ('th' or 'en')
            
        Returns:
            AI response
        """
        try:
            # Build system prompt based on language
            if language == "th":
                system_prompt = (
                    "คุณเป็น AI IT Technician Assistant ที่ช่วยเหลือวิศวกร IT \n"
                    "- ตอบคำถามเกี่ยวกับ IT, Infrastructure, Networking \n"
                    "- ให้คำแนะนำที่ชัดเจนและปฏิบัติได้ \n"
                    "- ตอบเป็นภาษาไทยเท่านั้น \n"
                    "- ถ้าได้รับข้อมูล Log หรือ Error ให้ทำการวิเคราะห์โดยละเอียด"
                )
            else:
                system_prompt = (
                    "You are an AI IT Technician Assistant helping IT engineers. \n"
                    "- Answer questions about IT, Infrastructure, Networking \n"
                    "- Provide clear and actionable recommendations \n"
                    "- Respond only in English \n"
                    "- If provided with logs or errors, analyze them in detail"
                )
            
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n"
            if context:
                full_prompt += f"Context: {context}\n\n"
            full_prompt += f"User: {prompt}"
            
            # Call Gemini API
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                logger.info("AI response generated successfully")
                return response.text
            else:
                logger.warning("Empty response from Gemini API")
                return "ไม่สามารถได้รับคำตอบจาก AI" if language == "th" else "Unable to get response from AI"
        
        except Exception as e:
            logger.error(f"Error in AI chat: {str(e)}")
            error_msg = f"เกิดข้อผิดพลาด: {str(e)}" if language == "th" else f"Error: {str(e)}"
            return error_msg

    def analyze_log(self, log_content: str, language: str = "th") -> Dict[str, Any]:
        """Analyze logs and error messages.
        
        Args:
            log_content: Log or error content to analyze
            language: Response language
            
        Returns:
            Analysis result with findings and recommendations
        """
        if language == "th":
            prompt = (
                "วิเคราะห์ Log ด้านล่างนี้: \n"
                f"{log_content}\n\n"
                "กรุณา: \n"
                "1. ระบุปัญหาที่เกิดขึ้น \n"
                "2. อธิบายสาเหตุที่เป็นไปได้ \n"
                "3. แนะนำวิธีแก้ไข \n"
                "4. ข้อเตือนที่สำคัญ"
            )
        else:
            prompt = (
                "Analyze the following log: \n"
                f"{log_content}\n\n"
                "Please: \n"
                "1. Identify the issues \n"
                "2. Explain possible causes \n"
                "3. Recommend solutions \n"
                "4. Important warnings"
            )
        
        analysis = self.chat(prompt, language=language)
        
        return {
            "status": "success",
            "analysis": analysis,
            "language": language
        }

    def generate_script(self, description: str, script_language: str = "powershell", lang: str = "th") -> str:
        """Generate PowerShell or Python script.
        
        Args:
            description: What the script should do
            script_language: 'powershell' or 'python'
            lang: Response language
            
        Returns:
            Generated script
        """
        if lang == "th":
            prompt = (
                f"สร้าง {script_language} script สำหรับ: {description}\n\n"
                "ข้อกำหนด: \n"
                "- โค้ดต้องสามารถใช้งานได้จริง \n"
                "- เพิ่ม Comments เป็นภาษาไทย \n"
                "- เพิ่มการจัดการ Error \n"
                "- ให้โค้ดที่สมบูรณ์พร้อมใช้งาน"
            )
        else:
            prompt = (
                f"Create a {script_language} script for: {description}\n\n"
                "Requirements: \n"
                "- Code must be functional \n"
                "- Add comments in English \n"
                "- Include error handling \n"
                "- Provide complete, ready-to-use code"
            )
        
        return self.chat(prompt, language=lang)

    def get_model_info(self) -> Dict[str, str]:
        """Get information about the current model.
        
        Returns:
            Model information
        """
        return {
            "model": self.model_name,
            "type": "Gemini",
            "status": "active"
        }
