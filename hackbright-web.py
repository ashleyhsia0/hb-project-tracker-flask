from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add", methods=['GET'])
def student_add():
    """Add a student."""

    return render_template("student_add.html")


@app.route("/student-add-confirmation", methods=['POST'])
def student_add_confirmation():
    """Confirm student has been added."""

    first = request.form.get('firstname')
    last = request.form.get('lastname')
    github = request.form.get('github')
    hackbright.make_new_student(first, last, github)

    return render_template("student_add_confirmation.html",
                            github=github)

# # Keeps /student-add route, but two methods based on form submission
# @app.route("/student-add", methods=['POST'])
# def display_student_add():
#     """Display student info."""

#     first = request.form.get('firstname')
#     last = request.form.get('lastname')
#     github = request.form.get('github')
#     hackbright.make_new_student(first, last, github)

#     return render_template("student_info.html",
#                            first=first,
#                            last=last,
#                            github=github)

@app.route("/project")
def get_project_info():
    """Show info about project."""

    title = request.args.get('title', 'Markov')
    title, description, max_grade = hackbright.get_project_by_title(title)
    students_and_grade = hackbright.get_grades_by_title(title)

    for github, grade in students_and_grade:
        first_name, last_name, github = hackbright.get_student_by_github(github)
    # endsloop on last person does catch each student - NEED TO FIX

    return render_template("project_info.html",
                            title = title,
                            description = description,
                            max_grade = max_grade,
                            students_and_grade = students_and_grade,
                            first_name = first_name,
                            last_name = last_name)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
