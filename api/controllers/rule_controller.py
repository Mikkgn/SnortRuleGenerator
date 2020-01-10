from flask import current_app

from api.db.models import Rule


def get_rules():
    return [rule.body for rule in current_app.scoped_session.query(Rule).all()]


def remove_rules():
    current_app.scoped_session.query(Rule).delete(synchronize_session=False)
    current_app.scoped_session.commit()
    return 204
