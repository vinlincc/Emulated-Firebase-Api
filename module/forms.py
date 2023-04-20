import wtforms
from wtforms.validators import EqualTo, Email
from models import User, Email




class Register(wtforms.Form):
    email = wtforms.StringField(validators=[Email()])
    code = wtforms.StringField()
    user = wtforms.StringField()
    password = wtforms.StringField()
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="Confirm twice password is the same!")])


    def email_validation(self, field):
        email = field.data
        user = User.objects(email=email).first()
        if user:
            raise wtforms.ValidationError(message="This email has been signed up!")


    def code_validation(self, field):
        code = field.data
        email = self.email.data
        email_in_db = Email.objects(email=email,code=code).first()
        if not email_in_db:
            raise wtforms.ValidationError(message="Validation code is wrong!")
        else:
            email_in_db.delete()

class Login(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Email format is wrong!")])
    password = wtforms.StringField()


