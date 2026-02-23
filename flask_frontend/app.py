from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "super-secret-key-change-me"  # needed for flash messages

API_BASE_URL = "http://127.0.0.1:8000"  # ← your FastAPI server

@app.route("/")
def index():
    try:
        response = requests.get(f"{API_BASE_URL}/students/")
        response.raise_for_status()
        students = response.json()
    except requests.RequestException as e:
        flash(f"Error fetching students: {str(e)}", "danger")
        students = []

    return render_template("index.html", students=students)


@app.route("/create", methods=["GET", "POST"])
def create():
    form_data = {}  # what we'll pass to template

    if request.method == "POST":
        form_data = {
            "first_name": request.form.get("first_name", ""),
            "last_name": request.form.get("last_name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "date_of_birth": request.form.get("date_of_birth", ""),
            "status": request.form.get("status", "active"),
        }

        try:
            response = requests.post(f"{API_BASE_URL}/students/", json=form_data)
            response.raise_for_status()
            flash("Student created successfully!", "success")
            return redirect(url_for("index"))
        except requests.RequestException as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except:
                error_detail = str(e)
            flash(f"Error: {error_detail}", "danger")
            # keep user input on error
            return render_template("create.html", student=form_data)

    # GET → show empty form
    return render_template("create.html", student=form_data)


@app.route("/student/<int:student_id>")
def detail(student_id):
    try:
        response = requests.get(f"{API_BASE_URL}/students/{student_id}")
        response.raise_for_status()
        student = response.json()
    except requests.RequestException:
        flash("Student not found", "danger")
        return redirect(url_for("index"))

    return render_template("detail.html", student=student)


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit(student_id):
    if request.method == "POST":
        data = {}
        for field in ["first_name", "last_name", "email", "phone", "date_of_birth", "status"]:
            if field in request.form and request.form[field]:
                data[field] = request.form[field]

        try:
            response = requests.put(f"{API_BASE_URL}/students/{student_id}", json=data)
            response.raise_for_status()
            flash("Student updated successfully!", "success")
            return redirect(url_for("detail", student_id=student_id))
        except requests.RequestException as e:
            flash(f"Error updating student: {response.text or str(e)}", "danger")

    # GET: load current data
    try:
        response = requests.get(f"{API_BASE_URL}/students/{student_id}")
        response.raise_for_status()
        student = response.json()
    except requests.RequestException:
        flash("Student not found", "danger")
        return redirect(url_for("index"))

    return render_template("edit.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete(student_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/students/{student_id}")
        response.raise_for_status()
        flash("Student deleted successfully!", "success")
    except requests.RequestException as e:
        flash(f"Error deleting student: {str(e)}", "danger")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)