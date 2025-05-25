from flask import render_template, request, redirect, url_for
from app import app
from app.models import Todo
from app import db


@app.route('/')
def home():
    query = request.args.get('query')
    if query:
        allTodo = Todo.query.filter(
            (Todo.title.ilike(f"%{query}%")) | (Todo.desc.ilike(f"%{query}%"))
        ).all()
    else:
        allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title,desc = desc)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    allTodo = Todo.query.all()
    return render_template('add.html',allTodo=allTodo)

@app.route('/delete/<int:SNo>')
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/') 

@app.route('/update/<int:SNo>',methods=['GET','POST'])
def update(SNo):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(SNo=SNo).first()
        todo.tittle = title
        todo.desc = desc  
        db.session.add(todo)
        db.session.commit()
        return redirect('/')


    todo = Todo.query.filter_by(SNo=SNo).first()
    return render_template('update.html',todo=todo)

@app.route('/about')
def about():
    return render_template('about.html')