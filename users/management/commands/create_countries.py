from django.core.management.base import BaseCommand
from projects.models import Country, State
import json


class Command(BaseCommand):
    help = 'Create Countries with States'

    def handle(self, *args, **kwargs):
        info = open('json/countries_states_cities.json', encoding='utf-8')
        countries = json.loads(info.read())
        for country in countries:
            country_obj, created = Country.objects.get_or_create(
                pk=country['id'], name=country['name'])
            country_obj.phone_code = country['phone_code']
            country_obj.currency = country['currency']
            country_obj.capital = country['capital']
            country_obj.iso3 = country['iso3']
            country_obj.iso2 = country['iso2']
            country_obj.region = country['region']
            country_obj.subregion = country['subregion']
            country_obj.latitude = country['latitude']
            country_obj.longitude = country['longitude']
            country_obj.save()
            for state in country['states']:
                state_obj, created = State.objects.get_or_create(
                    pk=state['id'])
                state_obj.name = state['name']
                state_obj.state_code = state['state_code']
                state_obj.latitude = state['latitude']
                state_obj.longitude = state['longitude']
                state_obj.country = country_obj
                state_obj.save()
                # for city in state['cities']:
                #     city_obj, created = City.objects.get_or_create(
                #         pk=city['id'])
                #     city_obj.name = city['name']
                #     city_obj.latitude = city['latitude']
                #     city_obj.longitude = city['longitude']
                #     city_obj.state = state_obj
                #     city_obj.save()
