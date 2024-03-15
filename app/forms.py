from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired

class AddNewProperty(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    noOfRooms = IntegerField('No. of Rooms', validators=[InputRequired()])
    noOfBathrooms = IntegerField('No. of Bathrooms', validators=[InputRequired()])
    price = DecimalField('Price', validators=[InputRequired()])
    propertyType = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])