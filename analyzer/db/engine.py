from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session


def create_scoped_session() -> Session:
    engine = create_engine('sqlite://///Users/mganjin/PycharmProjects/SnortRuleGenerator/analyzer/base.db')

    return scoped_session(sessionmaker(bind=engine))
