import datetime
import random

class ForensicReportGenerator:
    def __init__(self):
        self.report_data = {}

    def collect_data(self, exploit_data):
        self.report_data = exploit_data

    def generate_report(self):
        report = f"""
PHANTOM EXPLOIT FRAMEWORK - FORENSIC REPORT
===========================================
Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Target Information:
-------------------
IP Address: {self.report_data.get('target_ip', 'Unknown')}
Operating System: {self.report_data.get('os', 'Unknown')}
Open Ports: {', '.join(map(str, self.report_data.get('open_ports', [])))}

Exploit Details:
----------------
Exploit Type: {self.report_data.get('exploit_type', 'Unknown')}
Packets Sent: {self.report_data.get('packets_sent', 0)}
Execution Time: {self.report_data.get('execution_time', 0)} seconds

Vulnerabilities Detected:
-------------------------
"""
        for vuln in self.report_data.get('vulnerabilities', []):
            report += f"- {vuln['name']}: {vuln['description']}\n"

        report += f"""
Network Analysis:
-----------------
Suspicious Patterns Detected: {self.report_data.get('suspicious_patterns', 'None')}

System Recovery:
----------------
Backup Created: {'Yes' if self.report_data.get('backup_created', False) else 'No'}
Rollback Performed: {'Yes' if self.report_data.get('rollback_performed', False) else 'No'}
System Integrity: {self.report_data.get('system_integrity', 'Unknown')}

Recommendations:
----------------
1. Patch all detected vulnerabilities immediately.
2. Strengthen firewall rules to prevent unauthorized access.
3. Implement regular security audits to identify potential weaknesses.
4. Educate users about social engineering and phishing attacks.
5. Keep all software and systems up to date with the latest security patches.

DISCLAIMER: This report is generated for educational purposes only. 
The use of this information to attack systems you do not own is illegal.
"""
        return report

