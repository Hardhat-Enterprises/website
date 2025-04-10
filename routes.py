from flask import Blueprint, render_template, request
from sentiment_analysis import analyze_sentiment  # Import sentiment analysis function
from email_functions import send_follow_up_email  # Import email sending function

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('contact_us.html')

@main_routes.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    message = request.form['message']

    sentiment = analyze_sentiment(message)
    send_follow_up_email(first_name, last_name, email, message, sentiment)

    return render_template('thank_you.html', first_name=first_name, last_name=last_name, message=message)

