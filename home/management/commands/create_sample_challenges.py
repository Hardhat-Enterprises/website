from django.core.management.base import BaseCommand
from home.models import CyberChallenge

class Command(BaseCommand):
    help = 'Create sample cyber challenges for testing'

    def handle(self, *args, **options):
        # Sample challenges for each category
        challenges_data = [
            # Crypto challenges
            {
                'title': 'Caesar Cipher Basics',
                'description': 'Learn about the classic Caesar cipher encryption method',
                'question': 'In a Caesar cipher with shift 3, what does "A" become?',
                'choices': ['B', 'C', 'D', 'E'],
                'correct_answer': 'D',
                'difficulty': 'easy',
                'category': 'crypto',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'In Caesar cipher, each letter is shifted by a fixed number. With shift 3, A becomes D.'
            },
            {
                'title': 'Hash Functions',
                'description': 'Understand the basics of cryptographic hash functions',
                'question': 'Which of the following is NOT a property of a good hash function?',
                'choices': ['Deterministic', 'One-way', 'Reversible', 'Fixed output length'],
                'correct_answer': 'Reversible',
                'difficulty': 'easy',
                'category': 'crypto',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Hash functions are designed to be one-way, meaning they should not be reversible.'
            },
            {
                'title': 'Symmetric vs Asymmetric Encryption',
                'description': 'Compare symmetric and asymmetric encryption methods',
                'question': 'Which encryption method uses the same key for encryption and decryption?',
                'choices': ['Asymmetric', 'Symmetric', 'Both', 'Neither'],
                'correct_answer': 'Symmetric',
                'difficulty': 'easy',
                'category': 'crypto',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Symmetric encryption uses the same key for both encryption and decryption.'
            },
            {
                'title': 'Digital Signatures',
                'description': 'Learn about digital signatures and their importance',
                'question': 'What is the primary purpose of a digital signature?',
                'choices': ['Encryption', 'Authentication', 'Compression', 'Storage'],
                'correct_answer': 'Authentication',
                'difficulty': 'easy',
                'category': 'crypto',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Digital signatures are used to authenticate the sender and ensure message integrity.'
            },
            {
                'title': 'Public Key Infrastructure',
                'description': 'Understand PKI and certificate management',
                'question': 'What does PKI stand for?',
                'choices': ['Private Key Infrastructure', 'Public Key Infrastructure', 'Personal Key Infrastructure', 'Protected Key Infrastructure'],
                'correct_answer': 'Public Key Infrastructure',
                'difficulty': 'easy',
                'category': 'crypto',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'PKI stands for Public Key Infrastructure, which manages digital certificates.'
            },
            {
                'title': 'Advanced Cryptanalysis',
                'description': 'Explore advanced techniques for breaking cryptographic systems',
                'question': 'Which attack exploits the birthday paradox?',
                'choices': ['Brute force', 'Birthday attack', 'Man-in-the-middle', 'Dictionary attack'],
                'correct_answer': 'Birthday attack',
                'difficulty': 'hard',
                'category': 'crypto',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Birthday attacks exploit the birthday paradox to find hash collisions.'
            },
            {
                'title': 'Quantum Cryptography',
                'description': 'Introduction to quantum-resistant cryptographic methods',
                'question': 'What is the main advantage of quantum cryptography?',
                'choices': ['Faster encryption', 'Unbreakable security', 'Smaller keys', 'Lower cost'],
                'correct_answer': 'Unbreakable security',
                'difficulty': 'hard',
                'category': 'crypto',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Quantum cryptography theoretically provides unbreakable security through quantum mechanics.'
            },
            {
                'title': 'Advanced Encryption Standards',
                'description': 'Deep dive into AES encryption standards',
                'question': 'How many rounds does AES-128 use?',
                'choices': ['10', '12', '14', '16'],
                'correct_answer': '10',
                'difficulty': 'hard',
                'category': 'crypto',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'AES-128 uses 10 rounds, AES-192 uses 12 rounds, and AES-256 uses 14 rounds.'
            },
            {
                'title': 'Cryptographic Protocol Vulnerabilities',
                'description': 'Identify vulnerabilities in cryptographic protocols',
                'question': 'Which vulnerability affects SSL/TLS implementations?',
                'choices': ['Heartbleed', 'Shellshock', 'Meltdown', 'Spectre'],
                'correct_answer': 'Heartbleed',
                'difficulty': 'hard',
                'category': 'crypto',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Heartbleed is a vulnerability in OpenSSL that affects SSL/TLS implementations.'
            },
            {
                'title': 'Cryptographic Key Management',
                'description': 'Best practices for managing cryptographic keys',
                'question': 'What is the recommended key length for RSA encryption?',
                'choices': ['1024 bits', '2048 bits', '4096 bits', '8192 bits'],
                'correct_answer': '2048 bits',
                'difficulty': 'medium',
                'category': 'crypto',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': '2048 bits is the current recommended minimum key length for RSA encryption.'
            },
            {
                'title': 'Block Cipher Modes',
                'description': 'Understand different modes of operation for block ciphers',
                'question': 'Which mode provides both confidentiality and authentication?',
                'choices': ['CBC', 'ECB', 'GCM', 'CFB'],
                'correct_answer': 'GCM',
                'difficulty': 'medium',
                'category': 'crypto',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'GCM (Galois/Counter Mode) provides both confidentiality and authentication.'
            },
            {
                'title': 'Cryptographic Randomness',
                'description': 'Importance of randomness in cryptographic systems',
                'question': 'What is a cryptographically secure random number generator?',
                'choices': ['Predictable', 'Unpredictable', 'Fast', 'Slow'],
                'correct_answer': 'Unpredictable',
                'difficulty': 'medium',
                'category': 'crypto',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'A cryptographically secure RNG must be unpredictable and pass statistical tests.'
            },
            {
                'title': 'Elliptic Curve Cryptography',
                'description': 'Introduction to ECC and its advantages',
                'question': 'What is the main advantage of ECC over RSA?',
                'choices': ['Faster computation', 'Smaller key sizes', 'Better security', 'All of the above'],
                'correct_answer': 'All of the above',
                'difficulty': 'medium',
                'category': 'crypto',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'ECC provides faster computation, smaller key sizes, and better security than RSA.'
            },
            {
                'title': 'Cryptographic Hash Collisions',
                'description': 'Understanding hash collisions and their implications',
                'question': 'What happens when a hash collision occurs?',
                'choices': ['Nothing', 'Security breach', 'Performance improvement', 'Key generation'],
                'correct_answer': 'Security breach',
                'difficulty': 'medium',
                'category': 'crypto',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Hash collisions can lead to security breaches as they compromise the integrity of hash functions.'
            },
            {
                'title': 'Zero-Knowledge Proofs',
                'description': 'Introduction to zero-knowledge proof systems',
                'question': 'What is the main property of zero-knowledge proofs?',
                'choices': ['Speed', 'Privacy', 'Simplicity', 'Cost'],
                'correct_answer': 'Privacy',
                'difficulty': 'hard',
                'category': 'crypto',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Zero-knowledge proofs allow proving knowledge without revealing the knowledge itself.'
            },

            # Network challenges
            {
                'title': 'Firewall Basics',
                'description': 'Learn about firewall configuration and management',
                'question': 'What is the default action of a firewall when no rules match?',
                'choices': ['Allow', 'Deny', 'Log', 'Redirect'],
                'correct_answer': 'Deny',
                'difficulty': 'easy',
                'category': 'network',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Firewalls typically deny traffic by default when no explicit rules allow it.'
            },
            {
                'title': 'Intrusion Detection Systems',
                'description': 'Understand IDS and their role in network security',
                'question': 'What does IDS stand for?',
                'choices': ['Intrusion Detection System', 'Internet Defense System', 'Internal Data Security', 'Intrusion Defense Service'],
                'correct_answer': 'Intrusion Detection System',
                'difficulty': 'easy',
                'category': 'network',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'IDS stands for Intrusion Detection System, which monitors network traffic for suspicious activity.'
            },
            {
                'title': 'Network Protocols',
                'description': 'Learn about secure network protocols',
                'question': 'Which protocol provides secure communication over HTTP?',
                'choices': ['HTTP', 'HTTPS', 'FTP', 'SMTP'],
                'correct_answer': 'HTTPS',
                'difficulty': 'easy',
                'category': 'network',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'HTTPS (HTTP Secure) provides encrypted communication over HTTP using SSL/TLS.'
            },
            {
                'title': 'VPN Technology',
                'description': 'Understanding Virtual Private Networks',
                'question': 'What is the primary purpose of a VPN?',
                'choices': ['Speed up internet', 'Secure remote access', 'Block ads', 'Monitor traffic'],
                'correct_answer': 'Secure remote access',
                'difficulty': 'easy',
                'category': 'network',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'VPNs provide secure remote access to private networks over public networks.'
            },
            {
                'title': 'Network Segmentation',
                'description': 'Learn about network segmentation strategies',
                'question': 'What is network segmentation?',
                'choices': ['Dividing network into smaller parts', 'Increasing network speed', 'Reducing costs', 'Adding users'],
                'correct_answer': 'Dividing network into smaller parts',
                'difficulty': 'easy',
                'category': 'network',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Network segmentation divides a network into smaller, isolated segments for better security.'
            },
            {
                'title': 'Advanced Firewall Rules',
                'description': 'Complex firewall rule configuration',
                'question': 'Which firewall rule allows SSH traffic from specific IP?',
                'choices': ['iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT', 'iptables -A INPUT -p tcp --dport 80 -j ACCEPT', 'iptables -A INPUT -j DROP', 'iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT'],
                'correct_answer': 'iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT',
                'difficulty': 'hard',
                'category': 'network',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'This rule allows SSH (port 22) traffic from the 192.168.1.0/24 network.'
            },
            {
                'title': 'Network Forensics',
                'description': 'Investigation techniques for network attacks',
                'question': 'What tool is commonly used for network packet analysis?',
                'choices': ['Wireshark', 'Nmap', 'Metasploit', 'Burp Suite'],
                'correct_answer': 'Wireshark',
                'difficulty': 'hard',
                'category': 'network',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Wireshark is a network protocol analyzer used for packet capture and analysis.'
            },
            {
                'title': 'Advanced IDS Evasion',
                'description': 'Techniques used to evade intrusion detection',
                'question': 'What is fragmentation used for in IDS evasion?',
                'choices': ['Speed up attacks', 'Bypass detection', 'Improve performance', 'Reduce costs'],
                'correct_answer': 'Bypass detection',
                'difficulty': 'hard',
                'category': 'network',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Fragmentation is used to split attacks into smaller pieces to evade IDS detection.'
            },
            {
                'title': 'Network Security Architecture',
                'description': 'Design secure network architectures',
                'question': 'What is the principle of least privilege in network design?',
                'choices': ['Give maximum access', 'Give minimum necessary access', 'No access control', 'Random access'],
                'correct_answer': 'Give minimum necessary access',
                'difficulty': 'hard',
                'category': 'network',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Least privilege means giving users only the minimum access necessary to perform their tasks.'
            },
            {
                'title': 'Network Monitoring',
                'description': 'Implement comprehensive network monitoring',
                'question': 'What is SNMP used for in network monitoring?',
                'choices': ['Encryption', 'Network management', 'Authentication', 'Compression'],
                'correct_answer': 'Network management',
                'difficulty': 'medium',
                'category': 'network',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'SNMP (Simple Network Management Protocol) is used for network device management and monitoring.'
            },
            {
                'title': 'Wireless Security',
                'description': 'Secure wireless network configurations',
                'question': 'Which wireless security protocol is most secure?',
                'choices': ['WEP', 'WPA', 'WPA2', 'WPA3'],
                'correct_answer': 'WPA3',
                'difficulty': 'medium',
                'category': 'network',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'WPA3 is the most recent and secure wireless security protocol.'
            },
            {
                'title': 'Network Access Control',
                'description': 'Implement network access control mechanisms',
                'question': 'What does NAC stand for?',
                'choices': ['Network Access Control', 'Network Authentication Center', 'Network Administration Console', 'Network Audit Committee'],
                'correct_answer': 'Network Access Control',
                'difficulty': 'medium',
                'category': 'network',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'NAC stands for Network Access Control, which manages device access to network resources.'
            },
            {
                'title': 'Network Threat Intelligence',
                'description': 'Use threat intelligence for network security',
                'question': 'What is the primary source of network threat intelligence?',
                'choices': ['Social media', 'Security feeds', 'News websites', 'Blogs'],
                'correct_answer': 'Security feeds',
                'difficulty': 'medium',
                'category': 'network',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Security feeds provide real-time threat intelligence about network attacks and vulnerabilities.'
            },
            {
                'title': 'Network Incident Response',
                'description': 'Respond to network security incidents',
                'question': 'What is the first step in network incident response?',
                'choices': ['Containment', 'Identification', 'Recovery', 'Lessons learned'],
                'correct_answer': 'Identification',
                'difficulty': 'medium',
                'category': 'network',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Identification is the first step in incident response - detecting and confirming the incident.'
            },

            # Web challenges
            {
                'title': 'SQL Injection Basics',
                'description': 'Learn about SQL injection vulnerabilities',
                'question': 'What is SQL injection?',
                'choices': ['Database optimization', 'Code injection attack', 'Network protocol', 'Encryption method'],
                'correct_answer': 'Code injection attack',
                'difficulty': 'easy',
                'category': 'web',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'SQL injection is a code injection attack that exploits vulnerabilities in database queries.'
            },
            {
                'title': 'Cross-Site Scripting (XSS)',
                'description': 'Understand XSS vulnerabilities and prevention',
                'question': 'What does XSS stand for?',
                'choices': ['Cross-Site Scripting', 'Cross-Site Security', 'Cross-Site Session', 'Cross-Site Storage'],
                'correct_answer': 'Cross-Site Scripting',
                'difficulty': 'easy',
                'category': 'web',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'XSS stands for Cross-Site Scripting, a vulnerability that allows injecting malicious scripts.'
            },
            {
                'title': 'CSRF Attacks',
                'description': 'Learn about Cross-Site Request Forgery',
                'question': 'What does CSRF stand for?',
                'choices': ['Cross-Site Request Forgery', 'Cross-Site Resource Forgery', 'Cross-Site Response Forgery', 'Cross-Site Routing Forgery'],
                'correct_answer': 'Cross-Site Request Forgery',
                'difficulty': 'easy',
                'category': 'web',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'CSRF stands for Cross-Site Request Forgery, where unauthorized commands are transmitted from a user.'
            },
            {
                'title': 'Web Application Firewalls',
                'description': 'Understand WAF and its role in web security',
                'question': 'What does WAF stand for?',
                'choices': ['Web Application Firewall', 'Web Access Filter', 'Web Authentication Framework', 'Web Attack Filter'],
                'correct_answer': 'Web Application Firewall',
                'difficulty': 'easy',
                'category': 'web',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'WAF stands for Web Application Firewall, which filters HTTP traffic to web applications.'
            },
            {
                'title': 'Secure Coding Practices',
                'description': 'Learn secure coding practices for web applications',
                'question': 'What is input validation?',
                'choices': ['Checking user input', 'Encrypting data', 'Compressing files', 'Optimizing code'],
                'correct_answer': 'Checking user input',
                'difficulty': 'easy',
                'category': 'web',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Input validation is the process of checking and sanitizing user input to prevent attacks.'
            },
            {
                'title': 'Advanced SQL Injection',
                'description': 'Complex SQL injection techniques and defenses',
                'question': 'Which SQL injection technique uses UNION?',
                'choices': ['Blind SQL injection', 'Union-based injection', 'Time-based injection', 'Boolean-based injection'],
                'correct_answer': 'Union-based injection',
                'difficulty': 'hard',
                'category': 'web',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Union-based injection uses the UNION operator to combine results from different tables.'
            },
            {
                'title': 'Advanced XSS Techniques',
                'description': 'Complex XSS attack vectors and prevention',
                'question': 'What is DOM-based XSS?',
                'choices': ['Server-side XSS', 'Client-side XSS', 'Database XSS', 'Network XSS'],
                'correct_answer': 'Client-side XSS',
                'difficulty': 'hard',
                'category': 'web',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'DOM-based XSS is a client-side vulnerability where the attack is executed in the DOM.'
            },
            {
                'title': 'Web Application Security Testing',
                'description': 'Comprehensive web application security assessment',
                'question': 'What is OWASP ZAP used for?',
                'choices': ['Database management', 'Web application security testing', 'Network monitoring', 'Code compilation'],
                'correct_answer': 'Web application security testing',
                'difficulty': 'hard',
                'category': 'web',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'OWASP ZAP is a web application security testing tool for finding vulnerabilities.'
            },
            {
                'title': 'API Security',
                'description': 'Secure API design and implementation',
                'question': 'What is API rate limiting used for?',
                'choices': ['Speed up APIs', 'Prevent abuse', 'Reduce costs', 'Improve performance'],
                'correct_answer': 'Prevent abuse',
                'difficulty': 'hard',
                'category': 'web',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'API rate limiting prevents abuse by limiting the number of requests per user/time period.'
            },
            {
                'title': 'Web Security Headers',
                'description': 'Implement security headers for web applications',
                'question': 'What does CSP stand for?',
                'choices': ['Content Security Policy', 'Cross-Site Protection', 'Content Service Protocol', 'Cross-Site Policy'],
                'correct_answer': 'Content Security Policy',
                'difficulty': 'medium',
                'category': 'web',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'CSP stands for Content Security Policy, a security standard for preventing XSS attacks.'
            },
            {
                'title': 'Session Management',
                'description': 'Secure session handling in web applications',
                'question': 'What is session hijacking?',
                'choices': ['Creating sessions', 'Stealing session tokens', 'Ending sessions', 'Managing sessions'],
                'correct_answer': 'Stealing session tokens',
                'difficulty': 'medium',
                'category': 'web',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Session hijacking involves stealing session tokens to impersonate users.'
            },
            {
                'title': 'Authentication Security',
                'description': 'Implement secure authentication mechanisms',
                'question': 'What is multi-factor authentication?',
                'choices': ['Single password', 'Multiple passwords', 'Multiple verification methods', 'Single verification'],
                'correct_answer': 'Multiple verification methods',
                'difficulty': 'medium',
                'category': 'web',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'MFA uses multiple verification methods (password + token/SMS/biometric) for authentication.'
            },
            {
                'title': 'Web Vulnerability Scanning',
                'description': 'Automated web vulnerability detection',
                'question': 'What is Burp Suite used for?',
                'choices': ['Database management', 'Web application testing', 'Network monitoring', 'Code analysis'],
                'correct_answer': 'Web application testing',
                'difficulty': 'medium',
                'category': 'web',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Burp Suite is a web application security testing platform.'
            },
            {
                'title': 'Web Application Architecture Security',
                'description': 'Design secure web application architectures',
                'question': 'What is defense in depth?',
                'choices': ['Single security layer', 'Multiple security layers', 'No security', 'Basic security'],
                'correct_answer': 'Multiple security layers',
                'difficulty': 'medium',
                'category': 'web',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Defense in depth uses multiple security layers to protect against various attack vectors.'
            },

            # General challenges
            {
                'title': 'Cybersecurity Fundamentals',
                'description': 'Basic concepts in cybersecurity',
                'question': 'What is the CIA triad?',
                'choices': ['Confidentiality, Integrity, Availability', 'Confidentiality, Information, Access', 'Control, Integrity, Access', 'Confidentiality, Integrity, Authentication'],
                'correct_answer': 'Confidentiality, Integrity, Availability',
                'difficulty': 'easy',
                'category': 'general',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'The CIA triad represents Confidentiality, Integrity, and Availability - the core principles of cybersecurity.'
            },
            {
                'title': 'Threat Modeling',
                'description': 'Understand threat modeling methodologies',
                'question': 'What is STRIDE used for?',
                'choices': ['Encryption', 'Threat modeling', 'Network scanning', 'Code analysis'],
                'correct_answer': 'Threat modeling',
                'difficulty': 'easy',
                'category': 'general',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'STRIDE is a threat modeling methodology that categorizes threats into six categories.'
            },
            {
                'title': 'Risk Assessment',
                'description': 'Learn about cybersecurity risk assessment',
                'question': 'What is risk in cybersecurity?',
                'choices': ['Certainty of attack', 'Probability of threat × Impact', 'Cost of security', 'Number of vulnerabilities'],
                'correct_answer': 'Probability of threat × Impact',
                'difficulty': 'easy',
                'category': 'general',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Risk is calculated as the probability of a threat occurring multiplied by its potential impact.'
            },
            {
                'title': 'Security Policies',
                'description': 'Develop and implement security policies',
                'question': 'What is a security policy?',
                'choices': ['Technical controls', 'Guidelines for security', 'Hardware devices', 'Software programs'],
                'correct_answer': 'Guidelines for security',
                'difficulty': 'easy',
                'category': 'general',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Security policies are guidelines and rules that define how an organization approaches security.'
            },
            {
                'title': 'Incident Response',
                'description': 'Plan and execute incident response procedures',
                'question': 'What is the first phase of incident response?',
                'choices': ['Preparation', 'Detection', 'Containment', 'Recovery'],
                'correct_answer': 'Preparation',
                'difficulty': 'easy',
                'category': 'general',
                'points': 10,
                'challenge_type': 'mcq',
                'explanation': 'Preparation is the first phase, involving planning, training, and tool preparation.'
            },
            {
                'title': 'Advanced Threat Intelligence',
                'description': 'Use threat intelligence for security operations',
                'question': 'What is APT?',
                'choices': ['Advanced Persistent Threat', 'Automated Penetration Testing', 'Application Performance Testing', 'Advanced Protection Technology'],
                'correct_answer': 'Advanced Persistent Threat',
                'difficulty': 'hard',
                'category': 'general',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'APT stands for Advanced Persistent Threat - sophisticated, long-term cyber attacks.'
            },
            {
                'title': 'Security Architecture Design',
                'description': 'Design comprehensive security architectures',
                'question': 'What is zero trust architecture?',
                'choices': ['No security', 'Trust but verify', 'Never trust, always verify', 'Trust everyone'],
                'correct_answer': 'Never trust, always verify',
                'difficulty': 'hard',
                'category': 'general',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'Zero trust architecture follows the principle of never trust, always verify.'
            },
            {
                'title': 'Compliance and Regulations',
                'description': 'Understand cybersecurity compliance requirements',
                'question': 'What does GDPR stand for?',
                'choices': ['General Data Protection Regulation', 'Global Data Protection Rules', 'General Data Privacy Rules', 'Global Data Privacy Regulation'],
                'correct_answer': 'General Data Protection Regulation',
                'difficulty': 'hard',
                'category': 'general',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'GDPR stands for General Data Protection Regulation, EU data protection law.'
            },
            {
                'title': 'Security Operations Center',
                'description': 'Manage Security Operations Center (SOC)',
                'question': 'What is SIEM?',
                'choices': ['Security Information and Event Management', 'Security Intelligence and Event Monitoring', 'Security Information and Event Monitoring', 'Security Intelligence and Event Management'],
                'correct_answer': 'Security Information and Event Management',
                'difficulty': 'hard',
                'category': 'general',
                'points': 30,
                'challenge_type': 'mcq',
                'explanation': 'SIEM stands for Security Information and Event Management, used for security monitoring.'
            },
            {
                'title': 'Security Awareness Training',
                'description': 'Develop and deliver security awareness programs',
                'question': 'What is the most common attack vector?',
                'choices': ['Technical vulnerabilities', 'Social engineering', 'Physical access', 'Network attacks'],
                'correct_answer': 'Social engineering',
                'difficulty': 'medium',
                'category': 'general',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Social engineering is the most common attack vector, exploiting human psychology.'
            },
            {
                'title': 'Security Metrics and KPIs',
                'description': 'Measure and improve security performance',
                'question': 'What is MTTR?',
                'choices': ['Mean Time To Recovery', 'Mean Time To Response', 'Mean Time To Repair', 'Mean Time To Resolution'],
                'correct_answer': 'Mean Time To Recovery',
                'difficulty': 'medium',
                'category': 'general',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'MTTR stands for Mean Time To Recovery - average time to recover from incidents.'
            },
            {
                'title': 'Security Governance',
                'description': 'Implement security governance frameworks',
                'question': 'What is COBIT used for?',
                'choices': ['Network security', 'IT governance', 'Application security', 'Physical security'],
                'correct_answer': 'IT governance',
                'difficulty': 'medium',
                'category': 'general',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'COBIT is a framework for IT governance and management.'
            },
            {
                'title': 'Security Risk Management',
                'description': 'Implement comprehensive risk management',
                'question': 'What is residual risk?',
                'choices': ['Original risk', 'Risk after controls', 'New risk', 'Eliminated risk'],
                'correct_answer': 'Risk after controls',
                'difficulty': 'medium',
                'category': 'general',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'Residual risk is the risk remaining after implementing security controls.'
            },
            {
                'title': 'Security Program Management',
                'description': 'Manage enterprise security programs',
                'question': 'What is the primary goal of a security program?',
                'choices': ['Reduce costs', 'Protect assets', 'Increase speed', 'Improve performance'],
                'correct_answer': 'Protect assets',
                'difficulty': 'medium',
                'category': 'general',
                'points': 15,
                'challenge_type': 'mcq',
                'explanation': 'The primary goal of a security program is to protect organizational assets.'
            }
        ]

        # Create challenges
        created_count = 0
        for challenge_data in challenges_data:
            challenge, created = CyberChallenge.objects.get_or_create(
                title=challenge_data['title'],
                defaults=challenge_data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} cyber challenges')
        )
