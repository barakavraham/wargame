from app.models.army import Army
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class SetArmyNameForm(FlaskForm):
    army_name = StringField('Army name', validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Submit')

    @staticmethod
    def validate_army_name(_, army_name):
        army = Army.query.filter_by(name=army_name).first()
        if not army_name.data.isalnum():
            raise ValidationError('Army name must contain only letters and numbers')
        if army:
            raise ValidationError('This army name already exists')

