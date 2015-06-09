import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


ENGINE = create_engine(os.environ.get("DATABASE_URL", "sqlite:///transit.db"), echo=False)
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = Session.query_property()

####Classes go here
#routes.txt route_id > trips.txt trip_id > stop_times.txt stop_id > stops.txt stop_id


class Agency(Base):
    __tablename__ = 'gtfs_agency'
    agency_id = Column(String(30), primary_key=True)
    agency_name = Column(String(30), nullable=False)
    agency_url = Column(String(64), nullable=False)
    agency_timezone = Column(String(30), nullable=False)
    agency_lang = Column(String(10), nullable=False)
    agency_phone = Column(String(20), nullable=True)


def get_agency_routes(agency_id):
    agency_routes = Session.query(Route).filter_by(agency_id=agency_id).all()
    return agency_routes


def get_all_agencies():
    all_agencies = Session.query(Agency).all()
    return all_agencies


def get_agency_name_dict():
    agencies_id_to_name = {'3D': 'Tridelta Transit',
                           'AB': 'AirBART',
                           'AC': 'AC Transit',
                           'AM': 'Capitol Corridor',
                           'AT': 'Angel Island Ferry',
                           'AY': 'American Canyon Transit (Vine Transit)',
                           'BA': 'BART',
                           'BG': 'Blue and Gold Fleet',
                           'CC': 'County Connection',
                           'CE': 'Ace Rail',
                           'CT': 'CalTrain',
                           'DE': 'Dumbarton Express',
                           'EM': 'EmeryGoRound (Free shuttle)',
                           'FS': 'FAST Transit',
                           'GF': 'Golden Gate Ferry',
                           'GG': 'Golden Gate Transit',
                           'HF': 'Alcatraz Cruises',
                           'MA': 'Marin Transit',
                           'MS': 'Marguerite Shuttle (Free Stanford shuttle)',
                           'PE': 'Petaluma Transit',
                           'RV': 'Delta Breeze Transit (Rio Vista City)',
                           'SB': 'San Francisco Bay Ferry',
                           'SC': 'Vally Transportation Authority',
                           'SF': 'SFMTA (Muni)',
                           'SM': 'SamTrans',
                           'SO': 'Sonoma County Transit',
                           'SR': 'CityBus (Santa Rosa)',
                           'ST': 'Soltrans',
                           'UC': 'Union City Transit',
                           'VC': 'City Coach',
                           'VN': 'The Vine',
                           'WC': 'WestCat',
                           'WH': 'Wheels Bus',
                           'YV': 'Yountville Trolley (Free shuttle)'
                           }
    # name = agencies_id_to_name[agency_id]
    return agencies_id_to_name


class Route(Base):
    __tablename__ = 'gtfs_routes'
    route_id = Column(String(10), primary_key=True)
    route_short_name = Column(String(10), nullable=True)
    route_long_name = Column(String(30), nullable=True)
    route_type = Column(Integer, nullable=True)
    agency_id = Column(Integer, ForeignKey('gtfs_agency.agency_id'))

    agency = relationship("Agency",
                          primaryjoin="Agency.agency_id==Route.agency_id")


def get_route_trips(route_id):
    trips = []
    trip1 = Session.query(Trip).filter_by(route_id=route_id).filter_by(direction_id=1).first()
    trip2 = Session.query(Trip).filter_by(route_id=route_id).filter_by(direction_id=0).first()
    if trip1:
        trips.append(trip1)
    if trip2:
        trips.append(trip2)
    #trips=Session.query(Trip).filter_by(route_id=route_id).all()
    return trips


def get_all_stops_on_route(route_id):
    trips = get_route_trips(route_id)      # <--- outputs list of trip objects in route
    trip_ids = []

    for trip in trips:
        trip_ids.append(trip.trip_id)     # putting all the trip_ids into a list

    stop_times = get_stops_by_trip_ids(trip_ids)
    lat_longs_on_route = {}
    for stop_time in stop_times:
        if not stop_time.trip_id in lat_longs_on_route.keys():
            lat_longs_on_route[stop_time.trip_id] = []
        lat = stop_time.stop.stop_lat
        lon = stop_time.stop.stop_lon
        lat_longs_on_route[stop_time.trip_id].append([lat, lon])

    return lat_longs_on_route


class Trip(Base):
    __tablename__ = 'gtfs_trips'
    trip_id = Column(Integer, primary_key=True)
    service_id = Column(Integer, nullable=True)
    trip_headsign = Column(String(10), nullable=True)
    direction_id = Column(Integer, nullable=True)
    route_id = Column(Integer, ForeignKey('gtfs_routes.route_id'))
    direction_id = Column(Integer, nullable=True)

    route = relationship("Route",
                         primaryjoin="Route.route_id==Trip.route_id")


class Stop_Time(Base):
    __tablename__ = 'gtfs_stop_times'
    trip_id = Column(Integer, ForeignKey('gtfs_trips.trip_id'), primary_key=True)
    stop_id = Column(Integer, ForeignKey('gtfs_stops.stop_id'), primary_key=True)
    stop_sequence = Column(Integer, primary_key=True)
    arrival_time = Column(String(30))
    departure_time = Column(String(30))

    trip = relationship("Trip",
                        primaryjoin="Trip.trip_id==Stop_Time.trip_id")

    stop = relationship("Stop",
                        primaryjoin="Stop.stop_id==Stop_Time.stop_id")


def get_stops_by_trip_ids(trip_ids):
    stop_time_objects = Session.query(Stop_Time).filter(Stop_Time.trip_id.in_(trip_ids)).join(Stop).order_by('trip_id, stop_sequence').all()
    return stop_time_objects


class Stop(Base):
    __tablename__ = 'gtfs_stops'
    stop_id = Column(Integer, primary_key=True)
    stop_name = Column(String, nullable=True)
    stop_lat = Column(Float)
    stop_lon = Column(Float)
    zone_id = Column(Integer, nullable=True)


def get_stop_by_id(stop_id):
    stop = Session.query(Stop).filter_by(stop_id=stop_id).all()
    stop = stop[0]
    return stop


def get_stop_lat_long(stop_id):
    lat_long = []
    stop = Session.query(Stop).filter_by(stop_id=stop_id).all()
    stop = stop[0]
    lat = stop.stop_lat
    lon = stop.stop_lon
    lat_long.append(lat)
    lat_long.append(lon)
    return lat_long


class Calender(Base):
    __tablename__ = ('gtfs_calender')

    service_id = Column(Integer, primary_key=True)
    monday = Column(Integer)
    tuesday = Column(Integer)
    wednesday = Column(Integer)
    thursday = Column(Integer)
    friday = Column(Integer)
    saturday = Column(Integer)
    sunday = Column(Integer)
    start_date = Column(Integer)
    end_date = Column(Integer)


class Fare_attributes(Base):
    __tablename__ = 'gtfs_fare_attributes'
    fare_id = Column(Integer, primary_key=True)
    price = Column(Integer)
    currency_type = Column(String(10))
    payment_method = Column(Integer)
    transfers = Column(Integer)


def agency_to_routes_dict():
    output = {
        'FS': {
            'F S_30': {
                'name': '30',
                'id': 'FS_30'
            },
            'FS_1': {
                'name': '1',
                'id': 'FS_1'
            },
            'FS_2': {
                'name': '2',
                'id': 'FS_2'
            },
            'FS_3': {
                'name': '3',
                'id': 'FS_3'
            },
            'FS_4': {
                'name': '4',
                'id': 'FS_4'
            },
            'FS_5': {
                'name': '5',
                'id': 'FS_5'
            },
            'FS_6': {
                'name': '6',
                'id': 'FS_6'
            },
            'FS_20': {
                'name': '20',
                'id': 'FS_20'
            },
            'FS_8': {
                'name': '8',
                'id': 'FS_8'
            },
            'FS_7': {
                'name': '7',
                'id': 'FS_7'
            },
            'FS_90': {
                'name': '90',
                'id': 'FS_90'
            },
            'FS_40': {
                'name': '40',
                'id': 'FS_40'
            },
            'FS_Travis AFB': {
                'name': 'Travis AFB',
                'id': 'FS_Travis AFB'
            },
            'FS_7T': {
                'name': '7T',
                'id': 'FS_7T'
            }
            },
        'WC': {
            'WC_17': {
                'name': '17',
                'id': 'WC_17'
            },
            'WC_LYNX': {
                'name': 'LYNX',
                'id': 'WC_LYNX'
            },
            'WC_JL': {
                'name': 'JL',
                'id': 'WC_JL'
            },
            'WC_JR': {
                'name': 'JR',
                'id': 'WC_JR'
            },
            'WC_16': {
                'name': '16',
                'id': 'WC_16'
            },
            'WC_15': {
                'name': '15',
                'id': 'WC_15'
            },
            'WC_12': {
                'name': '12',
                'id': 'WC_12'
            },
            'WC_11': {
                'name': '11',
                'id': 'WC_11'
            },
            'WC_10': {
                'name': '10',
                'id': 'WC_10'
            },
            'WC_30Z': {
                'name': '30Z',
                'id': 'WC_30Z'
            },
            'WC_C3': {
                'name': 'C3',
                'id': 'WC_C3'
            },
            'WC_JPX': {
                'name': 'JPX',
                'id': 'WC_JPX'
            },
            'WC_JX': {
                'name': 'JX',
                'id': 'WC_JX'
            },
            'WC_19': {
                'name': '19',
                'id': 'WC_19'
            },
            'WC_18': {
                'name': '18',
                'id': 'WC_18'
            }
            },
        'BA': {
            'BA_MILL/RICH': {
                'name': 'MILL/RICH',
                'id': 'BA_MILL/RICH'
            },
            'BA_FREMONT/DALY': {
                'name': 'FREMONT/DALY',
                'id': 'BA_FREMONT/DALY'
            },
            'BA_DUBLIN/DALY': {
                'name': 'DUBLIN/DALY',
                'id': 'BA_DUBLIN/DALY'
            },
            'BA_DALY/FREMONT': {
                'name': 'DALY/FREMONT',
                'id': 'BA_DALY/FREMONT'
            },
            'BA_RICH/MILL': {
                'name': 'RICH/MILL',
                'id': 'BA_RICH/MILL'
            },
            'BA_BAY PT/SFIA': {
                'name': 'BAY PT/SFIA',
                'id': 'BA_BAY PT/SFIA'
            },
            'BA_SFIA/BAY PT': {
                'name': 'SFIA/BAY PT',
                'id': 'BA_SFIA/BAY PT'
            },
            'BA_RICH/FREMONT': {
                'name': 'RICH/FREMONT',
                'id': 'BA_RICH/FREMONT'
            },
            'BA_FREMONT/RICH': {
                'name': 'FREMONT/RICH',
                'id': 'BA_FREMONT/RICH'
            },
            'BA_DALY/DUBLIN': {
                'name': 'DALY/DUBLIN',
                'id': 'BA_DALY/DUBLIN'
            }
            },
        'DE': {
            'DE_DB1': {
                'name': 'DB1',
                'id': 'DE_DB1'
            },
            'DE_DB': {
                'name': 'DB',
                'id': 'DE_DB'
            }
            },
        'VC': {
            'VC_1': {
                'name': '1',
                'id': 'VC_1'
            },
            'VC_2': {
                'name': '2',
                'id': 'VC_2'
            },
            'VC_4': {
                'name': '4',
                'id': 'VC_4'
            },
            'VC_5': {
                'name': '5',
                'id': 'VC_5'
            },
            'VC_6': {
                'name': '6',
                'id': 'VC_6'
            },
            'VC_8': {
                'name': '8',
                'id': 'VC_8'
            }
            },
        'WH': {
            'WH_601': {
                'name': '601',
                'id': 'WH_601'
            },
            'WH_602': {
                'name': '602',
                'id': 'WH_602'
            },
            'WH_604': {
                'name': '604',
                'id': 'WH_604'
            },
            'WH_8': {
                'name': '8',
                'id': 'WH_8'
            },
            'WH_9': {
                'name': '9',
                'id': 'WH_9'
            },
            'WH_403': {
                'name': '403',
                'id': 'WH_403'
            },
            'WH_70X': {
                'name': '70X',
                'id': 'WH_70X'
            },
            'WH_1': {
                'name': '1',
                'id': 'WH_1'
            },
            'WH_2': {
                'name': '2',
                'id': 'WH_2'
            },
            'WH_3': {
                'name': '3',
                'id': 'WH_3'
            },
            'WH_53': {
                'name': '53',
                'id': 'WH_53'
            },
            'WH_20X': {
                'name': '20X',
                'id': 'WH_20X'
            },
            'WH_54': {
                'name': '54',
                'id': 'WH_54'
            },
            'WH_14': {
                'name': '14',
                'id': 'WH_14'
            },
            'WH_12V': {
                'name': '12V',
                'id': 'WH_12V'
            },
            'WH_12': {
                'name': '12',
                'id': 'WH_12'
            },
            'WH_10': {
                'name': '10',
                'id': 'WH_10'
            },
            'WH_11': {
                'name': '11',
                'id': 'WH_11'
            },
            'WH_70XV': {
                'name': '70XV',
                'id': 'WH_70XV'
            },
            'WH_703': {
                'name': '703',
                'id': 'WH_703'
            },
            'WH_702': {
                'name': '702',
                'id': 'WH_702'
            },
            'WH_704': {
                'name': '704',
                'id': 'WH_704'
            },
            'WH_15A': {
                'name': '15A',
                'id': 'WH_15A'
            },
            'WH_R': {
                'name': 'R',
                'id': 'WH_R'
            }
            },
        'BG': {
            'BG_1': {
                'name': 'TIBURON',
                'id': 'BG_1'
            },
            'BG_2': {
                'name': 'ANGEL ISLAND',
                'id': 'BG_2'
            },
            'BG_SAUSALITO': {
                'name': 'SAUSALITO',
                'id': 'BG_SAUSALITO'
            }
            },
        'HF': {
            'HF_Early Bird': {
                'name': 'Early Bird',
                'id': 'HF_Early Bird'
            },
            'HF_Night Tour': {
                'name': 'Night Tour',
                'id': 'HF_Night Tour'
            },
            'HF_Day Tour': {
                'name': 'Day Tour',
                'id': 'HF_Day Tour'
            }
            },
        '3D': {
            '3D_395': {
                'name': '395',
                'id': '3D_395'
            },
            '3D_300': {
                'name': '300',
                'id': '3D_300'
            },
            '3D_391': {
                'name': '391',
                'id': '3D_391'
            },
            '3D_392': {
                'name': '392',
                'id': '3D_392'
            },
            '3D_393': {
                'name': '393',
                'id': '3D_393'
            },
            '3D_383': {
                'name': '383',
                'id': '3D_383'
            },
            '3D_201': {
                'name': '201',
                'id': '3D_201'
            },
            '3D_394': {
                'name': '394',
                'id': '3D_394'
            },
            '3D_389': {
                'name': '389',
                'id': '3D_389'
            },
            '3D_388': {
                'name': '388',
                'id': '3D_388'
            },
            '3D_385': {
                'name': '385',
                'id': '3D_385'
            },
            '3D_387': {
                'name': '387',
                'id': '3D_387'
            },
            '3D_386': {
                'name': '386',
                'id': '3D_386'
            },
            '3D_200': {
                'name': '200',
                'id': '3D_200'
            },
            '3D_379': {
                'name': '379',
                'id': '3D_379'
            },
            '3D_390': {
                'name': '390',
                'id': '3D_390'
            },
            '3D_380': {
                'name': '380',
                'id': '3D_380'
            }
            },
        'RV': {
            'RV_50': {
                'name': '50',
                'id': 'RV_50'
            },
            'RV_52': {
                'name': '52',
                'id': 'RV_52'
            }
            },
        'PE': {
            'PE_1T': {
                'name': '1T',
                'id': 'PE_1T'
            },
            'PE_24': {
                'name': '24',
                'id': 'PE_24'
            },
            'PE_11': {
                'name': '11',
                'id': 'PE_11'
            },
            'PE_33': {
                'name': '33',
                'id': 'PE_33'
            },
            'PE_1': {
                'name': '1',
                'id': 'PE_1'
            },
            'PE_2': {
                'name': '2',
                'id': 'PE_2'
            },
            'PE_3': {
                'name': '3',
                'id': 'PE_3'
            }
            },
        'YV': {
            'YV_SHUTTLE': {
                'name': 'SHUTTLE',
                'id': 'YV_SHUTTLE'
            }
            },
        'EM': {
            'EM_POWELL': {
                'name': 'POWELL',
                'id': 'EM_POWELL'
            },
            'EM_HOLLIS': {
                'name': 'HOLLIS',
                'id': 'EM_HOLLIS'
            },
            'EM_WATERGATE': {
                'name': 'WATERGATE',
                'id': 'EM_WATERGATE'
            }
            },
        'AC': {
            'AC_386': {
                'name': '386',
                'id': 'AC_386'
            },
            'AC_95': {
                'name': '95',
                'id': 'AC_95'
            },
            'AC_OX': {
                'name': 'OX',
                'id': 'AC_OX'
            },
            'AC_72M': {
                'name': '72M',
                'id': 'AC_72M'
            },
            'AC_72R': {
                'name': '72R',
                'id': 'AC_72R'
            },
            'AC_51B': {
                'name': '51B',
                'id': 'AC_51B'
            },
            'AC_314': {
                'name': '314',
                'id': 'AC_314'
            },
            'AC_99': {
                'name': '99',
                'id': 'AC_99'
            },
            'AC_98': {
                'name': '98',
                'id': 'AC_98'
            },
            'AC_93': {
                'name': '93',
                'id': 'AC_93'
            },
            'AC_51A': {
                'name': '51A',
                'id': 'AC_51A'
            },
            'AC_94': {
                'name': '94',
                'id': 'AC_94'
            },
            'AC_97': {
                'name': '97',
                'id': 'AC_97'
            },
            'AC_251': {
                'name': '251',
                'id': 'AC_251'
            },
            'AC_BSN': {
                'name': 'BSN',
                'id': 'AC_BSN'
            },
            'AC_BSD': {
                'name': 'BSD',
                'id': 'AC_BSD'
            },
            'AC_65': {
                'name': '65',
                'id': 'AC_65'
            },
            'AC_67': {
                'name': '67',
                'id': 'AC_67'
            },
            'AC_60': {
                'name': '60',
                'id': 'AC_60'
            },
            'AC_LC': {
                'name': 'LC',
                'id': 'AC_LC'
            },
            'AC_62': {
                'name': '62',
                'id': 'AC_62'
            },
            'AC_LA': {
                'name': 'LA',
                'id': 'AC_LA'
            },
            'AC_851': {
                'name': '851',
                'id': 'AC_851'
            },
            'AC_FS': {
                'name': 'FS',
                'id': 'AC_FS'
            },
            'AC_88': {
                'name': '88',
                'id': 'AC_88'
            },
            'AC_89': {
                'name': '89',
                'id': 'AC_89'
            },
            'AC_83': {
                'name': '83',
                'id': 'AC_83'
            },
            'AC_86': {
                'name': '86',
                'id': 'AC_86'
            },
            'AC_85': {
                'name': '85',
                'id': 'AC_85'
            },
            'AC_NXC': {
                'name': 'NXC',
                'id': 'AC_NXC'
            },
            'AC_840': {
                'name': '840',
                'id': 'AC_840'
            },
            'AC_11': {
                'name': '11',
                'id': 'AC_11'
            },
            'AC_12': {
                'name': '12',
                'id': 'AC_12'
            },
            'AC_14': {
                'name': '14',
                'id': 'AC_14'
            },
            'AC_18': {
                'name': '18',
                'id': 'AC_18'
            },
            'AC_376': {
                'name': '376',
                'id': 'AC_376'
            },
            'AC_NX4': {
                'name': 'NX4',
                'id': 'AC_NX4'
            },
            'AC_1R': {
                'name': '1R',
                'id': 'AC_1R'
            },
            'AC_NX1': {
                'name': 'NX1',
                'id': 'AC_NX1'
            },
            'AC_232': {
                'name': '232',
                'id': 'AC_232'
            },
            'AC_NX3': {
                'name': 'NX3',
                'id': 'AC_NX3'
            },
            'AC_NX2': {
                'name': 'NX2',
                'id': 'AC_NX2'
            },
            'AC_275': {
                'name': '275',
                'id': 'AC_275'
            },
            'AC_NX': {
                'name': 'NX',
                'id': 'AC_NX'
            },
            'AC_NL': {
                'name': 'NL',
                'id': 'AC_NL'
            },
            'AC_1': {
                'name': '1',
                'id': 'AC_1'
            },
            'AC_SB': {
                'name': 'SB',
                'id': 'AC_SB'
            },
            'AC_7': {
                'name': '7',
                'id': 'AC_7'
            },
            'AC_39': {
                'name': '39',
                'id': 'AC_39'
            },
            'AC_37': {
                'name': '37',
                'id': 'AC_37'
            },
            'AC_32': {
                'name': '32',
                'id': 'AC_32'
            },
            'AC_31': {
                'name': '31',
                'id': 'AC_31'
            },
            'AC_212': {
                'name': '212',
                'id': 'AC_212'
            },
            'AC_210': {
                'name': '210',
                'id': 'AC_210'
            },
            'AC_Z': {
                'name': 'Z',
                'id': 'AC_Z'
            },
            'AC_216': {
                'name': '216',
                'id': 'AC_216'
            },
            'AC_217': {
                'name': '217',
                'id': 'AC_217'
            },
            'AC_215': {
                'name': '215',
                'id': 'AC_215'
            },
            'AC_54': {
                'name': '54',
                'id': 'AC_54'
            },
            'AC_57': {
                'name': '57',
                'id': 'AC_57'
            },
            'AC_': {
                'name': '',
                'id': 'AC_'
            },
            'AC_356': {
                'name': '356',
                'id': 'AC_356'
            },
            'AC_W': {
                'name': 'W',
                'id': 'AC_W'
            },
            'AC_V': {
                'name': 'V',
                'id': 'AC_V'
            },
            'AC_H': {
                'name': 'H',
                'id': 'AC_H'
            },
            'AC_J': {
                'name': 'J',
                'id': 'AC_J'
            },
            'AC_M': {
                'name': 'M',
                'id': 'AC_M'
            },
            'AC_L': {
                'name': 'L',
                'id': 'AC_L'
            },
            'AC_O': {
                'name': 'O',
                'id': 'AC_O'
            },
            'AC_C': {
                'name': 'C',
                'id': 'AC_C'
            },
            'AC_B': {
                'name': 'B',
                'id': 'AC_B'
            },
            'AC_E': {
                'name': 'E',
                'id': 'AC_E'
            },
            'AC_G': {
                'name': 'G',
                'id': 'AC_G'
            },
            'AC_F': {
                'name': 'F',
                'id': 'AC_F'
            },
            'AC_20': {
                'name': '20',
                'id': 'AC_20'
            },
            'AC_21': {
                'name': '21',
                'id': 'AC_21'
            },
            'AC_22': {
                'name': '22',
                'id': 'AC_22'
            },
            'AC_25': {
                'name': '25',
                'id': 'AC_25'
            },
            'AC_26': {
                'name': '26',
                'id': 'AC_26'
            },
            'AC_200': {
                'name': '200',
                'id': 'AC_200'
            },
            'AC_48': {
                'name': '48',
                'id': 'AC_48'
            },
            'AC_49': {
                'name': '49',
                'id': 'AC_49'
            },
            'AC_46': {
                'name': '46',
                'id': 'AC_46'
            },
            'AC_47': {
                'name': '47',
                'id': 'AC_47'
            },
            'AC_58L': {
                'name': '58L',
                'id': 'AC_58L'
            },
            'AC_45': {
                'name': '45',
                'id': 'AC_45'
            },
            'AC_40': {
                'name': '40',
                'id': 'AC_40'
            },
            'AC_802': {
                'name': '802',
                'id': 'AC_802'
            },
            'AC_801': {
                'name': '801',
                'id': 'AC_801'
            },
            'AC_800': {
                'name': '800',
                'id': 'AC_800'
            },
            'AC_805': {
                'name': '805',
                'id': 'AC_805'
            },
            'AC_P': {
                'name': 'P',
                'id': 'AC_P'
            },
            'AC_S': {
                'name': 'S',
                'id': 'AC_S'
            },
            'AC_239': {
                'name': '239',
                'id': 'AC_239'
            },
            'AC_73': {
                'name': '73',
                'id': 'AC_73'
            },
            'AC_72': {
                'name': '72',
                'id': 'AC_72'
            },
            'AC_71': {
                'name': '71',
                'id': 'AC_71'
            },
            'AC_70': {
                'name': '70',
                'id': 'AC_70'
            },
            'AC_76': {
                'name': '76',
                'id': 'AC_76'
            },
            'AC_75': {
                'name': '75',
                'id': 'AC_75'
            },
            'AC_74': {
                'name': '74',
                'id': 'AC_74'
            },
            'AC_339': {
                'name': '339',
                'id': 'AC_339'
            },
            'AC_52': {
                'name': '52',
                'id': 'AC_52'
            },
            'AC_CB': {
                'name': 'CB',
                'id': 'AC_CB'
            }
        },
        'AB':     {
            'AB_SHUTTLE': {
                'name': 'SHUTTLE',
                'id  ': 'AB_SHUTTLE'
            }
        },
        'SM':     {
            'SM_24': {
                'name': '24',
                'id  ': 'SM_24'
            },
            'SM_43': {
                'name': '43',
                'id': 'SM_43'
            },
            'SM_87': {
                'name': '87',
                'id': 'SM_87'
            },
            'SM_292': {
                'name': '292',
                'id': 'SM_292'
            },
            'SM_67': {
                'name': '67',
                'id': 'SM_67'
            },
            'SM_274': {
                'name': '274',
                'id': 'SM_274'
            },
            'SM_ECR': {
                'name': 'ECR',
                'id': 'SM_ECR'
            },
            'SM_140': {
                'name': '140',
                'id': 'SM_140'
            },
            'SM_141': {
                'name': '141',
                'id': 'SM_141'
            },
            'SM_270': {
                'name': '270',
                'id': 'SM_270'
            },
            'SM_FlxS': {
                'name': 'FlxS',
                'id': 'SM_FlxS'
            },
            'SM_80': {
                'name': '80',
                'id': 'SM_80'
            },
            'SM_296': {
                'name': '296',
                'id': 'SM_296'
            },
            'SM_297': {
                'name': '297',
                'id': 'SM_297'
            },
            'SM_294': {
                'name': '294',
                'id': 'SM_294'
            },
            'SM_295': {
                'name': '295',
                'id': 'SM_295'
            },
            'SM_278': {
                'name': '278',
                'id': 'SM_278'
            },
            'SM_89': {
                'name': '89',
                'id': 'SM_89'
            },
            'SM_120': {
                'name': '120',
                'id': 'SM_120'
            },
            'SM_121': {
                'name': '121',
                'id': 'SM_121'
            },
            'SM_250': {
                'name': '250',
                'id': 'SM_250'
            },
            'SM_251': {
                'name': '251',
                'id': 'SM_251'
            },
            'SM_256': {
                'name': '256',
                'id': 'SM_256'
            },
            'SM_86': {
                'name': '86',
                'id': 'SM_86'
            },
            'SM_54': {
                'name': '54',
                'id': 'SM_54'
            },
            'SM_275': {
                'name': '275',
                'id': 'SM_275'
            },
            'SM_276': {
                'name': '276',
                'id': 'SM_276'
            },
            'SM_252': {
                'name': '252',
                'id': 'SM_252'
            },
            'SM_39': {
                'name': '39',
                'id': 'SM_39'
            },
            'SM_38': {
                'name': '38',
                'id': 'SM_38'
            },
            'SM_17': {
                'name': '17',
                'id': 'SM_17'
            },
            'SM_KX': {
                'name': 'KX',
                'id': 'SM_KX'
            },
            'SM_37': {
                'name': '37',
                'id': 'SM_37'
            },
            'SM_122': {
                'name': '122',
                'id': 'SM_122'
            },
            'SM_35': {
                'name': '35',
                'id': 'SM_35'
            },
            'SM_261': {
                'name': '261',
                'id': 'SM_261'
            },
            'SM_260': {
                'name': '260',
                'id': 'SM_260'
            },
            'SM_133': {
                'name': '133',
                'id': 'SM_133'
            },
            'SM_FlxP': {
                'name': 'FlxP',
                'id': 'SM_FlxP'
            },
            'SM_131': {
                'name': '131',
                'id': 'SM_131'
            },
            'SM_130': {
                'name': '130',
                'id': 'SM_130'
            },
            'SM_286': {
                'name': '286',
                'id': 'SM_286'
            },
            'SM_281': {
                'name': '281',
                'id': 'SM_281'
            },
            'SM_280': {
                'name': '280',
                'id': 'SM_280'
            },
            'SM_397': {
                'name': '397',
                'id': 'SM_397'
            },
            'SM_118': {
                'name': '118',
                'id': 'SM_118'
            },
            'SM_398': {
                'name': '398',
                'id': 'SM_398'
            },
            'SM_110': {
                'name': '110',
                'id': 'SM_110'
            },
            'SM_112': {
                'name': '112',
                'id': 'SM_112'
            }
        },
        'CC':     {
            'CC_36': {
                'name': '36',
                'id  ': 'CC_36'
            },
            'CC_91X': {
                'name': '91X',
                'id': 'CC_91X'
            },
            'CC_93X': {
                'name': '93X',
                'id': 'CC_93X'
            },
            'CC_95X': {
                'name': '95X',
                'id': 'CC_95X'
            },
            'CC_320': {
                'name': '320',
                'id': 'CC_320'
            },
            'CC_321': {
                'name': '321',
                'id': 'CC_321'
            },
            'CC_97X': {
                'name': '97X',
                'id': 'CC_97X'
            },
            'CC_301': {
                'name': '301',
                'id': 'CC_301'
            },
            'CC_25': {
                'name': '25',
                'id': 'CC_25'
            },
            'CC_20': {
                'name': '20',
                'id': 'CC_20'
            },
            'CC_21': {
                'name': '21',
                'id': 'CC_21'
            },
            'CC_28': {
                'name': '28',
                'id': 'CC_28'
            },
            'CC_649': {
                'name': '649',
                'id': 'CC_649'
            },
            'CC_627': {
                'name': '627',
                'id': 'CC_627'
            },
            'CC_92X': {
                'name': '92X',
                'id': 'CC_92X'
            },
            'CC_315': {
                'name': '315',
                'id': 'CC_315'
            },
            'CC_314': {
                'name': '314',
                'id': 'CC_314'
            },
            'CC_316': {
                'name': '316',
                'id': 'CC_316'
            },
            'CC_311': {
                'name': '311',
                'id': 'CC_311'
            },
            'CC_310': {
                'name': '310',
                'id': 'CC_310'
            },
            'CC_96X': {
                'name': '96X',
                'id': 'CC_96X'
            },
            'CC_98X': {
                'name': '98X',
                'id': 'CC_98X'
            },
            'CC_35': {
                'name': '35',
                'id': 'CC_35'
            },
            'CC_11': {
                'name': '11',
                'id': 'CC_11'
            },
            'CC_10': {
                'name': '10',
                'id': 'CC_10'
            },
            'CC_17': {
                'name': '17',
                'id': 'CC_17'
            },
            'CC_16': {
                'name': '16',
                'id': 'CC_16'
            },
            'CC_15': {
                'name': '15',
                'id': 'CC_15'
            },
            'CC_14': {
                'name': '14',
                'id': 'CC_14'
            },
            'CC_19': {
                'name': '19',
                'id': 'CC_19'
            },
            'CC_18': {
                'name': '18',
                'id': 'CC_18'
            },
            'CC_7': {
                'name': '7',
                'id': 'CC_7'
            },
            'CC_6': {
                'name': '6',
                'id': 'CC_6'
            },
            'CC_5': {
                'name': '5',
                'id': 'CC_5'
            },
            'CC_4': {
                'name': '4',
                'id': 'CC_4'
            },
            'CC_2': {
                'name': '2',
                'id': 'CC_2'
            },
            'CC_1': {
                'name': '1',
                'id': 'CC_1'
            },
            'CC_9': {
                'name': '9',
                'id': 'CC_9'
            }
        },
        'VN':     {
            'VN_5': {
                'name': '5',
                'id  ': 'VN_5'
            },
            'VN_4': {
                'name': '4',
                'id': 'VN_4'
            },
            'VN_7': {
                'name': '7',
                'id': 'VN_7'
            },
            'VN_6': {
                'name': '6',
                'id': 'VN_6'
            },
            'VN_1': {
                'name': '1',
                'id': 'VN_1'
            },
            'VN_3': {
                'name': '3',
                'id': 'VN_3'
            },
            'VN_2': {
                'name': '2',
                'id': 'VN_2'
            },
            'VN_8': {
                'name': '8',
                'id': 'VN_8'
            },
            'VN_11': {
                'name': '11',
                'id': 'VN_11'
            },
            'VN_29': {
                'name': '29',
                'id': 'VN_29'
            },
            'VN_25': {
                'name': '25',
                'id': 'VN_25'
            },
            'VN_21': {
                'name': '21',
                'id': 'VN_21'
            },
            'VN_10': {
                'name': '10',
                'id': 'VN_10'
            }
        },
        'AM':     {
            'AM_CAPITOL': {
                'name': 'CAPITOL',
                'id  ': 'AM_CAPITOL'
            }
        },
        'CE':     {
            'CE_WESTBOUND': {
                'name': 'WESTBOUND',
                'id  ': 'CE_WESTBOUND'
            },
            'CE_EASTBOUND': {
                'name': 'EASTBOUND',
                'id': 'CE_EASTBOUND'
            }
        },
        'GG':     {
            'GG_36': {
                'name': '36',
                'id  ': 'GG_36'
            },
            'GG_8': {
                'name': '8',
                'id': 'GG_8'
            },
            'GG_4': {
                'name': '4',
                'id': 'GG_4'
            },
            'GG_2': {
                'name': '2',
                'id': 'GG_2'
            },
            'GG_71': {
                'name': '71',
                'id': 'GG_71'
            },
            'GG_70': {
                'name': '70',
                'id': 'GG_70'
            },
            'GG_72': {
                'name': '72',
                'id': 'GG_72'
            },
            'GG_74': {
                'name': '74',
                'id': 'GG_74'
            },
            'GG_76': {
                'name': '76',
                'id': 'GG_76'
            },
            'GG_117': {
                'name': '117',
                'id': 'GG_117'
            },
            'GG_54': {
                'name': '54',
                'id': 'GG_54'
            },
            'GG_72X': {
                'name': '72X',
                'id': 'GG_72X'
            },
            'GG_18': {
                'name': '18',
                'id': 'GG_18'
            },
            'GG_56': {
                'name': '56',
                'id': 'GG_56'
            },
            'GG_38': {
                'name': '38',
                'id': 'GG_38'
            },
            'GG_35': {
                'name': '35',
                'id': 'GG_35'
            },
            'GG_10': {
                'name': '10',
                'id': 'GG_10'
            },
            'GG_17': {
                'name': '17',
                'id': 'GG_17'
            },
            'GG_101X': {
                'name': '101X',
                'id': 'GG_101X'
            },
            'GG_93': {
                'name': '93',
                'id': 'GG_93'
            },
            'GG_92': {
                'name': '92',
                'id': 'GG_92'
            },
            'GG_91': {
                'name': '91',
                'id': 'GG_91'
            },
            'GG_97': {
                'name': '97',
                'id': 'GG_97'
            },
            'GG_127': {
                'name': '127',
                'id': 'GG_127'
            },
            'GG_125': {
                'name': '125',
                'id': 'GG_125'
            },
            'GG_126': {
                'name': '126',
                'id': 'GG_126'
            },
            'GG_101': {
                'name': '101',
                'id': 'GG_101'
            },
            'GG_49': {
                'name': '49',
                'id': 'GG_49'
            },
            'GG_40': {
                'name': '40',
                'id': 'GG_40'
            },
            'GG_42': {
                'name': '42',
                'id': 'GG_42'
            },
            'GG_44': {
                'name': '44',
                'id': 'GG_44'
            },
            'GG_45': {
                'name': '45',
                'id': 'GG_45'
            },
            'GG_29': {
                'name': '29',
                'id': 'GG_29'
            },
            'GG_58': {
                'name': '58',
                'id': 'GG_58'
            },
            'GG_27': {
                'name': '27',
                'id': 'GG_27'
            },
            'GG_24': {
                'name': '24',
                'id': 'GG_24'
            },
            'GG_25': {
                'name': '25',
                'id': 'GG_25'
            },
            'GG_22': {
                'name': '22',
                'id': 'GG_22'
            },
            'GG_23': {
                'name': '23',
                'id': 'GG_23'
            },
            'GG_80': {
                'name': '80',
                'id': 'GG_80'
            }
        },
        'GF':     {
            'GF_2': {
                'name': 'SF',
                'id  ': 'GF_2'
            },
            'GF_1': {
                'name': 'LF',
                'id': 'GF_1'
            }
        },
        'AT':     {
            'AT_FERRY': {
                'name': 'FERRY',
                'id  ': 'AT_FERRY'
            }
        },
        'AY':     {
            'AY_SHUTTLE': {
              'name': 'SHUTTLE',
              'id  ': 'AY_SHUTTLE'
            }
        },
        'CT':     {
            'CT_LOCAL': {
              'name': 'LOCAL',
              'id  ': 'CT_LOCAL'
            },
            'CT_BABY BULLET': {
                'name': 'BABY BULLET',
                'id': 'CT_BABY BULLET'
            },
            'CT_LIMITED': {
                'name': 'LIMITED',
                'id': 'CT_LIMITED'
            },
            'CT_SHUTTLE': {
                'name': 'SHUTTLE',
                'id': 'CT_SHUTTLE'
            }
        },
        'MA':     {
            'MA_66': {
                'name': '66',
                'id  ': 'MA_66'
            },
            'MA_259': {
                'name': '259',
                'id': 'MA_259'
            },
            'MA_65': {
                'name': '65',
                'id': 'MA_65'
            },
            'MA_119': {
                'name': '119',
                'id': 'MA_119'
            },
            'MA_61': {
                'name': '61',
                'id': 'MA_61'
            },
            'MA_113': {
                'name': '113',
                'id': 'MA_113'
            },
            'MA_115': {
                'name': '115',
                'id': 'MA_115'
            },
            'MA_139': {
                'name': '139',
                'id': 'MA_139'
            },
            'MA_68': {
                'name': '68',
                'id': 'MA_68'
            },
            'MA_257': {
                'name': '257',
                'id': 'MA_257'
            },
            'MA_233': {
                'name': '233',
                'id': 'MA_233'
            },
            'MA_151': {
                'name': '151',
                'id': 'MA_151'
            },
            'MA_219': {
                'name': '219',
                'id': 'MA_219'
            },
            'MA_154': {
                'name': '154',
                'id': 'MA_154'
            },
            'MA_251': {
                'name': '251',
                'id': 'MA_251'
            },
            'MA_228': {
                'name': '228',
                'id': 'MA_228'
            }
        },
        'SR':     {
            'SR_8': {
                'name': '8',
                'id  ': 'SR_8'
            },
            'SR_9': {
                'name': '9',
                'id': 'SR_9'
            },
            'SR_6': {
                'name': '6',
                'id': 'SR_6'
            },
            'SR_7': {
                'name': '7',
                'id': 'SR_7'
            },
            'SR_4': {
                'name': '4',
                'id': 'SR_4'
            },
            'SR_5': {
                'name': '5',
                'id': 'SR_5'
            },
            'SR_2': {
                'name': '2',
                'id': 'SR_2'
            },
            'SR_3': {
                'name': '3',
                'id': 'SR_3'
            },
            'SR_1': {
                'name': '1',
                'id': 'SR_1'
            },
            'SR_14': {
                'name': '14',
                'id': 'SR_14'
            },
            'SR_15': {
                'name': '15',
                'id': 'SR_15'
            },
            'SR_17': {
                'name': '17',
                'id': 'SR_17'
            },
            'SR_10': {
                'name': '10',
                'id': 'SR_10'
            },
            'SR_11': {
                'name': '11',
                'id': 'SR_11'
            },
            'SR_12': {
                'name': '12',
                'id': 'SR_12'
            },
            'SR_18': {
                'name': '18',
                'id': 'SR_18'
            },
            'SR_19': {
                'name': '19',
                'id': 'SR_19'
            }
        },
        'ST':     {
            'ST_78': {
                'name': '78',
                'id  ': 'ST_78'
            },
            'ST_85': {
                'name': '85',
                'id': 'ST_85'
            },
            'ST_15': {
                'name': '15',
                'id': 'ST_15'
            },
            'ST_80': {
                'name': '80',
                'id': 'ST_80'
            },
            'ST_76': {
                'name': '76',
                'id': 'ST_76'
            },
            'ST_80s': {
                'name': '80s',
                'id': 'ST_80s'
            },
            'ST_5': {
                'name': '5',
                'id': 'ST_5'
            },
            'ST_4': {
                'name': '4',
                'id': 'ST_4'
            },
            'ST_17': {
                'name': '17',
                'id': 'ST_17'
            },
            'ST_6': {
                'name': '6',
                'id': 'ST_6'
            },
            'ST_7': {
                'name': '7',
                'id': 'ST_7'
            },
            'ST_12': {
                'name': '12',
                'id': 'ST_12'
            },
            'ST_1': {
                'name': '1',
                'id': 'ST_1'
            },
            'ST_2': {
                'name': '2',
                'id': 'ST_2'
            },
            'ST_3': {
                'name': '3',
                'id': 'ST_3'
            }
        },
        'SO':     {
            'SO_60X': {
                'name': '60X',
                'id  ': 'SO_60X'
            },
            'SO_48X': {
                'name': '48X',
                'id': 'SO_48X'
            },
            'SO_20X': {
                'name': '20X',
                'id': 'SO_20X'
            },
            'SO_30X': {
                'name': '30X',
                'id': 'SO_30X'
            },
            'SO_66': {
                'name': '66',
                'id': 'SO_66'
            },
            'SO_28': {
                'name': '28',
                'id': 'SO_28'
            },
            'SO_62': {
                'name': '62',
                'id': 'SO_62'
            },
            'SO_60': {
                'name': '60',
                'id': 'SO_60'
            },
            'SO_22': {
                'name': '22',
                'id': 'SO_22'
            },
            'SO_48': {
                'name': '48',
                'id': 'SO_48'
            },
            'SO_46': {
                'name': '46',
                'id': 'SO_46'
            },
            'SO_40': {
                'name': '40',
                'id': 'SO_40'
            },
            'SO_68': {
                'name': '68',
                'id': 'SO_68'
            },
            'SO_44': {
                'name': '44',
                'id': 'SO_44'
            },
            'SO_24': {
                'name': '24',
                'id': 'SO_24'
            },
            'SO_20': {
                'name': '20',
                'id': 'SO_20'
            },
            'SO_12': {
                'name': '12',
                'id': 'SO_12'
            },
            'SO_14': {
                'name': '14',
                'id': 'SO_14'
            },
            'SO_29A': {
                'name': '29A',
                'id': 'SO_29A'
            },
            'SO_29B': {
                'name': '29B',
                'id': 'SO_29B'
            },
            'SO_10': {
                'name': '10',
                'id': 'SO_10'
            },
            'SO_26': {
                'name': '26',
                'id': 'SO_26'
            },
            'SO_38': {
                'name': '38',
                'id': 'SO_38'
            },
            'SO_42': {
                'name': '42',
                'id': 'SO_42'
            },
            'SO_30': {
                'name': '30',
                'id': 'SO_30'
            },
            'SO_32': {
                'name': '32',
                'id': 'SO_32'
            },
            'SO_34': {
                'name': '34',
                'id': 'SO_34'
            }
        },
        'MS':     {
            'MS_Line P': {
                'name': 'Line P',
                'id  ': 'MS_Line P'
            },
            'MS_EB': {
                'name': 'EB',
                'id': 'MS_EB'
            },
            'MS_Research Pk': {
                'name': 'Research Pk',
                'id': 'MS_Research Pk'
            },
            'MS_Line V': {
                'name': 'Line V',
                'id': 'MS_Line V'
            },
            'MS_Line SE': {
                'name': 'Line SE',
                'id': 'MS_Line SE'
            },
            'MS_Line X': {
                'name': 'Line X',
                'id': 'MS_Line X'
            },
            'MS_MedCtr-LOOP': {
                'name': 'MedCtr-LOOP',
                'id': 'MS_MedCtr-LOOP'
            },
            'MS_Line S': {
                'name': 'Line S',
                'id': 'MS_Line S'
            },
            'MS_TECH': {
                'name': 'TECH',
                'id': 'MS_TECH'
            },
            'MS_SLAC': {
                'name': 'SLAC',
                'id': 'MS_SLAC'
            },
            'MS_Line C': {
                'name': 'Line C',
                'id': 'MS_Line C'
            },
            'MS_OCA': {
                'name': 'OCA',
                'id': 'MS_OCA'
            },
            'MS_Line Y': {
                'name': 'Line Y',
                'id': 'MS_Line Y'
            },
            'MS_Line H': {
                'name': 'Line H',
                'id': 'MS_Line H'
            },
            'MS_Ardenwood Ex': {
                'name': 'Ardenwood Ex',
                'id': 'MS_Ardenwood Ex'
            },
            'MS_Bohannon': {
                'name': 'Bohannon',
                'id': 'MS_Bohannon'
            },
            'MS_1050 Arastra': {
                'name': '1050 Arastra',
                'id': 'MS_1050 Arastra'
            },
            'MS_Line HD': {
                'name': 'Line HD',
                'id': 'MS_Line HD'
            },
            'MS_Line N': {
                'name': 'Line N',
                'id': 'MS_Line N'
            },
            'MS_Line O': {
                'name': 'Line O',
                'id': 'MS_Line O'
            }
        },
        'SC':     {
            'SC_140': {
                'name': '140',
                'id  ': 'SC_140'
            },
            'SC_321': {
                'name': '321',
                'id': 'SC_321'
            },
            'SC_55': {
                'name': '55',
                'id': 'SC_55'
            },
            'SC_323': {
                'name': '323',
                'id': 'SC_323'
            },
            'SC_53': {
                'name': '53',
                'id': 'SC_53'
            },
            'SC_52': {
                'name': '52',
                'id': 'SC_52'
            },
            'SC_902': {
                'name': '902',
                'id': 'SC_902'
            },
            'SC_328': {
                'name': '328',
                'id': 'SC_328'
            },
            'SC_180': {
                'name': '180',
                'id': 'SC_180'
            },
            'SC_120': {
                'name': '120',
                'id': 'SC_120'
            },
            'SC_32': {
                'name': '32',
                'id': 'SC_32'
            },
            'SC_304': {
                'name': '304',
                'id': 'SC_304'
            },
            'SC_201': {
                'name': '201',
                'id': 'SC_201'
            },
            'SC_822': {
                'name': '822',
                'id': 'SC_822'
            },
            'SC_13': {
                'name': '13',
                'id': 'SC_13'
            },
            'SC_12': {
                'name': '12',
                'id': 'SC_12'
            },
            'SC_37': {
                'name': '37',
                'id': 'SC_37'
            },
            'SC_10': {
                'name': '10',
                'id': 'SC_10'
            },
            'SC_31': {
                'name': '31',
                'id': 'SC_31'
            },
            'SC_16': {
                'name': '16',
                'id': 'SC_16'
            },
            'SC_14': {
                'name': '14',
                'id': 'SC_14'
            },
            'SC_71': {
                'name': '71',
                'id': 'SC_71'
            },
            'SC_70': {
                'name': '70',
                'id': 'SC_70'
            },
            'SC_73': {
                'name': '73',
                'id': 'SC_73'
            },
            'SC_72': {
                'name': '72',
                'id': 'SC_72'
            },
            'SC_900': {
                'name': '900',
                'id': 'SC_900'
            },
            'SC_901': {
                'name': '901',
                'id': 'SC_901'
            },
            'SC_77': {
                'name': '77',
                'id': 'SC_77'
            },
            'SC_831': {
                'name': '831',
                'id': 'SC_831'
            },
            'SC_18': {
                'name': '18',
                'id': 'SC_18'
            },
            'SC_51': {
                'name': '51',
                'id': 'SC_51'
            },
            'SC_39': {
                'name': '39',
                'id': 'SC_39'
            },
            'SC_19': {
                'name': '19',
                'id': 'SC_19'
            },
            'SC_57': {
                'name': '57',
                'id': 'SC_57'
            },
            'SC_122': {
                'name': '122',
                'id': 'SC_122'
            },
            'SC_522': {
                'name': '522',
                'id': 'SC_522'
            },
            'SC_81': {
                'name': '81',
                'id': 'SC_81'
            },
            'SC_82': {
                'name': '82',
                'id': 'SC_82'
            },
            'SC_200': {
                'name': '200',
                'id': 'SC_200'
            },
            'SC_88': {
                'name': '88',
                'id': 'SC_88'
            },
            'SC_89': {
                'name': '89',
                'id': 'SC_89'
            },
            'SC_40': {
                'name': '40',
                'id': 'SC_40'
            },
            'SC_42': {
                'name': '42',
                'id': 'SC_42'
            },
            'SC_121': {
                'name': '121',
                'id': 'SC_121'
            },
            'SC_54': {
                'name': '54',
                'id': 'SC_54'
            },
            'SC_45': {
                'name': '45',
                'id': 'SC_45'
            },
            'SC_46': {
                'name': '46',
                'id': 'SC_46'
            },
            'SC_47': {
                'name': '47',
                'id': 'SC_47'
            },
            'SC_48': {
                'name': '48',
                'id': 'SC_48'
            },
            'SC_49': {
                'name': '49',
                'id': 'SC_49'
            },
            'SC_330': {
                'name': '330',
                'id': 'SC_330'
            },
            'SC_26': {
                'name': '26',
                'id': 'SC_26'
            },
            'SC_27': {
                'name': '27',
                'id': 'SC_27'
            },
            'SC_68': {
                'name': '68',
                'id': 'SC_68'
            },
            'SC_25': {
                'name': '25',
                'id': 'SC_25'
            },
            'SC_22': {
                'name': '22',
                'id': 'SC_22'
            },
            'SC_23': {
                'name': '23',
                'id': 'SC_23'
            },
            'SC_61': {
                'name': '61',
                'id': 'SC_61'
            },
            'SC_62': {
                'name': '62',
                'id': 'SC_62'
            },
            'SC_63': {
                'name': '63',
                'id': 'SC_63'
            },
            'SC_60': {
                'name': '60',
                'id': 'SC_60'
            },
            'SC_58': {
                'name': '58',
                'id': 'SC_58'
            },
            'SC_66': {
                'name': '66',
                'id': 'SC_66'
            },
            'SC_64': {
                'name': '64',
                'id': 'SC_64'
            },
            'SC_65': {
                'name': '65',
                'id': 'SC_65'
            },
            'SC_35': {
                'name': '35',
                'id': 'SC_35'
            },
            'SC_168': {
                'name': '168',
                'id': 'SC_168'
            },
            'SC_828': {
                'name': '828',
                'id': 'SC_828'
            },
            'SC_827': {
                'name': '827',
                'id': 'SC_827'
            },
            'SC_826': {
                'name': '826',
                'id': 'SC_826'
            },
            'SC_825': {
                'name': '825',
                'id': 'SC_825'
            },
            'SC_824': {
                'name': '824',
                'id': 'SC_824'
            },
            'SC_823': {
                'name': '823',
                'id': 'SC_823'
            },
            'SC_181': {
                'name': '181',
                'id': 'SC_181'
            },
            'SC_182': {
                'name': '182',
                'id': 'SC_182'
            },
            'SC_104': {
                'name': '104',
                'id': 'SC_104'
            },
            'SC_970': {
                'name': '970',
                'id': 'SC_970'
            },
            'SC_101': {
                'name': '101',
                'id': 'SC_101'
            },
            'SC_102': {
                'name': '102',
                'id': 'SC_102'
            },
            'SC_103': {
                'name': '103',
                'id': 'SC_103'
            },
            'SC_17': {
                'name': '17',
                'id': 'SC_17'
            },
            'SC_34': {
                'name': '34',
                'id': 'SC_34'
            }
        },
        'SB':     {
            'SB_Ala/Oak-SSF': {
                'name': 'Ala/Oak-SSF',
                'id  ': 'SB_Ala/Oak-SSF'
            },
            'SB_4': {
                'name': 'SSF-SF',
                'id': 'SB_4'
            },
            'SB_2': {
                'name': 'HarborBay-SF',
                'id': 'SB_2'
            },
            'SB_3': {
                'name': 'Vallejo-SF',
                'id': 'SB_3'
            },
            'SB_200': {
                'name': '200',
                'id': 'SB_200'
            },
            'SB_1': {
                'name': 'Ala/Oak-SF',
                'id': 'SB_1'
            }
        },
        'SF':     {
            'SF_29': {
                'name': '29',
                'id  ': 'SF_29'
            },
            'SF_43': {
                'name': '43',
                'id': 'SF_43'
            },
            'SF_41': {
                'name': '41',
                'id': 'SF_41'
            },
            'SF_66': {
                'name': '66',
                'id': 'SF_66'
            },
            'SF_61': {
                'name': 'CALIFORNIA',
                'id': 'SF_61'
            },
            'SF_60': {
                'name': 'Powell-Hyde',
                'id': 'SF_60'
            },
            'SF_45': {
                'name': '45',
                'id': 'SF_45'
            },
            'SF_16X': {
                'name': '16X',
                'id': 'SF_16X'
            },
            'SF_21': {
                'name': '21',
                'id': 'SF_21'
            },
            'SF_23': {
                'name': '23',
                'id': 'SF_23'
            },
            'SF_22': {
                'name': '22',
                'id': 'SF_22'
            },
            'SF_71L': {
                'name': '71L',
                'id': 'SF_71L'
            },
            'SF_24': {
                'name': '24',
                'id': 'SF_24'
            },
            'SF_27': {
                'name': '27',
                'id': 'SF_27'
            },
            'SF_2': {
                'name': '2',
                'id': 'SF_2'
            },
            'SF_3': {
                'name': '3',
                'id': 'SF_3'
            },
            'SF_1AX': {
                'name': '1AX',
                'id': 'SF_1AX'
            },
            'SF_1': {
                'name': '1',
                'id': 'SF_1'
            },
            'SF_6': {
                'name': '6',
                'id': 'SF_6'
            },
            'SF_8BX': {
                'name': '8BX',
                'id': 'SF_8BX'
            },
            'SF_5': {
                'name': '5',
                'id': 'SF_5'
            },
            'SF_47': {
                'name': '47',
                'id': 'SF_47'
            },
            'SF_38BX': {
                'name': '38BX',
                'id': 'SF_38BX'
            },
            'SF_9': {
                'name': '9',
                'id': 'SF_9'
            },
            'SF_31AX': {
                'name': '31AX',
                'id': 'SF_31AX'
            },
            'SF_31': {
                'name': '31',
                'id': 'SF_31'
            },
            'SF_38AX': {
                'name': '38AX',
                'id': 'SF_38AX'
            },
            'SF_83X': {
                'name': '83X',
                'id': 'SF_83X'
            },
            'SF_31BX': {
                'name': '31BX',
                'id': 'SF_31BX'
            },
            'SF_90': {
                'name': '90',
                'id': 'SF_90'
            },
            'SF_91': {
                'name': '91',
                'id': 'SF_91'
            },
            'SF_44': {
                'name': '44',
                'id': 'SF_44'
            },
            'SF_K OWL': {
                'name': 'K-OWL',
                'id': 'SF_K OWL'
            },
            'SF_10': {
                'name': '10',
                'id': 'SF_10'
            },
            'SF_12': {
                'name': '12',
                'id': 'SF_12'
            },
            'SF_14': {
                'name': '14',
                'id': 'SF_14'
            },
            'SF_67': {
                'name': '67',
                'id': 'SF_67'
            },
            'SF_17': {
                'name': '17',
                'id': 'SF_17'
            },
            'SF_18': {
                'name': '18',
                'id': 'SF_18'
            },
            'SF_19': {
                'name': '19',
                'id': 'SF_19'
            },
            'SF_81X': {
                'name': '81X',
                'id': 'SF_81X'
            },
            'SF_L OWL': {
                'name': 'L-OWL',
                'id': 'SF_L OWL'
            },
            'SF_M OWL': {
                'name': 'M-OWL',
                'id': 'SF_M OWL'
            },
            'SF_28L': {
                'name': '28L',
                'id': 'SF_28L'
            },
            'SF_N OWL': {
                'name': 'N-OWL',
                'id': 'SF_N OWL'
            },
            'SF_39': {
                'name': '39',
                'id': 'SF_39'
            },
            'SF_14L': {
                'name': '14L',
                'id': 'SF_14L'
            },
            'SF_59': {
                'name': 'Powell-Mason',
                'id': 'SF_59'
            },
            'SF_38': {
                'name': '38',
                'id': 'SF_38'
            },
            'SF_71': {
                'name': '71',
                'id': 'SF_71'
            },
            'SF_54': {
                'name': '54',
                'id': 'SF_54'
            },
            'SF_33': {
                'name': '33',
                'id': 'SF_33'
            },
            'SF_56': {
                'name': '56',
                'id': 'SF_56'
            },
            'SF_1BX': {
                'name': '1BX',
                'id': 'SF_1BX'
            },
            'SF_36': {
                'name': '36',
                'id': 'SF_36'
            },
            'SF_37': {
                'name': '37',
                'id': 'SF_37'
            },
            'SF_52': {
                'name': '52',
                'id': 'SF_52'
            },
            'SF_14X': {
                'name': '14X',
                'id': 'SF_14X'
            },
            'SF_76X': {
                'name': '76X',
                'id': 'SF_76X'
            },
            'SF_9L': {
                'name': '9L',
                'id': 'SF_9L'
            },
            'SF_KT': {
                'name': 'KT',
                'id': 'SF_KT'
            },
            'SF_35': {
                'name': '35',
                'id': 'SF_35'
            },
            'SF_38L': {
                'name': '38L',
                'id': 'SF_38L'
            },
            'SF_28': {
                'name': '28',
                'id': 'SF_28'
            },
            'SF_108': {
                'name': '108',
                'id': 'SF_108'
            },
            'SF_8AX': {
                'name': '8AX',
                'id': 'SF_8AX'
            },
            'SF_F': {
                'name': 'F',
                'id': 'SF_F'
            },
            'SF_48': {
                'name': '48',
                'id': 'SF_48'
            },
            'SF_82X': {
                'name': '82X',
                'id': 'SF_82X'
            },
            'SF_88': {
                'name': '88',
                'id': 'SF_88'
            },
            'SF_J': {
                'name': 'J',
                'id': 'SF_J'
            },
            'SF_8X': {
                'name': '8X',
                'id': 'SF_8X'
            },
            'SF_49': {
                'name': '49',
                'id': 'SF_49'
            },
            'SF_N': {
                'name': 'N',
                'id': 'SF_N'
            },
            'SF_L': {
                'name': 'L',
                'id': 'SF_L'
            },
            'SF_M': {
                'name': 'M',
                'id': 'SF_M'
            },
            'SF_S': {
                'name': 'S',
                'id': 'SF_S'
            },
            'SF_30X': {
                'name': '30X',
                'id': 'SF_30X'
            },
            'SF_T OWL': {
                'name': 'T-OWL',
                'id': 'SF_T OWL'
            },
            'SF_5L': {
                'name': '5L',
                'id': 'SF_5L'
            },
            'SF_30': {
                'name': '30',
                'id': 'SF_30'
            },
            'SF_NX': {
                'name': 'NX',
                'id': 'SF_NX'
            }
        },
        'UC':     {
            'UC_5': {
                'name': '5',
                'id  ': 'UC_5'
            },
            'UC_4': {
                'name': '4',
                'id': 'UC_4'
            },
            'UC_7': {
                'name': '7',
                'id': 'UC_7'
            },
            'UC_6': {
                'name': '6',
                'id': 'UC_6'
            },
            'UC_1': {
                'name': '1',
                'id': 'UC_1'
            },
            'UC_3': {
                'name': '3',
                'id': 'UC_3'
            },
            'UC_2': {
                'name': '2',
                'id': 'UC_2'
            },
            'UC_9': {
                'name': '9',
                'id': 'UC_9'
            },
            'UC_8': {
                'name': '8',
                'id': 'UC_8'
            }
        }
    }
    return output
