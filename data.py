import json
import urllib
import requests
from datetime import datetime


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def get_data(country):
    time, cases, deaths = [], [], []
    url = "https://pomber.github.io/covid19/timeseries.json"
    try:
        data = json.loads(requests.get(url).text)
    except requests.ConnectionError:
        print('No internet ?')
        with open('data/timeseries.json', 'r') as f:
            data = json.load(f)
    for entry in data[country]:
        if float(entry["confirmed"]) > 50:
            time.append(entry["date"])
            cases.append(float(entry["confirmed"]) - float(entry["recovered"]))
            deaths.append(float(entry["deaths"]))
    time_number_days = []
    for t in time:
        time_number_days.append(days_between(t, time[0]))
    return time, time_number_days, cases, deaths
