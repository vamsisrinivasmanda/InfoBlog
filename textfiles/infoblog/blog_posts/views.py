from flask import render_template,url_for,redirect,flash,request,Blueprint
from flask_login import current_user,login_required
from puppycompanyblog import db
from puppycompanyblog.models import Blogpost
from puppycompanyblog.blog_posts.forms import Blogpostform

blog_posts = Blueprint('blog_posts', __name__)

@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form=Blogpostform()

    if form.validate_on_submit():
        blog_post = Blogpost(title=form.title.data,text=form.text.data,user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html',form=form)





@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',title=blog_post.title,date=blog_post.date,post=blog_post)



@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update_blog_post(blog_post_id):
    
    blog_post = Blogpost.query.get_or_404(blog_post_id)

    if  blog_post.author != current_user:
        abort(403)

    form=Blogpostform()
    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post_id))

    elif request.method == 'GET':
        form.title.data = blog_post.title  
        form.text.data = blog_post.text

    return render_template('create_post.html',form=form,title="updating")




@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)


    db.session.delete(blog_post)
    db.session.commit()
    return redirect(url_for('core.index'))

