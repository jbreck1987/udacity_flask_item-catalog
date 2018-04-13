import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager


Base = declarative_base()


class Restaurant(Base):

    # Set name of DB table associated
    # with this ORM class
    __tablename__ = 'restaurant'

    # Create mappings (table columns)
    Id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.Id
        }

class MenuItem(Base):

    # Set name of DB table associated
    # with this ORM class
    __tablename__ = 'menu_item'

    # Create mappings (table columns)
    name = Column(String(80), nullable=False)
    Id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.Id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.Id,
            'description': self.description,
            'price': self.price,
            'course': self.course,
            'restaurant_id': self.restaurant_id
        }


# END OF FILE
# create engine to be used by app modules
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# def create_db_session():
     # Session = sessionmaker(bind=engine)
     # return Session()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
