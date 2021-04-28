from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import Post, User
from flask_login import login_user, logout_user

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        p = Post(email='derek@codingtemple.com', body=request.form.get('body_text'))
        db.session.add(p)
        db.session.commit()
        flash('Sucess!')
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        s = Submit(email='derek@codingtemple.com',
                 body=request.form.get('body_text'))
        db.session.add(s)
        db.session.commit()
        flash('Thank you for your submission!')
        return redirect(url_for('home'))
    return render_template('contact.html')

@app.route('/blog')
def blog():
    
    context = {
        'posts': [p.to_dict() for p in Post.query.all()]
    }
    return render_template('blog.html', **context)

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is None or user.check_password(request.form.get('password')) is False:
            print('Something is not right')
            flash('User name and email do not match')
            return redirect(url_for('login'))
        remember_me=True if request.form.get('checked') is not None else False
        login_user(user, remember=remember_me)
        flash('Welcome! You are logged in!')
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = User()
        u.from_dict(request.form)
        u.save()
        flash('Success!')
        return redirect(url_for('login'))

    return render_template('register.html')
