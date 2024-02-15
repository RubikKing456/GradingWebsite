from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Function to load student data from JSON file
def load_students():
    try:
        with open('students.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save student data to JSON file
def save_students(students):
    with open('students.json', 'w') as file:
        json.dump(students, file, indent=4)

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route to display the list of students
@app.route('/students')
def student_list():
    students = load_students()
    return render_template('students.html', students=students)

# Route to add a new student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        students = load_students()
        name = request.form['name']
        grade = request.form['grade']
        students[name] = grade
        save_students(students)
        return redirect(url_for('student_list'))
    return render_template('add_student.html')

# Route to update a student's grade
@app.route('/update_grade/<name>', methods=['GET', 'POST'])
def update_grade(name):
    students = load_students()
    if request.method == 'POST':
        new_grade = request.form['grade']
        students[name] = new_grade
        save_students(students)
        return redirect(url_for('student_list'))
    return render_template('update_grade.html', name=name, grade=students.get(name))

if __name__ == '__main__':
    app.run(debug=True)