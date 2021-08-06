from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,DecimalField,validators
from wtforms.validators import Length,EqualTo,Email,DataRequired, ValidationError,NumberRange
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('UserName Already Exists! Try a different username')
    def validate_email(self,email_to_check):
        email=User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Try a different email address')
    username=StringField(label='User Name:',validators=[Length(min=2,max=30), DataRequired()])
    email=StringField(label='Email Address:',validators=[Email(),DataRequired()])
    password1=PasswordField(label='Password:',validators=[Length(min=4),DataRequired()])
    password2=PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
    budget=IntegerField(label='Budget',validators=[DataRequired()])
    submit=SubmitField(label='Register')

class LoginForm(FlaskForm):
    username=StringField(label='User Name:',validators=[DataRequired()])
    password=PasswordField(label='Password:',validators=[DataRequired()])
    submit=SubmitField(label='Log In')

class PurchaseItemForm(FlaskForm):
   submit=SubmitField(label='Purchase') 

class SellItemForm(FlaskForm):
   submit=SubmitField(label='Sell') 