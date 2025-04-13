from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your mail server
app.config['MAIL_PORT'] = 587  # Replace with your mail port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_password'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'  # Replace with your email

mail = Mail(app)

@app.route('/')
def index():
    return render_template('contact_us.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    message = request.form['message']

    # Analyze sentiment
    sentiment = analyze_sentiment(message)

    # Send follow-up email based on sentiment
    send_follow_up_email(first_name, last_name, email, message, sentiment)

    return render_template('thank_you.html', first_name=first_name, last_name=last_name, message=message)

def analyze_sentiment(message):
    positive_keywords = ['good', 'great', 'excellent', 'happy', 'love', 'fantastic']
    negative_keywords = ['bad', 'terrible', 'hate', 'sad', 'angry', 'disappointed']

    message_lower = message.lower()
    
    if any(word in message_lower for word in positive_keywords):
        return 'positive'
    elif any(word in message_lower for word in negative_keywords):
        return 'negative'
    else:
        return 'neutral'

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

if __name__ == '__main__':
    app.run(debug=True)