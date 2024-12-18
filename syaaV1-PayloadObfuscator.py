import base64
import random
import string

class PayloadObfuscator:
    @staticmethod
    def obfuscate(payload: str) -> str:
        # Base64 encode
        encoded = base64.b64encode(payload.encode()).decode()
        
        # Add random noise
        noise = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        obfuscated = noise + encoded + noise[::-1]
        
        # Reverse
        return obfuscated[::-1]

    @staticmethod
    def deobfuscate(obfuscated: str) -> str:
        # Reverse
        reversed_str = obfuscated[::-1]
        
        # Remove noise
        encoded = reversed_str[10:-10]
        
        # Base64 decode
        return base64.b64decode(encoded).decode()

