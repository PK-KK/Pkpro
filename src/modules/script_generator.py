"""Script generation module."""

from typing import Dict, List, Any
from datetime import datetime


class ScriptGenerator:
    """Generate PowerShell, Python, and Bash scripts."""
    
    TEMPLATES = {
        'powershell': {
            'disk_space': '''# Check Disk Space
$drives = Get-Volume
foreach ($drive in $drives) {
    $percentUsed = ($drive.SizeRemaining / $drive.Size) * 100
    Write-Host "$($drive.DriveLetter): $percentUsed% free"
}
''',
            'user_list': '''# List Active Directory Users
Get-ADUser -Filter * -Properties Name, EmailAddress, LastLogonDate | 
Select-Object Name, EmailAddress, LastLogonDate | 
Format-Table -AutoSize
''',
            'services': '''# List Running Services
Get-Service | Where-Object {$_.Status -eq 'Running'} | 
Select-Object Name, DisplayName | 
Format-Table -AutoSize
''',
            'network_test': '''# Test Network Connectivity
$hosts = @('8.8.8.8', '1.1.1.1', 'google.com')
foreach ($host in $hosts) {
    if (Test-Connection -ComputerName $host -Count 1 -Quiet) {
        Write-Host "$host: OK" -ForegroundColor Green
    } else {
        Write-Host "$host: FAILED" -ForegroundColor Red
    }
}
'''
        },
        'python': {
            'disk_space': '''import shutil
import psutil

# Check disk usage
for partition in psutil.disk_partitions():
    usage = psutil.disk_usage(partition.mountpoint)
    print(f"{partition.device}: {usage.percent}% used")
''',
            'network_test': '''import socket
import platform
import subprocess

HOSTS = ['8.8.8.8', '1.1.1.1', 'google.com']

for host in HOSTS:
    try:
        result = subprocess.run(['ping', '-c', '1' if platform.system() != 'Windows' else '-n', '1', host],
                              capture_output=True, timeout=5)
        print(f"{host}: {'OK' if result.returncode == 0 else 'FAILED'}")
    except Exception as e:
        print(f"{host}: ERROR - {e}")
''',
            'process_monitor': '''import psutil
import time

print("Top 5 processes by CPU usage:")
for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                   key=lambda p: p.info['cpu_percent'], reverse=True)[:5]:
    print(f"{proc.info['pid']}: {proc.info['name']} - {proc.info['cpu_percent']}%")
'''
        },
        'bash': {
            'disk_space': '''#!/bin/bash
# Check disk space
df -h
''',
            'network_test': '''#!/bin/bash
# Test network connectivity
for host in 8.8.8.8 1.1.1.1 google.com; do
    if ping -c 1 $host &> /dev/null; then
        echo "$host: OK"
    else
        echo "$host: FAILED"
    fi
done
'''
        }
    }
    
    @staticmethod
    def generate(description: str, script_type: str = 'powershell', ai_engine=None, language: str = 'th') -> Dict[str, Any]:
        """Generate script based on description."""
        result = {
            'status': 'success',
            'script_type': script_type,
            'timestamp': datetime.utcnow().isoformat(),
            'code': '',
            'description': description,
            'language': language,
            'template_used': False
        }
        
        # Try to find matching template
        keywords = description.lower().split()
        
        if script_type in ScriptGenerator.TEMPLATES:
            for template_name, template_code in ScriptGenerator.TEMPLATES[script_type].items():
                if any(keyword in template_name for keyword in keywords):
                    result['code'] = template_code
                    result['template_used'] = True
                    return result
        
        # Use AI if template not found and AI engine available
        if ai_engine:
            try:
                code = ai_engine.generate_script(
                    description,
                    script_language=script_type,
                    lang=language
                )
                result['code'] = code
            except Exception as e:
                result['error'] = f'Failed to generate script: {str(e)}'
        else:
            # Default template
            result['code'] = f"# {description}\n# TODO: Implement script\n"
        
        return result
    
    @staticmethod
    def validate_syntax(code: str, language: str) -> Dict[str, Any]:
        """Validate script syntax."""
        result = {
            'valid': False,
            'language': language,
            'errors': []
        }
        
        try:
            if language == 'python':
                compile(code, '<string>', 'exec')
                result['valid'] = True
            elif language == 'powershell':
                # Basic PowerShell validation
                if '{' in code and '}' not in code:
                    result['errors'].append('Mismatched braces')
                elif '(' in code and ')' not in code:
                    result['errors'].append('Mismatched parentheses')
                else:
                    result['valid'] = True
            else:
                result['valid'] = True
        except SyntaxError as e:
            result['errors'].append(str(e))
        
        return result
    
    @staticmethod
    def get_templates(script_type: str) -> List[str]:
        """Get available templates for script type."""
        if script_type in ScriptGenerator.TEMPLATES:
            return list(ScriptGenerator.TEMPLATES[script_type].keys())
        return []
