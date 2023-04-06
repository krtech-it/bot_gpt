from sqlalchemy import Column, Integer, String, ForeignKey
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


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey('people.id'), nullable=False)


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

    @classmethod
    def get_all_rooms_user(cls, user_id):
        with Session(autoflush=False, bind=engine) as db:
            rooms = db.query(
                Person.id,
                Person.id_user,
                Person.name,
                Room.title
            ).join(Room).filter(Person.id_user==user_id).all()
        return rooms

    @classmethod
    def get_room(cls, room_id):
        with Session(autoflush=False, bind=engine) as db:
            room = db.query(Room).filter(Room.id==room_id).first()
        return room

    @classmethod
    def create_room(cls, user_id, title):
        with Session(autoflush=False, bind=engine) as db:
            room = Room(owner_id=user_id, title=title)
            db.add(room)
            db.commit()
            room_id = room.id
        return cls.get_room(room_id)
