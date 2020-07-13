import requests
import traceback

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


def populate_countries_fields():
    countries = Country.objects.all()
    countries_api_response = requests.get("https://restcountries.eu/rest/v2/all").json()
    for country in countries:
        try:
            country_api_item = [
                country_item for country_item in countries_api_response
                if country.country_name.lower() in country_item['name'].lower()
            ][0]
            country.currency_symbol = country_api_item['currencies'][0]['symbol']
            country.isd_code = country_api_item['callingCodes'][0]
            country.currency_name = country_api_item['currencies'][0]['name']
            country.currency_code = country_api_item['currencies'][0]['code']
            country.country_flag_icon_url = "https://www.countryflags.io/" + country.se_country_code.lower() + "/shiny/64.png"
            country.save()
            print("Success: Country: " + str(country.country_name) + " : " + str(country.currency_code))
        except:
            print(traceback.format_exc())


if __name__ == "__main__":
    # populate_countries()
    populate_countries_fields()