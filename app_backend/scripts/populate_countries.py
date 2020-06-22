from app_backend.helpers.saltedge_client import initiate_saltedge_client
from app_backend.helpers.saltedge_urls import COUNTRIES_INFO_URL
from app_backend.models.country import Country


def populate_countries():
    saltedge_client = initiate_saltedge_client()
    response = saltedge_client.get(COUNTRIES_INFO_URL)
    countries_list = response.json()['data']
    for country in countries_list:
        new_country = Country(country_name=country['name'], se_country_code=country['code'])
        new_country.save()


if __name__ == "__main__":
    populate_countries()