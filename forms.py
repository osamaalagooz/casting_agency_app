from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField
from wtforms.validators import DataRequired, Length, URL

class ActorForm(FlaskForm):
    name = StringField('name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    age = StringField('age',
                        validators=[DataRequired()])
    
    gender = RadioField('gender', choices=[('male','Male'), ('female','Female')], validators=[DataRequired()])

    image_url = StringField('image_url', validators=[DataRequired(), URL()] ) 

    movie = StringField('movie',
                        validators=[DataRequired()])                     
    

class MovieForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(min=2, max=20)])

    release_date = DateField('release_date', validators = [DataRequired()])

    image_url = StringField('image_url', validators=[DataRequired(), URL()] )


class ActorForm2(FlaskForm):
    name = StringField('name',
                           validators=[ Length(min=2, max=20)])
    age = StringField('age')
                        
    
    gender = RadioField('gender', choices=[('male','Male'), ('female','Female')])

    image_url = StringField('image_url', validators=[URL()] ) 

    movie = StringField('movie')                     
    
class MovieForm2(FlaskForm):
    title = StringField('title', validators = [ Length(min=2, max=20)])

    release_date = DateField('release_date')

    image_url = StringField('image_url', validators=[URL()])