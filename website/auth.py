from flask import Blueprint,render_template,redirect,url_for,request,flash,Response
import re

from .models import User,db
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint('auth',__name__)


@auth.route('/login' ,methods=['POST','GET'])
def login():
    if request.method =='GET':
        return render_template('login.html',user=current_user)
    try:
        data = request.form
        email = data.get('email')
        password = data.get('password')
        user=User.query.filter_by(email=email).first()
        if not user:
            return "email doesn't exists", 400, {'Content-Type': 'text/plain'}
        if check_password_hash(user.password,password):
            flash('Logged in!',category='success')
            login_user(user,remember=True)

            return redirect(url_for('views.home'))
        else:
      
            return 'Password Incorrect', 400, {'Content-Type': 'text/plain'}
    except:
       
        return 'Something Went Wrong', 400, {'Content-Type': 'text/plain'}

@auth.route('/sign-up',methods=['POST','GET'])
def sign_up():
    if request.method =='GET':
        return render_template('signup.html',user=current_user)
    
    try:
        data = request.form
        email = data.get('email')
        username = data.get('Username')
        password = data.get('password')
        password2 = data.get('password2')


        email_exists=User.query.filter_by(email=email).first()
        
        if email_exists:
           
            
            return 'Email is already in use.', 400, {'Content-Type': 'text/plain'}
        
        username_exists=User.query.filter_by(username=username).first()
        if username_exists:
           
           
            return 'Username is already in use.', 400, {'Content-Type': 'text/plain'}

        if password!=password2 :
            
            return "Password don't match with confirm password", 400, {'Content-Type': 'text/plain'}
            
        if len(username) <4 :
  
            return 'Username is too short', 400, {'Content-Type': 'text/plain'}
        if len(password)<6:
           
            return 'Password should be atleast 6 characters long', 400, {'Content-Type': 'text/plain'}
        

        if re.match(r'^[\w\.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)==None:
        
           return 'Email is invalid', 400, {'Content-Type': 'text/plain'}
        
        new_user=User(email=email,username=username,password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user,remember=True)
        flash('User created',category='success')
        return redirect(url_for('views.home'))
    except Exception as e:
        print(e)

        return 'Something Went Wrong.', 400, {'Content-Type': 'text/plain'}


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))