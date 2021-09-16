from flask import Flask, jsonify, request
from crudService import CrudService
app = Flask(__name__)

@app.route("/itsbritneyb")
def getData():

    headers = {'Authorization': request.headers.get('Authorization')}

    Service = CrudService(headers)

    # https://api-ssl.bitly.com/v4/user
    user = Service.getUser()
    
    # grab group guid and name
    group_guid = user['default_group_guid']
    name = user['name']

    # https://api-ssl.bitly.com/v4/groups/{group_guid}/bitlinks
    bitlinks = Service.getLinks(group_guid)
    
    # grab dict of all links data
    links = bitlinks['links']  

    countries = {} # Eventually return this dictionary holding {<country>: <average daily clicks over past month>}

    # loop over all bitlinks
    for i in range(len(links)):

        # grab bitlink
        bitlink = links[i]['id']
        
        # https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/countries
        unit, units = 'month', '30'
        clicks = Service.getClicksByCountry(bitlink, unit, units)

        metrics = clicks['metrics']
        
        # if country is already in dict, add to total count, otherwise, add new country to dict with click data
        for i in range(len(metrics)):
            clicks = metrics[i]['clicks']
            country = metrics[i]['value']
            if country in countries:
                countries[country] += clicks
            else:
                countries[country] = clicks
    
    # divide each click by 30 => "average daily clicks"
    for key, value in countries.items():
        countries[key] = float(f'{(value/30):.5f}')

    return jsonify({f'{name}\'s average daily clicks per country over the past month': countries})
    

if __name__=='__main__':
    app.run(port=5000, debug=True)