from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from app import app, db, bcrypt, login_manager
from app.models import User, Todo, CompletedTodo


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        
        if password != repeat_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already exists!", "danger")  # "danger" for Bootstrap styling
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        repeat_password = request.form.get('repeat_password')

        if new_password != repeat_password:
            flash("Passwords do not match!", "danger")
            return render_template('forgot_password.html')

        user = User.query.filter_by(username=username).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash("Password updated successfully!", "success")
            return redirect(url_for('login'))
        else:
            flash("Username not found!", "danger")
            return render_template('forgot_password.html')

    return render_template('forgot_password.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    allTodo = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        planned_date = datetime.strptime(request.form['planned_date'], '%Y-%m-%d').date()
        planned_time = datetime.strptime(request.form['planned_time'], '%H:%M').time()
        todo = Todo(title=title, desc=desc, planned_date=planned_date, planned_time=planned_time, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('add.html')

@app.route('/delete/<int:SNo>')
@login_required
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo, user_id=current_user.id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/update/<int:SNo>', methods=['GET', 'POST'])
@login_required
def update(SNo):
    todo = Todo.query.filter_by(SNo=SNo, user_id=current_user.id).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.planned_date = datetime.strptime(request.form['planned_date'], '%Y-%m-%d').date()
        todo.planned_time = datetime.strptime(request.form['planned_time'], '%H:%M').time()
        db.session.commit()
        return redirect('/dashboard')
    return render_template('update.html', todo=todo)

@app.route('/complete/<int:SNo>')
@login_required
def complete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    if todo:
        completed = CompletedTodo(
            SNo=todo.SNo,
            title=todo.title,
            desc=todo.desc,
            planned_date=todo.planned_date,
            planned_time=todo.planned_time,
           completed_at=datetime.now()
        )
        db.session.add(completed)
        db.session.delete(todo)
        db.session.commit()
    return redirect('/completed')

@app.route('/completed')
@login_required
def completed_view():
    allTodo = CompletedTodo.query.all()
    return render_template('complete.html', allTodo=allTodo)

@app.route('/Delete/<int:CompleteId>')
@login_required
def Delete(CompleteId):
    todo = CompletedTodo.query.filter_by(CompleteId=CompleteId).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/completed')
