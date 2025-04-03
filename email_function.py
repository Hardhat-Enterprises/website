from flask_mail import Mail, Message

# Initialize Flask-Mail
mail = Mail()

def send_follow_up_email(first_name, last_name, email, message, sentiment):
    if sentiment == 'positive':
        subject = "Thank You for Your Positive Feedback!"
        body = f"Hi {first_name} {last_name},\n\nThank you for your positive message! We're thrilled to hear from you.\n\nYour message: {message}\n\nBest regards,\nYour Company"
    elif sentiment == 'negative':
        subject = "We're Sorry to Hear That"
        body = f"Hi {first_name} {last_name},\n\nWe're sorry to hear that you're not satisfied. Please let us know how we can help resolve your issues.\n\nYour message: {message}\n\nBest regards,\nYour Company"
    else:
        subject = "Thank You for Your Message"
        body = f"Hi {first_name} {last_name},\n\nThank you for your message. We have received it and will get back to you shortly.\n\nYour message: {message}\n\nBest regards,\nYour Company"

    msg = Message(subject, recipients=[email])
    msg.body = body
    mail.send(msg)
