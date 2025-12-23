from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'agents.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    access_level = db.Column(db.String(50))


def generate_codename():
    first = ['Shadow', 'Black', 'Silent', 'Ghost', 'Iron']
    second = ['Fox', 'Widow', 'Wolf', 'Eagle', 'Viper']
    return f'{random.choice(first)} {random.choice(second)}'


@app.route('/')
def index():
    level = request.args.get('level')

    if level:
        agents = Agent.query.filter_by(access_level=level).all()
    else:
        agents = Agent.query.all()

    return render_template('index.html', agents=agents)


@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        codename = request.form['codename'] or generate_codename()

        agent = Agent(
            codename=codename,
            phone=request.form['phone'],
            email=request.form['email'],
            access_level=request.form['access_level']
        )

        db.session.add(agent)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/agent/<int:agent_id>')
def agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    return render_template('agent.html', agent=agent)


@app.route('/edit/<int:agent_id>', methods=['GET', 'POST'])
def edit_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)

    if request.method == 'POST':
        agent.codename = request.form['codename']
        agent.phone = request.form['phone']
        agent.email = request.form['email']
        agent.access_level = request.form['access_level']

        db.session.commit()
        return redirect(url_for('agent', agent_id=agent.id))

    return render_template('edit.html', agent=agent)


@app.route('/delete/<int:agent_id>')
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/wipe')
def wipe():
    db.session.query(Agent).delete()
    db.session.commit()
    return redirect(url_for('index'))
