from django.test import TestCase

# Create your tests here.

#Testing Validation
#import re
#from django.core.exceptions import ValidationError

#def xss_detection(input_data):
    #pattern = r"<\s*script\b[^>]*>.*?<\s*/\s*script\s*>"
    #if re.search(pattern, input_data, re.IGNORECASE):
        #print(f"XSS Attack Detected: {input_data}")
        #raise ValidationError(f"XSS Attack Detected: {input_data}")
    #return input_data

# Test for Contact in terms of Validation
#xss_detection("<script>alert('XSS')</script>")
#xss_detection("hello")

#Testing LeaderBoard
from .models import LeaderBoardTable, User

class LeaderboardTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(first_name="Hardhat", last_name="Enterprise",email="hardhat@deakin.edu.au")
        LeaderBoardTable.objects.create(user=user, category="Crypto", total_points=150)

    def test_leaderboard_entries(self):
        entries = LeaderBoardTable.objects.all()
        self.assertEqual(entries.count(), 1)
        self.assertEqual(entries.first().user.first_name, "Hardhat")
        print(entries)

