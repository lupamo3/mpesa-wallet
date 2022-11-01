# standard python imports

from app.db import db

class EWallet(db.Model):
    __tablename__ = 'ewallets'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(80))
    balance = db.Column(db.Float(precision=2))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
