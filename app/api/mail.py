from app import db
from app.api import base_api, SubpathApi
from app.models.army import Army
from app.models.user import Mail
from app.permissions.permissions import login_required_for_api
from flask import url_for
from flask_restful import Resource, reqparse
from flask_login import current_user

subpath_api = SubpathApi(base_api, '/mail', 'mail')

class GetArmiesAPI(Resource):
    decorators = [login_required_for_api]

    @staticmethod
    def get(army_letters):
        armies_dict_list = []
        armies_list = Army.query.filter(Army.name.like(f'%{army_letters}%')).all()
        for army in armies_list:
            armies_dict_list.append({'name': army.name,
                                     'picture_url': army.user.avatar if army.user.is_google_user else url_for('static', filename="images/default.png")})
        return armies_dict_list

subpath_api.add_resource(GetArmiesAPI, '/get_armies/<string:army_letters>', endpoint='get_armies')

class SendMailAPI(Resource):
    decorators = [login_required_for_api]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('recipient_army', type=str, required=True)
        self.reqparse.add_argument('title', type=str, required=True)
        self.reqparse.add_argument('content', type=str)
        super(SendMailAPI, self).__init__()

    def is_user_exist(self, army_name):
        recipient_user_id = Army.query.filter_by(name=army_name).all()
        if recipient_user_id:
            return recipient_user_id[0].user.id

    def validate_letters_amount(self, mail_title, mail_content):
        if len(list(mail_title)) <2 or len(list(mail_content)) <2:
            return False
        return True

    def post(self):
        args = self.reqparse.parse_args()
        army_name = args['recipient_army']
        mail_title = args['title']
        mail_content = args['content']
        recipient_user_id = self.is_user_exist(army_name)
        validate_letters = self.validate_letters_amount(mail_title, mail_content)

        if recipient_user_id is None:
            send_result = 'Army not found'
            return {'succsess': False, 'send_result': send_result}, 404

        elif current_user.id == recipient_user_id:
            send_result = 'You cant send mail to yourself'
            return {'succsess': False, 'send_result': send_result}, 404

        elif validate_letters is False:
            send_result = 'Title/Content must be more than 1 letter'

        else:
            send_result = 'Mail sent'

        new_mail = Mail(author_id=current_user.id,
                               recipient_id=recipient_user_id,
                               title=mail_title,
                               content=mail_content)
        db.session.add(new_mail)
        db.session.commit()

        return {'succsess': validate_letters, 'send_result': send_result}, 200 if validate_letters else 400

subpath_api.add_resource(SendMailAPI, '/send_mail', endpoint='send_mail')
