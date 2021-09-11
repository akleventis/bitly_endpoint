from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/itsbritneyb/<auth_token>")
def hello(auth_token):
    headers = {
        'Authorization': f'Bearer {auth_token}',
    }

    # get group guid
    try:
        response = requests.get('https://api-ssl.bitly.com/v4/user', headers=headers)
    except requests.exceptions.RequestException as e:
        raise(SystemExit(e))

    group_guid = response.json()['default_group_guid']

    # grab name for a steezy http response
    name = response.json()['name']

    # get list of links
    try:
        response = requests.get(f'https://api-ssl.bitly.com/v4/groups/{group_guid}/bitlinks', headers=headers)
    except requests.exceptions.RequestException as e:
        raise(SystemExit(e))

    links = response.json()['links']    

    countries = {} # Eventually return this dictionary holding {<country>: <average daily clicks over past month>}

    # loop over all bitlinks
    for i in range(len(links)):

        # grab bitlink
        bitlink = links[i]['id']

        # request for clicks over past 30 days
        try:
            response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/countries?day=month&units=30', headers=headers)
        except requests.exceptions.RequestException as e:
            raise(SystemExit(e))

        data = response.json()

        metrics = data['metrics']
        
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