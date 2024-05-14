from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from .models import Post
from .models import User
from .models import Comment
from .models import Like
from .models import db
views = Blueprint('views',__name__)

@views.route('/')
@views.route('/home',methods=["GET"])
@login_required
def home():
    posts =Post.query.order_by(Post.date_created.desc()).all()

    return render_template('home.html',user=current_user,posts=posts)

@views.route('/create-post',methods=['GET','POST'])
@login_required
def create_post():
    if request.method =='POST':
        topic = request.form.get('topic')
        message = request.form.get('message')
        if not topic and not message :
            
            return 'All fields are required', 400, {'Content-Type': 'text/plain'}
        elif(len(topic)>190):
            print(topic)
            return 'Topic should not be more than 190 characters!', 400, {'Content-Type': 'text/plain'}
        elif(len(message)>400):
            return 'Message should not be more than 400 characters!', 400, {'Content-Type': 'text/plain'}
        else:
            post= Post(topic=topic,message=message,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            # return 'Post Created!', 200, {'Content-Type': 'text/plain'}
            return redirect(url_for('views.home'))
    return render_template('create_post.html',user=current_user)

@views.route('/delete-post/<id>',methods=['DELETE'])
@login_required
def delete_post(id):

    if request.method=='DELETE':
        
        try:
            post =Post.query.filter_by(id=id).first()
            
            if not (int(post.author) == int(current_user.id)):            
                return "You don't have permission.", 400, {'Content-Type': 'text/plain'}

            if not post:
                return "No Post Found for deletion", 400, {'Content-Type': 'text/plain'}
            db.session.delete(post)
            db.session.commit()
            return "Post Deleted SuccessFully", 200, {'Content-Type': 'text/plain'}
            
        except:
            
            return 'Something Went Wrong', 400, {'Content-Type': 'text/plain'}
        
@views.route('/delete-comment/<id>',methods=['DELETE'])
@login_required
def delete_comment(id):

    if request.method=='DELETE':
        
        try:
            comment =Comment.query.filter_by(id=id).first()
            
            if not (int(comment.author) == int(current_user.id)):            
                return "You don't have permission.", 400, {'Content-Type': 'text/plain'}

            if not comment:
                return "No Comment Found for deletion", 400, {'Content-Type': 'text/plain'}
            db.session.delete(comment)
            db.session.commit()
            return "Comment Deleted SuccessFully", 200, {'Content-Type': 'text/plain'}
            
        except:
            
            return 'Something Went Wrong', 400, {'Content-Type': 'text/plain'}
        
    
@views.route('/posts/<username>')
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists.')
        return redirect(url_for('views.home'))
    posts = user.posts
    return render_template('posts.html',user=current_user,posts=posts,username=username)

@views.route('/create-comment/<post_id>',methods=['POST'])
@login_required
def comment(post_id):
    text = request.form.get('text')
    if not text:
        return 'comment cannot be blank', 400, {'Content-Type': 'text/plain'}
    
    post= Post.query.filter_by(id=post_id).first()
    if not post:
        return 'No post found', 400, {'Content-Type': 'text/plain'}
    comment = Comment(text=text,author=current_user.id,post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return 'comment added', 200, {'Content-Type': 'text/plain'}
    
@views.route('/like-post/<post_id>',methods=['POST'])
@login_required
def like(post_id):
    
    try:
        post= Post.query.filter_by(id=post_id).first()
        if not post:
            return 'No post found', 400, {'Content-Type': 'text/plain'}
        like= Like.query.filter_by(post_id=post_id,author=current_user.id).first()
        
        if like:
            print('nice')
            db.session.delete(like)
            db.session.commit()
            return "disliked", 200, {'Content-Type': 'text/plain'}
        likes = Like(author=current_user.id,post_id=post_id)
        db.session.add(likes)
        db.session.commit()
        return 'liked', 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        print("manage it")
        

    
