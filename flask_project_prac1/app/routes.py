from flask import Blueprint, render_template, request, redirect, flash
import re
import datetime


main = Blueprint('main', __name__)

@main.route('/')
def home():
    current_time = datetime.datetime.now()
    return render_template('index.html', current_time=current_time)

@main.route('/about')
def about():
    team_members = [

        {'name': 'Alice', 'role': 'Developer'},

        {'name': 'Bob', 'role': 'Designer'},

        {'name': 'Charlie', 'role': 'Project Manager'}

    ]

    return render_template('about.html', team=team_members)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_info = {
        "manager": {
            "name": "John Smith",
            "position": "Account Manager",
            "email": "support@example.com",
            "phone": "+1 234 567-8900"
        },
        "address": {
            "street": "123 Main St.",
            "city": "New York",
            "zip": "10001"
        }
    }
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('All fields are required!', 'error')
            return redirect('/contact')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
            return redirect('/contact')

        flash('Your message has been sent successfully!', 'success')
        return redirect('/contact')

    return render_template('contact.html', contact=contact_info)
