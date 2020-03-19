import json
import urllib
import requests


def get_data(country):
    time, cases, deaths = [], [], []
    url = "https://pomber.github.io/covid19/timeseries.json"
    try:
        data = json.loads(requests.get(url).text)
    except:
        print('No internet ?')
        with open('data/timeseries.json', 'r') as f:
            data = json.load(f)
    for entry in data[country]:
        if float(entry["confirmed"]) > 50:
            time.append(entry["date"])
            cases.append(float(entry["confirmed"]) - float(entry["recovered"]))
            deaths.append(float(entry["deaths"]))
    return time, cases, deaths
