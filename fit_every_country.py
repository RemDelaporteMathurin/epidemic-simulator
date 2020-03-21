import fit_any_country
from data import fetch_data, get_data

if __name__ == "__main__":
    data = fetch_data()
    for country in data.keys():

        time, time_number_days, cases_ref, deaths_ref = get_data(country)
        if len(time) > 10:
            time_sim, cases_sim, healthy_sim, recovered_sim, deaths_sim = \
                fit_country(country, save_to_json=True)

