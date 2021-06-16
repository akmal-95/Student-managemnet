import os
import functools
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import StudentForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    

    def __init__(self, name, city, addr, pin, ):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin



@app.route('/')
def show_all():
    return render_template('show_all.html', students = Students.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'errror')
        else:
            student = Students(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
            
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')

@app.route('/update/<id>/', methods=['GET', 'POST'])
def edit_student(id):
    student = Students.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.add(student)
        db.session.commit()
        flash('Record was successfully updated')
        return redirect(url_for('show_all'))
    return render_template('student.html', form=form, student=student)

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete_student(id):
    student = Students.query.get_or_404(id)
    form = StudentForm(obj=student)
    db.session.delete(student)
    db.session.commit()
    flash('Record was successfully deleeted ')
    return redirect(url_for('show_all'))
    return render_template('show_all.html', form=form, student=student)
        

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)