from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate

from database import db
from forms import PersonForm
from models import Person

app = Flask(__name__)

# BD CONFIG
USER_DB = 'postgres'
PASS_DB = 'postgres'
HOST = '127.0.0.1'
DATABASE = 'sap_flask_db'
PORT = '5434'
URL = f'postgresql://{USER_DB}:{PASS_DB}@{HOST}:{PORT}/{DATABASE}'

app.config['SQLALCHEMY_DATABASE_URI'] = URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init database object
db.init_app(app)

# flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

# flask-wtf
app.config['SECRET_KEY'] = 'Alhe123$'


@app.route('/')
@app.route('/index')
def index():
    persons = Person.query.order_by('id')
    persons_count = Person.query.count()
    app.logger.debug(f'Personas: {persons}')
    app.logger.debug(f'Personas_Count: {persons_count}')
    return render_template('index.html', persons=persons, count_person=persons_count)


@app.route('/show/<int:id>')
def show_person(id):
    person = Person.query.get_or_404(id)
    app.logger.debug(f'Person: {person}')
    return render_template('show.html', person=person)


@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    person = Person()
    personForm = PersonForm(obj=person)
    if request.method == 'POST':
        if personForm.validate_on_submit():
            personForm.populate_obj(person)
            app.logger.debug(f'Person to save {person}')

            # save
            db.session.add(person)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('add.html', form=personForm)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    person = Person.query.get_or_404(id)
    personForm = PersonForm(obj=person)
    if request.method == 'POST':
        if personForm.validate_on_submit():
            personForm.populate_obj(person)
            app.logger.debug(f'Person to update {person}')

            # commit changes
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', form=personForm)


@app.route('/delete/<int:id>')
def delete_person(id):
    person = Person.query.get_or_404(id)
    app.logger.debug(f'Person to delete {person}')
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))
