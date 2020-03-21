import json
import urllib
import requests
from datetime import datetime
from datetime import timedelta


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def fetch_data():
    url = "https://pomber.github.io/covid19/timeseries.json"
    try:
        data = json.loads(requests.get(url).text)
    except requests.ConnectionError:
        print('No internet ?')
        with open('data/timeseries.json', 'r') as f:
            data = json.load(f)
    return data


def get_data(country):
    time, cases, deaths = [], [], []
    data = fetch_data()
    for entry in data[country]:
        if float(entry["confirmed"]) > 50:
            time.append(entry["date"])
            cases.append(float(entry["confirmed"]) - float(entry["recovered"]))
            deaths.append(float(entry["deaths"]))
    time_number_days = []
    for t in time:
        time_number_days.append(days_between(t, time[0]))
    return time, time_number_days, cases, deaths


def save_data(country, time, time_sim, cases_sim, deaths_sim):
    export = {country: []}
    for i in range(len(time_sim)):
        time_sim_date = datetime.strptime(time[0], "%Y-%m-%d") + \
            timedelta(days=time_sim[i])
        a = {
            "date": time_sim_date.strftime("%Y-%m-%d"),
            "cases_sim": cases_sim[i],
            "deaths_sim": deaths_sim[i]
        }
        export[country].append(a)
    with open("data/" + time[-1] + ".json", 'r') as f:
        data = json.load(f)
    data.update(export)
    with open("data/" + time[-1] + ".json", 'w+') as f:
        json.dump(data, f, indent=4)
    return 0
