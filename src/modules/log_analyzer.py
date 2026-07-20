"""Log analysis module."""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class LogAnalyzer:
    """Analyze logs and error messages."""
    
    # Error pattern detection
    ERROR_PATTERNS = {
        'connection': r'(connection|connect|timeout|refused|closed)',
        'authentication': r'(auth|login|permission|denied|unauthorized|403|401)',
        'database': r'(database|db|sql|query|connection string)',
        'memory': r'(memory|out of memory|heap|ram)',
        'disk': r'(disk|space|storage|full|quota)',
        'network': r'(network|tcp|udp|port|socket|ip)',
        'file': r'(file|path|directory|not found|access denied)',
        'service': r'(service|daemon|process|pid|exit)',
    }
    
    @staticmethod
    def analyze(log_content: str, ai_engine=None, language: str = 'th') -> Dict[str, Any]:
        """Analyze log content."""
        result = {
            'status': 'success',
            'log_length': len(log_content),
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'issues': [],
            'patterns': {},
            'severity': 'info',
            'recommendations': []
        }
        
        # Find error patterns
        for category, pattern in LogAnalyzer.ERROR_PATTERNS.items():
            matches = re.findall(pattern, log_content, re.IGNORECASE)
            if matches:
                result['patterns'][category] = len(matches)
                result['issues'].append(f"Found {len(matches)} {category} related issues")
        
        # Determine severity
        if 'error' in log_content.lower() or 'critical' in log_content.lower():
            result['severity'] = 'critical'
        elif 'warning' in log_content.lower():
            result['severity'] = 'warning'
        else:
            result['severity'] = 'info'
        
        # Extract common issues
        if re.search(r'connection.*timeout', log_content, re.IGNORECASE):
            result['recommendations'].append('Check network connectivity and firewall rules')
        if re.search(r'permission.*denied|access.*denied', log_content, re.IGNORECASE):
            result['recommendations'].append('Verify user permissions and access rights')
        if re.search(r'disk.*space|storage.*full', log_content, re.IGNORECASE):
            result['recommendations'].append('Clean up disk space and temporary files')
        if re.search(r'out of memory|heap', log_content, re.IGNORECASE):
            result['recommendations'].append('Increase allocated memory or optimize memory usage')
        
        # Use AI for deeper analysis if available
        if ai_engine:
            try:
                ai_analysis = ai_engine.analyze_log(log_content, language=language)
                result['ai_analysis'] = ai_analysis.get('analysis', '')
            except Exception as e:
                result['ai_analysis_error'] = str(e)
        
        return result
    
    @staticmethod
    def extract_errors(log_content: str) -> List[str]:
        """Extract error lines from log."""
        errors = []
        for line in log_content.split('\n'):
            if re.search(r'error|exception|failed|critical', line, re.IGNORECASE):
                errors.append(line.strip())
        return errors
    
    @staticmethod
    def parse_timestamp(log_line: str) -> Optional[datetime]:
        """Try to parse timestamp from log line."""
        # Common timestamp formats
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
        ]
        
        for fmt in formats:
            try:
                # Extract potential timestamp
                import re
                match = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', log_line)
                if match:
                    return datetime.strptime(match.group(), formats[0])
            except:
                pass
        
        return None


class EventLogParser:
    """Parse Windows Event Viewer logs."""
    
    @staticmethod
    def parse(xml_content: str) -> List[Dict[str, Any]]:
        """Parse XML event log."""
        events = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_content)
            
            for event in root.findall('.//Event'):
                event_data = {
                    'event_id': event.findtext('.//EventID'),
                    'timestamp': event.findtext('.//TimeCreated[@SystemTime]'),
                    'level': event.findtext('.//Level'),
                    'provider': event.findtext('.//Provider[@Name]'),
                    'message': event.findtext('.//Message'),
                }
                events.append(event_data)
        except Exception as e:
            return {'error': f'Failed to parse event log: {str(e)}'}
        
        return events
