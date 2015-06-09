import model


Systems_short_to_long = {'3D': 'Tridelta Transit',
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
                         'EM': 'Emerygoround',
                         'FS': 'FAST Transit',
                         'GF': 'Golden Gate Ferry',
                         'GG': 'Golden Gate Transit',
                         'HF': 'Alcatraz Cruises',
                         'MA': 'Marin Transit',
                         'MS': 'Marguerite Shuttle (Stanford)',
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
                         'YV': 'Yountville Trolley (Vine Transit)'
                         }


def agency_routes_dict():
    output = {}
    agencies = model.get_all_agencies()
    for agency in agencies:
        agency_id = agency.agency_id
        output[agency_id] = {}
        routes = model.get_agency_routes(agency_id)
        route_dict = output[agency_id]
        for route in routes:
            route_id = route.route_id
            route_dict[route_id] = {}
            route_info = route_dict[route_id]
            route_info['name'] = route.route_long_name
            route_info['id'] = route.route_id
    print output

agency_routes_dict()
