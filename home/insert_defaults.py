from home.models import Project
from home.models import Course

def insert_default_projects():
    default_titles = [
        'AppAttack',
        'Malware',
        'PT-GUI',
        'Smishing_Detection',
        'Deakin_CyberSafe_VR',
        'Deakin_Threat_Mirror',
        'Company_Website_Development',
    ]

    for title in default_titles:
        Project.objects.get_or_create(title=title)

def insert_default_courses():
    course_data = [
        ("BDS", "Bachelor of Data Science", False),
        ("BCS", "Bachelor of Computer Science", False),
        ("BCYB", "Bachelor of Cyber Security", False),
        ("BIT", "Bachelor of Information Technology", False),
        ("BSE", "Bachelor of Software Engineering", False),
        ("BAI", "Bachelor of AI", False),
        ("MAAI", "Master of Applied AI", True),
        ("MDS", "Master of Data Science", True),
        ("MIT", "Master of Information Technology", True),
        ("MITM", "Master of IT Management", True),
        ("MCS", "Master of Cyber Security", True),
    ]

    for code, title, is_pg in course_data:
        Course.objects.get_or_create(
            code=code,
            defaults={
                'title': title,
                'is_postgraduate': is_pg
            }
        )

