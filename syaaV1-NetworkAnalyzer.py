import random
from collections import defaultdict

class NetworkAnalyzer:
    def __init__(self):
        self.traffic_patterns = defaultdict(int)

    def analyze_traffic(self, packets):
        for packet in packets:
            self.traffic_patterns[packet['protocol']] += 1

        suspicious_patterns = self.detect_suspicious_patterns()
        return suspicious_patterns

    def detect_suspicious_patterns(self):
        suspicious = []
        for protocol, count in self.traffic_patterns.items():
            if count > 100:  # Threshold for suspicious activity
                suspicious.append(f"Suspicious activity detected on {protocol}: {count} packets")
        return suspicious

    def generate_mock_traffic(self, num_packets):
        protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'DNS']
        return [{'protocol': random.choice(protocols)} for _ in range(num_packets)]

