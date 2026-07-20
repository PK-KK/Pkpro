"""Report generation module."""

from datetime import datetime
from typing import Dict, List, Any, Optional
import json


class ReportGenerator:
    """Generate various types of reports."""
    
    REPORT_TYPES = [
        'network_diagnostic',
        'security_audit',
        'performance_analysis',
        'system_health',
        'incident_report',
        'compliance_check'
    ]
    
    @staticmethod
    def generate(report_type: str, data: Dict[str, Any], language: str = 'th') -> Dict[str, Any]:
        """Generate report based on type and data."""
        if report_type not in ReportGenerator.REPORT_TYPES:
            return {'error': f'Unknown report type: {report_type}'}, 400
        
        report_method = getattr(ReportGenerator, f'_generate_{report_type}', None)
        if report_method:
            return report_method(data, language)
        
        return {'error': 'Report generation failed'}, 500
    
    @staticmethod
    def _generate_network_diagnostic(data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate network diagnostic report."""
        report = {
            'type': 'network_diagnostic',
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'status': 'success',
            'sections': [
                {
                    'title': 'Network Connectivity' if language == 'en' else 'การเชื่อมต่อเครือข่าย',
                    'data': data.get('connectivity', {})
                },
                {
                    'title': 'DNS Status' if language == 'en' else 'สถานะ DNS',
                    'data': data.get('dns', {})
                },
                {
                    'title': 'Firewall Rules' if language == 'en' else 'กฎ Firewall',
                    'data': data.get('firewall', {})
                }
            ]
        }
        return report
    
    @staticmethod
    def _generate_security_audit(data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate security audit report."""
        report = {
            'type': 'security_audit',
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'status': 'success',
            'sections': [
                {
                    'title': 'User Accounts' if language == 'en' else 'บัญชีผู้ใช้',
                    'data': data.get('users', {})
                },
                {
                    'title': 'Access Control' if language == 'en' else 'การควบคุมการเข้าถึง',
                    'data': data.get('access_control', {})
                },
                {
                    'title': 'Vulnerabilities' if language == 'en' else 'จุดอ่อน',
                    'data': data.get('vulnerabilities', {})
                }
            ]
        }
        return report
    
    @staticmethod
    def _generate_performance_analysis(data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate performance analysis report."""
        report = {
            'type': 'performance_analysis',
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'status': 'success',
            'sections': [
                {
                    'title': 'CPU Usage' if language == 'en' else 'การใช้ CPU',
                    'data': data.get('cpu', {})
                },
                {
                    'title': 'Memory Usage' if language == 'en' else 'การใช้หน่วยความจำ',
                    'data': data.get('memory', {})
                },
                {
                    'title': 'Disk I/O' if language == 'en' else 'Disk I/O',
                    'data': data.get('disk_io', {})
                }
            ]
        }
        return report
    
    @staticmethod
    def _generate_system_health(data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate system health report."""
        report = {
            'type': 'system_health',
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'status': 'success',
            'sections': [
                {
                    'title': 'System Status' if language == 'en' else 'สถานะระบบ',
                    'data': data.get('status', {})
                },
                {
                    'title': 'Services' if language == 'en' else 'บริการ',
                    'data': data.get('services', {})
                },
                {
                    'title': 'Updates' if language == 'en' else 'การอัปเดต',
                    'data': data.get('updates', {})
                }
            ]
        }
        return report
    
    @staticmethod
    def _generate_incident_report(data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate incident report."""
        report = {
            'type': 'incident_report',
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'status': 'success',
            'sections': [
                {
                    'title': 'Incident Details' if language == 'en' else 'รายละเอียดเหตุการณ์',
                    'data': data.get('incident', {})
                },
                {
                    'title': 'Timeline' if language == 'en' else 'ลำดับเหตุการณ์',
                    'data': data.get('timeline', {})
                },
                {
                    'title': 'Resolution' if language == 'en' else 'การแก้ไข',
                    'data': data.get('resolution', {})
                }
            ]
        }
        return report
    
    @staticmethod
    def _generate_compliance_check(data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate compliance check report."""
        report = {
            'type': 'compliance_check',
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'status': 'success',
            'sections': [
                {
                    'title': 'Compliance Status' if language == 'en' else 'สถานะความเป็นไปตามข้อกำหนด',
                    'data': data.get('status', {})
                },
                {
                    'title': 'Issues Found' if language == 'en' else 'ปัญหาที่พบ',
                    'data': data.get('issues', {})
                },
                {
                    'title': 'Recommendations' if language == 'en' else 'คำแนะนำ',
                    'data': data.get('recommendations', {})
                }
            ]
        }
        return report
    
    @staticmethod
    def export_to_json(report: Dict[str, Any]) -> str:
        """Export report to JSON."""
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    @staticmethod
    def export_to_html(report: Dict[str, Any]) -> str:
        """Export report to HTML."""
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{report.get('type', 'Report')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #2563eb; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ccc; }}
        .timestamp {{ color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>{report.get('type', 'Report')}</h1>
    <p class="timestamp">Generated: {report.get('timestamp', '')}</p>
'''
        
        for section in report.get('sections', []):
            html += f'<div class="section"><h2>{section.get("title", "")}</h2>'
            html += f'<pre>{json.dumps(section.get("data", {}), indent=2, ensure_ascii=False)}</pre>'
            html += '</div>'
        
        html += '''</body>
</html>
'''
        return html
