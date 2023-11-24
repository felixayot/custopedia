from flask import current_app
from app import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), index=True, nullable=False)
    last_name = db.Column(db.String(45), index=True, nullable=False)
    email = db.Column(db.String(45), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.Unicode(255), index=True, unique=True,
                             nullable=False)
    username = db.Column(db.String(45), index=True, unique=True,
                         nullable=False)
    password = db.Column(db.String(128))
    tickets = db.relationship("Ticket", backref="owner", lazy="dynamic")

    def __repr__(self):
        return ("***Customer name: {} {}***\n***E-mail: {}***"
                .format(self.first_name, self.last_name, self.email))
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
