from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired


class Blogpostform(FlaskForm):
    title = StringField('Tittle',validators=[DataRequired()])
    text = TextAreaField('Text',validators=[DataRequired()])
    post = SubmitField('Post')




