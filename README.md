# Hardhat Enterprises - Cybersecurity Platform

Hardhat Enterprises is an organisation that aims to create cyber weapons and tools that can be used to empower white-hat operations. All deliverables produced by the company are open source so that anyone may use and benefit from them. These deliverables should either improve on existing tools or fill a market need that is not yet met.

The Hardhat Enterprises Website is a comprehensive Django-based cybersecurity platform that provides educational tools, security assessments, and hands-on learning experiences for cybersecurity professionals and students. The platform combines theoretical knowledge with practical application through interactive challenges, security tools, and real-world simulations.

##  Key Features

### Educational Platform
- **Interactive Cyber Challenges**: Multiple choice questions and code-fixing challenges across various cybersecurity domains
- **Skills Tracking**: Progress monitoring for cybersecurity skills development
- **Upskilling Modules**: Comprehensive learning paths for different cybersecurity specialisations
- **Leaderboard System**: Gamified learning with points and rankings

### Security Tools Arsenal
- **Penetration Testing Tools**: Integration with Metasploit, Burp Suite, and custom testing frameworks
- **Vulnerability Assessment**: Nessus scanner integration and custom vulnerability detection
- **Network Analysis**: Nmap, Wireshark, and network monitoring tools
- **SIEM Integration**: Splunk and custom security analytics
- **Identity Management**: CyberArk PAM and privileged access controls

### Hardhat Enterprises Cybersecurity Projects
- **AppAttack**: Application security testing and vulnerability assessment
- **Malware Visualisation**: Malware analysis and threat intelligence tools
- **PT-GUI (Deakin Detonator Toolkit)**: Comprehensive penetration testing GUI with 15+ integrated tools
- **Smishing Detection**: SMS phishing detection and prevention
- **VR Cybersecurity**: Virtual reality cybersecurity training modules
- **Threat Mirror**: Real-time threat intelligence and monitoring

### Career Development
- **Job Portal**: Cybersecurity job listings and application management
- **Career Path Finder**: Guided career planning for cybersecurity roles
- **Graduate Programmes**: Structured learning programmes for career advancement
- **Internship Opportunities**: Hands-on experience programmes

### Security Features
- **Multi-Factor Authentication**: Email OTP and Microsoft Azure AD integration
- **Session Management**: Secure session handling with timeout controls
- **Rate Limiting**: Protection against brute force attacks
- **Audit Logging**: Comprehensive security event logging
- **Device Fingerprinting**: Advanced user device tracking
- **Password Security**: Complex password requirements with history tracking

## Technical Architecture

### Backend Framework
- **Django 4.2.14**: Modern Python web framework
- **PostgreSQL**: Primary database with SQLite fallback
- **Django REST Framework**: API development
- **Celery & Redis**: Asynchronous task processing

### Frontend Technologies
- **Bootstrap 5**: Responsive UI framework
- **JavaScript**: Interactive components and AJAX functionality
- **TinyMCE**: Rich text editing
- **Chart.js**: Data visualisation and analytics

### Security & Authentication
- **Microsoft OAuth 2.0**: Enterprise authentication
- **bcrypt**: Secure password hashing
- **CSRF Protection**: Cross-site request forgery prevention
- **XSS Protection**: Input sanitisation with nh3
- **HTTPS Enforcement**: SSL/TLS security headers

### DevOps & Deployment
- **Docker**: Containerised deployment
- **Nginx**: Reverse proxy and static file serving
- **Gunicorn**: WSGI application server
- **PostgreSQL**: Production database

## Database Models

### User Management
- **Custom User Model**: Extended Django user with cybersecurity-specific fields
- **Student Profiles**: Academic tracking and project preferences
- **Admin Sessions**: Secure administrative access management
- **Device Tracking**: User device fingerprinting and management

### Educational Content
- **Cyber Challenges**: Interactive learning challenges with multiple formats
- **Skills & Progress**: Competency tracking and assessment
- **Resources**: Educational materials and documentation
- **Blog System**: Content management for cybersecurity articles

### Security & Monitoring
- **Security Events**: Comprehensive audit trail
- **Admin Notifications**: System alerts and feedback management
- **Vault Documents**: Secure file storage and sharing
- **Password History**: Password reuse prevention

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (for local development)
- PostgreSQL (for production)

### Docker Deployment (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hardhat-Enterprises/website.git
   cd website
   ```

2. **Configure environment variables**:
   ```bash
   cp env.sample .env
   # Edit .env with your configuration
   ```

3. **Start the application**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Website: http://localhost:8000
   - Nginx (production): http://localhost:8080

### Local Development

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations #Delete Intial migration file and run this command to generate any changes from models.py file
   python manage.py migrate
   python manage.py populate_database
   ```

4. **Start development server**:
   ```bash
   python manage.py runserver
   ```
5. **Create Superuser
   ```bash
   python manage.py createsuperuser
   ```
   *Note any user email verfication may go to your spam folder so always check.

## Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key (auto-generated)
- `DEBUG`: Development mode toggle
- `DB_ENGINE`: Database engine (postgresql/sqlite3)
- `MICROSOFT_CLIENT_ID`: Azure AD application ID
- `MICROSOFT_CLIENT_SECRET`: Azure AD application secret
- `EMAIL_HOST_USER`: SMTP email configuration

### Security Settings
- Rate limiting: 5 attempts per minute for login
- Session timeout: 30 minutes with activity reset
- Password complexity: Uppercase, lowercase, digit, and symbol required
- HSTS: 1 year with subdomain inclusion

## Project Structure

```
website/
├── core/                    # Django project configuration
│   ├── settings.py         # Main settings and security configuration
│   ├── urls.py            # URL routing
│   └── middleware.py      # Custom middleware components
├── home/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # Business logic and controllers
│   ├── urls.py            # Application URL patterns
│   ├── templates/         # HTML templates
│   └── management/        # Custom Django commands
├── custom_static/          # Static assets (CSS, JS, images)
├── nginx/                  # Nginx configuration
├── Scripts/               # Deployment and utility scripts
├── utils/                 # Utility functions and helpers
└── docker-compose.yml     # Docker orchestration
```

## Security Features

- **Authentication**: Multi-factor with OTP and Microsoft OAuth
- **Authorisation**: Role-based access control with staff/admin levels
- **Data Protection**: Input sanitisation, CSRF tokens, and XSS prevention
- **Session Security**: Secure cookies, timeout controls, and device tracking
- **Audit Trail**: Comprehensive logging of security events
- **Rate Limiting**: Brute force protection with intelligent lockout

## Internationalization

Supports multiple languages:
- English (default)
- Simplified Chinese
- French
- Spanish
- Japanese
- Korean

## Analytics & Monitoring

- **User Activity Tracking**: Comprehensive user behaviour analytics
- **Security Event Monitoring**: Real-time threat detection
- **Performance Metrics**: Application performance monitoring
- **Audit Logging**: Detailed security and administrative logs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Support

For support and questions:
- Email: hardhatwebsite@gmail.com
- Security Issues: security@hardhatenterprises.com

## Links

- [Documentation](./deployment_README.md)
- [Security Policy](/.well-known/security.txt)

---

**Hardhat Enterprises** - Empowering the next generation of cybersecurity professionals through hands-on learning and cutting-edge tools.
