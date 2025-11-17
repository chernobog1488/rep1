from app import app

@app.route("/hello")
def hello():
    return "Hello, world!"

@app.route("/info")
def info():
    return "This is an informational page."

@app.route('/calc/<a>/<b>')
def calc(a, b):
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        return 'Error: both parameters must be int', 400

    return f'The sum of {a} and {b} is {a+b}.'

@app.route('/reverse/<text>')
def reverse(text):
    if not text.strip():
        return 'Error: text must contain at least one non-space character.', 400

    return text[::-1]

@app.route('/user/<name>/<age>')
def user(name, age):
    try:
        age = int(age)
    except ValueError:
        return 'Error: parameter age must be int', 400
    if age < 0:
        return 'Error: age cannot be negative.', 400

    return f'Hello, {name}. You are {age} years old.'
