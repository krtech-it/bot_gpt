from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


sqlite_database = "sqlite:///bot.db"
engine = create_engine(sqlite_database)


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, index=True, primary_key=True)
    id_user = Column(Integer, index=True, unique=True)
    name = Column(String)


class DataBaseWork:
    @classmethod
    def check_db(cls):
        with Session(autoflush=False, bind=engine) as db:
            try:
                db.query(Person).all()
            except sqlalchemy.exc.OperationalError:
                return False
            else:
                return True

    @classmethod
    def start_db(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def get_user(cls, user_id):
        with Session(autoflush=False, bind=engine) as db:
            user = db.query(Person).filter(Person.id_user == user_id).first()
        return user

    @classmethod
    def create_user(cls, user_id, name):
        with Session(autoflush=False, bind=engine) as db:
            user = Person(name=name, id_user=user_id)
            db.add(user)
            db.commit()
        return cls.get_user(user_id)