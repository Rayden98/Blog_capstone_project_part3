from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime

## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PostForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Your Name', validators=[DataRequired()])
    img_url = StringField('Blog Image URL', validators=[DataRequired(), URL()])
    body = CKEditorField('Blog content', validators=[DataRequired()])  # <--
    submit = SubmitField('Submit Post')


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    # for blog_post in posts:
    #    if blog_post.id == post_id:
    #        requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.session.query(BlogPost).get(post_id)

    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )

    if request.method == "POST":
        form = PostForm()
        print("hello")
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%B %d, %Y")
        db.session.query(BlogPost).filter(BlogPost.id == post_id).update({'title': form.title.data})
        db.session.query(BlogPost).filter(BlogPost.id == post_id).update({'subtitle': form.subtitle.data})
        db.session.query(BlogPost).filter(BlogPost.id == post_id).update({'body': form.body.data})
        db.session.query(BlogPost).filter(BlogPost.id == post_id).update({'author': form.author.data})
        db.session.query(BlogPost).filter(BlogPost.id == post_id).update({'img_url': form.img_url.data})
        #post_to_update.id = post_id
            #post_to_update.title = form.title.data,
            #post_to_update.subtitle = form.subtitle.data,
            #post_to_update.date = formatted_datetime,
            #post_to_update.body = form.body.data,
            #post_to_update.author = form.author.data,
            #post_to_update.img_url = form.img_url.data,

        print("hello 4")

        db.session.commit()
        print("hello 5")
        requested_post = BlogPost.query.get(post_id)
        return render_template("post.html", post=requested_post)

    return render_template("make-post.html", form=edit_form, edit_blog=True)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%B %d, %Y")
        with app.app_context():
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                date=formatted_datetime,
                body=form.body.data,
                author=form.author.data,
                img_url=form.img_url.data,
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    print("hello")
    db.session.query(BlogPost).filter(BlogPost.id == post_id).delete()
    db.session.commit()
    print("hello2")
    #post_to_delete = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    #db.session.delete(post_to_delete)
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
