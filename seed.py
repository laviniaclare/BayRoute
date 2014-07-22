import model
import csv
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from alembic import op
import sqlalchemy.dialects.postgresql.json as json


Systems_short_to_long={
'3D':'Tridelta Transit',
'AB':'AirBART',
'AC':'AC Transit',
'AM':'Capitol Corridor',
'AT':'Angel Island Ferry',
'AY':'American Canyon Transit (Vine Transit)',
'BA':'BART',
'BG':'Blue and Gold Fleet',
'CC':'County Connection',
'CE':'Ace Rail',
'CT':'CalTrain',
'DE':'Dumbarton Express',
'EM':'Emerygoround',
'FS':'FAST Transit',
'GF':'Golden Gate Ferry',
'GG':'Golden Gate Transit',
'HF':'Alcatraz Cruises',
'MA':'Marin Transit',
'MS':'Marguerite Shuttle (Stanford)',
'PE':'Petaluma Transit',
'RV':'Delta Breeze Transit (Rio Vista City)',
'SB':'San Francisco Bay Ferry',
'SC':'Vally Transportation Authority',
'SF':'SFMTA (Muni)',
'SM':'SamTrans',
'SO':'Sonoma County Transit',
'SR':'CityBus (Santa Rosa)',
'ST':'Soltrans',
'UC':'Union City Transit',
'VC':'City Coach',
'VN':'The Vine',
'WC':'WestCat',
'WH':'Wheels Bus',
'YV':'Yountville Trolley (Vine Transit)'
}

# def fix_lingnames():
# 	names=model.session.query(model.Agency).all()
# 	for route_name in gtfs_agency:
# 		if name in Systems_shortname_to_longname:
# 			name=Systems_shortname_to_longname[name]



