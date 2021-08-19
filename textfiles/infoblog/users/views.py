from flask import render_template,redirect,url_for,Blueprint,request,flash
from flask_login import login_user,logout_user,current_user,login_required
from puppycompanyblog import db
from puppycompanyblog.models import User,Blogpost
from puppycompanyblog.users.forms import LoginForm,RegisterForm,UpdateForm
from puppycompanyblog.users.picture_handler import add_profile_pic


users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user=User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for register')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)


@users.route('/login',methods=['GET','POST'])
def login(): 
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log In Success')

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html',form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))



@users.route('/account',methods=['GET','POST'])
@login_required 
def account():
    form = UpdateForm()
    if form.validate_on_submit():

        if form.picture.data:
            username =current_user.username
            pic=add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('user account is updated')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.email.data=current_user.email
        form.username.data=current_user.username
    profileimage = url_for('static',filename='profile_pics/'+current_user.profileimage)
    return render_template('account.html',profileimage=profileimage,form=form) 


@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    blog_posts=Blogpost.query.filter_by(author=user).order_by(Blogpost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_post.html',blog_posts=blog_posts,user=user)

