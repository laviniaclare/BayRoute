from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


# ENGINE = create_engine("INSERT THING HERE PLZ", echo = False)
# Session = scoped_session(sessionmaker(bind = ENGINE, autocommit = False, autoflush = False))

# Base = declarative_base()
# Base.query = Session.query_property()

####Classes got here (Do I need classes?  What are they? Line, System, et?)

# class System(Base):
# 	__tablename__='systems'


# class Lines(Base):
# 	__tablename__='lines'