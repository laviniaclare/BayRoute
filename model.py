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
	agency_id = Column(String(30), primary_key = True)
	agency_name = Column(String(30), nullable=False)
	agency_url = Column(String(64), nullable = False)
	agency_timezone = Column(String(30), nullable=False)
	agency_lang = Column(String(10), nullable=False)
	agency_phone = Column(String(20), nullable=True)

def get_agency_routes(agency):
	pass

def get_all_agencies():
	pass




class Route(Base):
	__tablename__='gtfs_routes'
	route_id = Column(String(10), primary_key = True)
	route_short_name = Column(String(10), nullable = True)
	route_long_name = Column(String(30), nullable=True)
	route_type = Column(Integer, nullable=True)
	agency_id=Column(Integer, ForeignKey('gtfs_agency.agency_id'))

	agency = relationship("Agency",
		primaryjoin="Agency.agency_id==Route.agency_id")

def get_route_stops(route):
	pass

	


class Trip(Base):
	__tablename__='gtfs_trips'
	trip_id=Column(Integer, primary_key=True)
	service_id= Column(Integer, nullable=True)
	trip_headsign=Column(String(10), nullable=True)
	direction_id=Column(Integer, nullable=True)
	route_id=Column(Integer, ForeignKey('gtfs_routes.route_id'))
	direction_id=Column(Integer, nullable=True)


	route = relationship("Route",
		primaryjoin="Route.route_id==Trip.route_id")

	


class Stop_Time(Base):
	__tablename__='gtfs_stop_times'
	trip_id = Column(Integer, ForeignKey('gtfs_trips.trip_id'), primary_key=True)
	stop_id = Column(Integer, ForeignKey('gtfs_stops.stop_id'), primary_key=True)
	stop_sequence=Column(Integer, primary_key=True)
	arrival_time=Column(String(30))
	departure_time=Column(String(30))

	trip = relationship("Trip",
			primaryjoin="Trip.trip_id==Stop_Time.trip_id")

	stop = relationship("Stop", 
		primaryjoin="Stop.stop_id==Stop_Time.stop_id")
	


class Stop(Base):
	__tablename__='gtfs_stops'
	stop_id = Column(Integer, primary_key = True)
	stop_name = Column(String, nullable = True)
	stop_lat = Column(Float)
	stop_lon=Column(Float)
	zone_id=Column(Integer, nullable=True)




class Calender(Base):
	__tablename__=('gtfs_calender')

	service_id=Column(Integer, primary_key=True)
	monday=Column(Integer)
	tuesday=Column(Integer)
	wednesday=Column(Integer)
	thursday=Column(Integer)
	friday=Column(Integer)
	saturday=Column(Integer)
	sunday=Column(Integer)
	start_date=Column(Integer)
	end_date=Column(Integer)



class Fair_attributes(Base):
	__tablename__='gtfs_fair_attributes'
	fare_id=Column(Integer, primary_key=True)
	price=Column(Integer)
	currency_type=Column(String(10))
	payment_method=Column(Integer)
	transfers=Column(Integer)
