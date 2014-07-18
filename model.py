from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


ENGINE = create_engine("sqlite:///transit.db", echo = False)
Session = scoped_session(sessionmaker(bind = ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = Session.query_property()

####Classes go here
#routes.txt route_id > trips.txt trip_id > stop_times.txt stop_id > stops.txt stop_id



class Agency(Base):
	__tablename__='gtfs_agency'
	agency_id = Column(Integer, primary_key = True)
	agency_name = Column(String(30), nullable = True)
	agency_url = Column(String(64), nullable = True)
	agency_timezone = Column(String(30), nullable=True)
	agency_lang = Column(String(10), nullable=True)
	agency_phone = Column(String(20), nullable=True)

def get_agency_routes(agency):
	pass




class Route(Base):
	__tablename__='gtfs_routes'
	route_id = Column(String(10), primary_key = True)
	route_short_name = Column(String(10), nullable = True)
	route_long_name = Column(String(30), nullable=True)
	route_type = Column(Integer, nullable=True)
	agency_id=Column(Integer, ForeignKey('agencys.id'))

	agency = relationship("Agency",
		backref=backref("routes", order_by=id))

	


class Trip(Base):
	__tablename__='gtfs_trips'
	trip_id=Column(integer, primary_key=True)
	service_id= Column(Integer, nullable=True)
	trip_headsign=Column(String(10), nullable=True)
	direction_id=Column(Integer, nullable=True)
	route_id=Column(Integer, ForeignKey('routes.id'))
	direction_id=Column(Integer, nullable=True)


	route = relationship("Route",
		backref=backref("trips", order_by=id))

	


class Stop_Time(Base):
	__tablename__='gtfs_stop_times'
	id = Column(Integer, primary_key=True)
	trip_id = Column(Integer, ForeignKey('trips.id'))
	stop_id = Column(Integer, ForeignKey('stops.id'))
	stop_sequence=Column(Integer)
	arrival_time=Column(String(30), nullable=True)
	departure_time=Column(String(30), nullable=True)

	trip = relationship("Trip",
		backref=backref("stop_times", order_by=id))

	stop = relationship("Stop",
		backref=backref("stop_times", order_by=id))




class Stop(Base):
	__tablename__='gtfs_stops'
	stop_id = Column(Integer, primary_key = True)
	stop_name = Column(String, nullable = True)
	stop_lat = Column(Float)
	stop_lon=Column(Float)
	zone_id=Column(Integer, nullable=True)





class Calender(Base):
	__tablename__=('calender')
	service_id=Column(Integer, ForeignKey('trips.service_id'))
	monday=Column(Integer)
	tuesday=Column(Integer)
	wednesday=Column(Integer)
	thursday=Column(Integer)
	friday=Column(Integer)
	saturday=Column(Integer)
	sunday=Column(Integer)
	start_date=Column(Integer)
	end_date=Column(Integer)

	stop = relationship("Trip",
		backref=backref("calender", order_by=id))

class Fair_attributes(Base):
	pass
	#fare_id,price,currency_type,payment_method,transfers


