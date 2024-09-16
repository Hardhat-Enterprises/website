from twilio.rest import Client
from django.conf import settings

def send_verification_sms(to_phone_number, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Your verification code is {verification_code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_phone_number
    )
    
    return message.sid
