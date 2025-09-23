from django.core.management.base import BaseCommand
from home.models import Quiz, QuizQuestion

class Command(BaseCommand):
    help = 'Populate the database with quiz questions for all categories'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate quiz questions...')
        
        # Create quizzes for each category
        quiz_data = [
            {
                'title': 'Network Security Quiz',
                'category': 'network',
                'description': 'Test your knowledge of network security fundamentals, protocols, and best practices.'
            },
            {
                'title': 'Web Application Security Quiz',
                'category': 'web',
                'description': 'Challenge yourself with web security concepts, vulnerabilities, and protection mechanisms.'
            },
            {
                'title': 'Cryptography Quiz',
                'category': 'crypto',
                'description': 'Explore encryption, hashing, digital signatures, and cryptographic protocols.'
            },
            {
                'title': 'General Cybersecurity Quiz',
                'category': 'general',
                'description': 'Broad cybersecurity knowledge covering various domains and best practices.'
            }
        ]

        for quiz_info in quiz_data:
            quiz, created = Quiz.objects.get_or_create(
                category=quiz_info['category'],
                defaults={
                    'title': quiz_info['title'],
                    'description': quiz_info['description'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created quiz: {quiz.title}')
            else:
                self.stdout.write(f'Quiz already exists: {quiz.title}')

        # Network Security Questions
        network_questions = [
            # Easy Questions
            {
                'question_text': 'What does VPN stand for?',
                'option_a': 'Virtual Private Network',
                'option_b': 'Very Private Network',
                'option_c': 'Virtual Public Network',
                'option_d': 'Verified Private Network',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'VPN stands for Virtual Private Network, which creates a secure connection over the internet.'
            },
            {
                'question_text': 'What is the primary purpose of a firewall?',
                'option_a': 'To increase internet speed',
                'option_b': 'To prevent unauthorized access',
                'option_c': 'To store files securely',
                'option_d': 'To encrypt data',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'A firewall\'s main purpose is to prevent unauthorized access to or from a private network.'
            },
            {
                'question_text': 'Which port is commonly used for HTTPS?',
                'option_a': '80',
                'option_b': '443',
                'option_c': '21',
                'option_d': '25',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Port 443 is the standard port for HTTPS (HTTP Secure) traffic.'
            },
            {
                'question_text': 'What does DNS stand for?',
                'option_a': 'Domain Name System',
                'option_b': 'Dynamic Network Service',
                'option_c': 'Digital Network Security',
                'option_d': 'Data Name Server',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'DNS stands for Domain Name System, which translates domain names to IP addresses.'
            },
            {
                'question_text': 'Which protocol is used for secure email transmission?',
                'option_a': 'HTTP',
                'option_b': 'FTP',
                'option_c': 'SMTP',
                'option_d': 'SMTPS',
                'correct_answer': 'd',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'SMTPS (SMTP Secure) is used for secure email transmission over SSL/TLS.'
            },
            # Medium Questions
            {
                'question_text': 'What is the main difference between IDS and IPS?',
                'option_a': 'IDS detects, IPS prevents',
                'option_b': 'IDS prevents, IPS detects',
                'option_c': 'No difference',
                'option_d': 'IDS is cheaper than IPS',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'IDS (Intrusion Detection System) detects threats, while IPS (Intrusion Prevention System) can also prevent them.'
            },
            {
                'question_text': 'Which network topology is most resilient to single point of failure?',
                'option_a': 'Star',
                'option_b': 'Bus',
                'option_c': 'Mesh',
                'option_d': 'Ring',
                'correct_answer': 'c',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Mesh topology provides multiple paths between nodes, making it most resilient to failures.'
            },
            {
                'question_text': 'What does NAT stand for and what is its primary function?',
                'option_a': 'Network Address Translation - translates private IPs to public IPs',
                'option_b': 'Network Access Technology - manages network access',
                'option_c': 'Network Authentication Tool - authenticates users',
                'option_d': 'Network Analysis Tool - analyzes network traffic',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'NAT (Network Address Translation) translates private IP addresses to public IP addresses.'
            },
            {
                'question_text': 'Which protocol is used for secure remote access to network devices?',
                'option_a': 'Telnet',
                'option_b': 'HTTP',
                'option_c': 'SSH',
                'option_d': 'FTP',
                'correct_answer': 'c',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'SSH (Secure Shell) provides encrypted remote access to network devices.'
            },
            {
                'question_text': 'What is the purpose of VLANs in network security?',
                'option_a': 'To increase network speed',
                'option_b': 'To segment network traffic',
                'option_c': 'To encrypt data',
                'option_d': 'To authenticate users',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'VLANs (Virtual LANs) segment network traffic for better security and management.'
            },
            # Hard Questions
            {
                'question_text': 'What is the main vulnerability in WEP encryption?',
                'option_a': 'Weak key generation',
                'option_b': 'Static IV (Initialization Vector)',
                'option_c': 'Short key length',
                'option_d': 'All of the above',
                'correct_answer': 'd',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'WEP has multiple vulnerabilities including weak key generation, static IVs, and short key lengths.'
            },
            {
                'question_text': 'In BGP hijacking, what type of attack is typically performed?',
                'option_a': 'Man-in-the-middle',
                'option_b': 'Route hijacking',
                'option_c': 'DDoS',
                'option_d': 'SQL injection',
                'correct_answer': 'b',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'BGP hijacking involves maliciously announcing routes to redirect traffic.'
            },
            {
                'question_text': 'What is the primary security concern with IPv6?',
                'option_a': 'Larger address space',
                'option_b': 'Lack of NAT',
                'option_c': 'No encryption',
                'option_d': 'Slower processing',
                'correct_answer': 'b',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'IPv6\'s lack of NAT means all devices have globally routable addresses, increasing attack surface.'
            },
            {
                'question_text': 'Which attack exploits the three-way handshake in TCP?',
                'option_a': 'SYN flood',
                'option_b': 'Ping of death',
                'option_c': 'Smurf attack',
                'option_d': 'Land attack',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'SYN flood attack exploits the TCP three-way handshake by sending SYN packets without completing the handshake.'
            },
            {
                'question_text': 'What is the main difference between stateful and stateless firewalls?',
                'option_a': 'Stateful tracks connections, stateless doesn\'t',
                'option_b': 'Stateless is more secure',
                'option_c': 'No difference',
                'option_d': 'Stateful is slower',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Stateful firewalls track connection states, while stateless firewalls examine each packet independently.'
            }
        ]

        # Web Application Security Questions
        web_questions = [
            # Easy Questions
            {
                'question_text': 'What does XSS stand for?',
                'option_a': 'Cross-Site Scripting',
                'option_b': 'Cross-Site Security',
                'option_c': 'Cross-Site Session',
                'option_d': 'Cross-Site Storage',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'XSS stands for Cross-Site Scripting, a vulnerability that allows injection of malicious scripts.'
            },
            {
                'question_text': 'What is the primary purpose of input validation?',
                'option_a': 'To improve performance',
                'option_b': 'To prevent malicious input',
                'option_c': 'To reduce storage',
                'option_d': 'To enhance UI',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Input validation prevents malicious input that could lead to security vulnerabilities.'
            },
            {
                'question_text': 'Which HTTP method should be used for sensitive operations?',
                'option_a': 'GET',
                'option_b': 'POST',
                'option_c': 'PUT',
                'option_d': 'DELETE',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'POST method should be used for sensitive operations as data is not visible in URL.'
            },
            {
                'question_text': 'What does CSRF stand for?',
                'option_a': 'Cross-Site Request Forgery',
                'option_b': 'Cross-Site Resource Forgery',
                'option_c': 'Cross-Site Response Forgery',
                'option_d': 'Cross-Site Routing Forgery',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'CSRF stands for Cross-Site Request Forgery, which tricks users into performing unwanted actions.'
            },
            {
                'question_text': 'Which header helps prevent XSS attacks?',
                'option_a': 'Content-Type',
                'option_b': 'Content-Security-Policy',
                'option_c': 'Cache-Control',
                'option_d': 'Authorization',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Content-Security-Policy header helps prevent XSS attacks by controlling resource loading.'
            },
            # Medium Questions
            {
                'question_text': 'What is the main difference between stored and reflected XSS?',
                'option_a': 'Stored XSS persists on server, reflected XSS doesn\'t',
                'option_b': 'Reflected XSS is more dangerous',
                'option_c': 'No difference',
                'option_d': 'Stored XSS is faster',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Stored XSS persists malicious code on the server, while reflected XSS is immediately reflected back.'
            },
            {
                'question_text': 'Which authentication method is most secure for web applications?',
                'option_a': 'Basic authentication',
                'option_b': 'Session-based authentication',
                'option_c': 'Token-based authentication',
                'option_d': 'Cookie-based authentication',
                'correct_answer': 'c',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Token-based authentication (like JWT) is generally more secure and stateless.'
            },
            {
                'question_text': 'What is the primary purpose of HTTPS in web security?',
                'option_a': 'To increase speed',
                'option_b': 'To encrypt data in transit',
                'option_c': 'To compress data',
                'option_d': 'To cache content',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'HTTPS encrypts data in transit between client and server to prevent interception.'
            },
            {
                'question_text': 'Which vulnerability allows unauthorized database access?',
                'option_a': 'XSS',
                'option_b': 'SQL Injection',
                'option_c': 'CSRF',
                'option_d': 'Clickjacking',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'SQL Injection allows attackers to manipulate database queries and access unauthorized data.'
            },
            {
                'question_text': 'What does OWASP stand for?',
                'option_a': 'Open Web Application Security Project',
                'option_b': 'Online Web Application Security Protocol',
                'option_c': 'Open Web Application Security Protocol',
                'option_d': 'Online Web Application Security Project',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'OWASP stands for Open Web Application Security Project, a nonprofit focused on web security.'
            },
            # Hard Questions
            {
                'question_text': 'What is the main challenge with implementing Content Security Policy (CSP)?',
                'option_a': 'Performance impact',
                'option_b': 'Breaking existing functionality',
                'option_c': 'Complex configuration',
                'option_d': 'All of the above',
                'correct_answer': 'd',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'CSP implementation faces challenges with performance, breaking functionality, and complex configuration.'
            },
            {
                'question_text': 'In a race condition attack, what is being exploited?',
                'option_a': 'Timing vulnerabilities',
                'option_b': 'Memory corruption',
                'option_c': 'Network delays',
                'option_d': 'CPU speed',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Race condition attacks exploit timing vulnerabilities in concurrent operations.'
            },
            {
                'question_text': 'What is the primary risk of insecure direct object references?',
                'option_a': 'Performance degradation',
                'option_b': 'Unauthorized data access',
                'option_c': 'Memory leaks',
                'option_d': 'Network congestion',
                'correct_answer': 'b',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Insecure direct object references allow unauthorized access to data by manipulating object identifiers.'
            },
            {
                'question_text': 'Which attack technique involves manipulating HTTP headers?',
                'option_a': 'Header injection',
                'option_b': 'Host header injection',
                'option_c': 'HTTP response splitting',
                'option_d': 'All of the above',
                'correct_answer': 'd',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Multiple attack techniques involve manipulating HTTP headers, including injection and splitting attacks.'
            },
            {
                'question_text': 'What is the main security concern with client-side storage?',
                'option_a': 'Size limitations',
                'option_b': 'No encryption by default',
                'option_c': 'Browser compatibility',
                'option_d': 'Performance impact',
                'correct_answer': 'b',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Client-side storage (localStorage, sessionStorage) has no encryption by default, making it vulnerable.'
            }
        ]

        # Cryptography Questions
        crypto_questions = [
            # Easy Questions
            {
                'question_text': 'What does AES stand for?',
                'option_a': 'Advanced Encryption Standard',
                'option_b': 'Automated Encryption System',
                'option_c': 'Advanced Encoding Standard',
                'option_d': 'Automated Encoding System',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'AES stands for Advanced Encryption Standard, a widely used symmetric encryption algorithm.'
            },
            {
                'question_text': 'What is the main difference between symmetric and asymmetric encryption?',
                'option_a': 'Symmetric uses one key, asymmetric uses two keys',
                'option_b': 'Asymmetric is faster',
                'option_c': 'No difference',
                'option_d': 'Symmetric is more secure',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Symmetric encryption uses one key for both encryption and decryption, while asymmetric uses a key pair.'
            },
            {
                'question_text': 'What does MD5 produce?',
                'option_a': 'A 128-bit hash',
                'option_b': 'A 256-bit hash',
                'option_c': 'A 512-bit hash',
                'option_d': 'A 1024-bit hash',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'MD5 produces a 128-bit (16-byte) hash value, though it\'s considered cryptographically broken.'
            },
            {
                'question_text': 'Which algorithm is used in Bitcoin mining?',
                'option_a': 'SHA-1',
                'option_b': 'SHA-256',
                'option_c': 'MD5',
                'option_d': 'AES',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Bitcoin uses SHA-256 for its proof-of-work algorithm in mining.'
            },
            {
                'question_text': 'What does RSA stand for?',
                'option_a': 'Rivest-Shamir-Adleman',
                'option_b': 'Random Secure Algorithm',
                'option_c': 'Rapid Security Algorithm',
                'option_d': 'Reliable Security Algorithm',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'RSA stands for Rivest-Shamir-Adleman, the surnames of its inventors.'
            },
            # Medium Questions
            {
                'question_text': 'What is the main advantage of elliptic curve cryptography?',
                'option_a': 'Faster computation',
                'option_b': 'Smaller key sizes for same security',
                'option_c': 'Better compatibility',
                'option_d': 'Lower memory usage',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'ECC provides the same security level as RSA with much smaller key sizes.'
            },
            {
                'question_text': 'What is the primary purpose of a digital certificate?',
                'option_a': 'To encrypt data',
                'option_b': 'To verify identity',
                'option_c': 'To compress files',
                'option_d': 'To authenticate users',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Digital certificates verify the identity of entities in public key cryptography.'
            },
            {
                'question_text': 'Which cryptographic primitive provides data integrity?',
                'option_a': 'Encryption',
                'option_b': 'Hashing',
                'option_c': 'Key exchange',
                'option_d': 'Random number generation',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Cryptographic hashing provides data integrity by detecting any changes to the data.'
            },
            {
                'question_text': 'What is the main vulnerability of WEP encryption?',
                'option_a': 'Weak key generation',
                'option_b': 'Static IV reuse',
                'option_c': 'Short key length',
                'option_d': 'All of the above',
                'correct_answer': 'd',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'WEP has multiple vulnerabilities including weak key generation, IV reuse, and short keys.'
            },
            {
                'question_text': 'What does PKI stand for?',
                'option_a': 'Public Key Infrastructure',
                'option_b': 'Private Key Infrastructure',
                'option_c': 'Public Key Information',
                'option_d': 'Private Key Information',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'PKI stands for Public Key Infrastructure, which manages digital certificates and keys.'
            },
            # Hard Questions
            {
                'question_text': 'What is the main challenge with quantum computing for cryptography?',
                'option_a': 'It can break current public key algorithms',
                'option_b': 'It\'s too slow',
                'option_c': 'It requires too much power',
                'option_d': 'It\'s not reliable',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Quantum computers could break current public key algorithms like RSA and ECC using Shor\'s algorithm.'
            },
            {
                'question_text': 'What is the primary security concern with hash collisions?',
                'option_a': 'Performance degradation',
                'option_b': 'Different inputs producing same output',
                'option_c': 'Memory corruption',
                'option_d': 'Network delays',
                'correct_answer': 'b',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Hash collisions occur when different inputs produce the same hash output, compromising integrity.'
            },
            {
                'question_text': 'In post-quantum cryptography, what type of algorithms are being developed?',
                'option_a': 'Quantum-resistant algorithms',
                'option_b': 'Faster classical algorithms',
                'option_c': 'Smaller key algorithms',
                'option_d': 'More complex algorithms',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Post-quantum cryptography focuses on developing algorithms resistant to quantum computer attacks.'
            },
            {
                'question_text': 'What is the main difference between CBC and GCM modes in AES?',
                'option_a': 'GCM provides authentication, CBC doesn\'t',
                'option_b': 'CBC is faster',
                'option_c': 'No difference',
                'option_d': 'GCM uses smaller keys',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'GCM (Galois/Counter Mode) provides both encryption and authentication, while CBC only provides encryption.'
            },
            {
                'question_text': 'What is the primary purpose of a key escrow system?',
                'option_a': 'To improve performance',
                'option_b': 'To allow authorized access to encrypted data',
                'option_c': 'To reduce storage',
                'option_d': 'To enhance security',
                'correct_answer': 'b',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Key escrow systems allow authorized parties to access encrypted data by storing encryption keys.'
            }
        ]

        # General Cybersecurity Questions
        general_questions = [
            # Easy Questions
            {
                'question_text': 'What is the most common type of cyber attack?',
                'option_a': 'Phishing',
                'option_b': 'DDoS',
                'option_c': 'SQL Injection',
                'option_d': 'Zero-day Exploit',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Phishing is the most common type of cyber attack, where attackers trick users into revealing sensitive information.'
            },
            {
                'question_text': 'What is two-factor authentication?',
                'option_a': 'Using two different passwords',
                'option_b': 'A security process requiring two forms of identification',
                'option_c': 'Having two security questions',
                'option_d': 'Using two different devices',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Two-factor authentication requires two different forms of identification to verify a user\'s identity.'
            },
            {
                'question_text': 'What is the best practice for creating strong passwords?',
                'option_a': 'Using personal information',
                'option_b': 'Using the same password for all accounts',
                'option_c': 'Using a combination of letters, numbers, and symbols',
                'option_d': 'Writing passwords down',
                'correct_answer': 'c',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Strong passwords should include a combination of uppercase and lowercase letters, numbers, and special symbols.'
            },
            {
                'question_text': 'What does CIA stand for in cybersecurity?',
                'option_a': 'Confidentiality, Integrity, Availability',
                'option_b': 'Central Intelligence Agency',
                'option_c': 'Computer Information Assurance',
                'option_d': 'Cyber Intelligence Analysis',
                'correct_answer': 'a',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'In cybersecurity, CIA stands for Confidentiality, Integrity, and Availability - the three core principles.'
            },
            {
                'question_text': 'What is social engineering?',
                'option_a': 'A type of programming',
                'option_b': 'Manipulating people to reveal information',
                'option_c': 'A network protocol',
                'option_d': 'A type of encryption',
                'correct_answer': 'b',
                'difficulty': 'easy',
                'points': 10,
                'explanation': 'Social engineering is the manipulation of people to reveal confidential information or perform actions.'
            },
            # Medium Questions
            {
                'question_text': 'What is the primary purpose of penetration testing?',
                'option_a': 'To fix vulnerabilities',
                'option_b': 'To identify security weaknesses',
                'option_c': 'To improve performance',
                'option_d': 'To backup data',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Penetration testing identifies security weaknesses by simulating real-world attacks.'
            },
            {
                'question_text': 'What is the main difference between a virus and a worm?',
                'option_a': 'Viruses replicate, worms don\'t',
                'option_b': 'Worms self-replicate, viruses need host programs',
                'option_c': 'No difference',
                'option_d': 'Viruses are more dangerous',
                'correct_answer': 'b',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Worms can self-replicate and spread independently, while viruses need host programs to execute.'
            },
            {
                'question_text': 'What does GDPR stand for?',
                'option_a': 'General Data Protection Regulation',
                'option_b': 'Global Data Privacy Regulation',
                'option_c': 'General Data Privacy Rule',
                'option_d': 'Global Data Protection Rule',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'GDPR stands for General Data Protection Regulation, a European data protection law.'
            },
            {
                'question_text': 'What is the primary purpose of a honeypot?',
                'option_a': 'To attract attackers',
                'option_b': 'To store honey',
                'option_c': 'To improve performance',
                'option_d': 'To encrypt data',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Honeypots are decoy systems designed to attract and detect attackers.'
            },
            {
                'question_text': 'What is zero-day vulnerability?',
                'option_a': 'A vulnerability with no patches available',
                'option_b': 'A vulnerability that occurs at midnight',
                'option_c': 'A vulnerability with zero impact',
                'option_d': 'A vulnerability that takes zero time to exploit',
                'correct_answer': 'a',
                'difficulty': 'medium',
                'points': 15,
                'explanation': 'Zero-day vulnerabilities are unknown to vendors with no patches available yet.'
            },
            # Hard Questions
            {
                'question_text': 'What is the main challenge with Advanced Persistent Threats (APTs)?',
                'option_a': 'They are difficult to detect',
                'option_b': 'They use sophisticated techniques',
                'option_c': 'They persist for long periods',
                'option_d': 'All of the above',
                'correct_answer': 'd',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'APTs are challenging because they\'re hard to detect, use sophisticated techniques, and persist for long periods.'
            },
            {
                'question_text': 'What is the primary security concern with Internet of Things (IoT) devices?',
                'option_a': 'Limited processing power',
                'option_b': 'Default credentials and lack of security updates',
                'option_c': 'Small storage capacity',
                'option_d': 'Slow network connections',
                'correct_answer': 'b',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'IoT devices often have default credentials and lack regular security updates, making them vulnerable.'
            },
            {
                'question_text': 'What is the main difference between threat modeling and risk assessment?',
                'option_a': 'Threat modeling identifies threats, risk assessment evaluates impact',
                'option_b': 'No difference',
                'option_c': 'Risk assessment is faster',
                'option_d': 'Threat modeling is more expensive',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Threat modeling identifies potential threats, while risk assessment evaluates the impact and likelihood of those threats.'
            },
            {
                'question_text': 'What is the primary purpose of a Security Operations Center (SOC)?',
                'option_a': 'To monitor and respond to security incidents',
                'option_b': 'To develop security policies',
                'option_c': 'To conduct security audits',
                'option_d': 'To train security staff',
                'correct_answer': 'a',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'SOC\'s primary purpose is to monitor, detect, and respond to security incidents in real-time.'
            },
            {
                'question_text': 'What is the main challenge with supply chain attacks?',
                'option_a': 'They target trusted third-party components',
                'option_b': 'They are hard to detect',
                'option_c': 'They can affect multiple organizations',
                'option_d': 'All of the above',
                'correct_answer': 'd',
                'difficulty': 'hard',
                'points': 20,
                'explanation': 'Supply chain attacks target trusted components, are hard to detect, and can affect multiple organizations.'
            }
        ]

        # Create questions for each quiz
        all_questions = {
            'network': network_questions,
            'web': web_questions,
            'crypto': crypto_questions,
            'general': general_questions
        }

        for category, questions in all_questions.items():
            quiz = Quiz.objects.get(category=category)
            
            for question_data in questions:
                question, created = QuizQuestion.objects.get_or_create(
                    quiz=quiz,
                    question_text=question_data['question_text'],
                    defaults=question_data
                )
                if created:
                    self.stdout.write(f'Created question: {question.question_text[:50]}...')
                else:
                    self.stdout.write(f'Question already exists: {question.question_text[:50]}...')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated quiz questions!')
        )
