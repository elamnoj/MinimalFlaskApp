from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import Post, User, Submit
from flask_login import login_user, logout_user
import plotly
from plotly import express as px
import plotly.io as pio



import pandas as pd
import numpy as np
import json




@app.route('/')
def home():
    air = pd.read_csv(r'listings.csv')

    # pio.renderers.default = 'browser'
    fig = px.scatter_mapbox(air, lat="latitude", lon="longitude", hover_name="neighbourhood_cleansed", hover_data=[
                            "room_type", "price"], color="neighbourhood_cleansed", zoom=11, height=400)

    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    graphJSON = json.dumps(fig.show(), cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON=graphJSON)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        s = Submit()
        s.from_dict(request.form)
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
