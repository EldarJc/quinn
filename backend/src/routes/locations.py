import logging
from typing import Any

import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..extensions import cache
from ..schemas.location_schema import (
    CitiesSchema,
    CountriesSchema,
    StatesSchema,
)

logger = logging.getLogger(__name__)
api = "https://countriesnow.space/api/v0.1"
cache_exp = 0


@cache.cached(timeout=cache_exp, key_prefix="all_countries")
def get_countries() -> list[dict[Any, Any]]:
    try:
        response = requests.get(f"{api}/countries/iso")
        response.raise_for_status()
        result = response.json()

        if result.get("error"):
            logger.error(f"Failed to fetch countries: {result.get('error')}")
            abort(502, message="External API returned an error")

        countries = result.get("data", [])
        return countries

    except requests.RequestException as e:
        logger.error(f"Failed to fetch countries: {e}")
        abort(502, message="Unable to fetch countries from external API")


@cache.cached(timeout=cache_exp, key_prefix="all_cities")
def get_all_cities() -> dict[str, list[str]]:
    try:
        response = requests.get(f"{api}/countries")
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            logger.error(f"Failed to fetch cities: {result.get('error')}")
            abort(502, message="External API returned an error")

        cities = {ci.get("country"): ci.get("cities") for ci in result.get("data", [])}
        return cities

    except requests.RequestException as e:
        logger.error(f"Failed to fetch cities: {e}")
        abort(502, message="Unable to fetch cities from external API")


@cache.cached(timeout=cache_exp, key_prefix="all_states")
def get_states() -> dict[str, dict[str, str]]:
    try:
        response = requests.get(f"{api}/countries/states")
        response.raise_for_status()
        result = response.json()

        if result.get("error"):
            logger.error(f"Failed to fetch states: {result.get('error')}")
            abort(502, message="External API returned an error")

        states = {
            data.get("iso3"): {
                s.get("state_code"): s.get("name") for s in data.get("states", [])
            }
            for data in result.get("data", [])
        }
        return states

    except requests.RequestException as e:
        logger.error(f"Failed to fetch states: {e}")
        abort(502, message="Unable to fetch states from external API")


@cache.memoize(timeout=cache_exp)
def get_cities_by_state(country: str, state: str) -> dict[str, Any] | Any:
    try:
        response = requests.post(
            f"{api}/countries/state/cities",
            json={"country": country, "state": state},
        )
        response.raise_for_status()
        cities_result = response.json()

        if cities_result.get("error"):
            abort(404, message=f"No cities found for state '{state}' in '{country}'")

        return cities_result

    except requests.RequestException as e:
        logger.error(f"Failed to fetch cities for {state}, {country}: {e}")
        abort(502, message="Unable to fetch cities from external API")


def get_cities_by_country(country: str) -> list[str]:
    cities = get_all_cities()
    country_cities = cities.get(country, None)

    if not country_cities:
        abort(404, message=f"No cities found for {country} country")

    return country_cities


def get_country_states(iso3: str) -> list[dict[str, str]]:
    states = get_states()

    country_states = states.get(iso3, None)

    if not country_states:
        abort(404, message=f"No states found for {iso3}")

    return [{"state_code": code, "name": name} for code, name in country_states.items()]


bp = Blueprint("Location", __name__)


@bp.route("/countries")
class Countries(MethodView):
    @bp.response(200, CountriesSchema())
    def get(self):
        countries = get_countries()
        return {"data": countries}


@bp.route("/countries/<string:iso>/states")
class States(MethodView):
    @bp.response(200, StatesSchema())
    def get(self, iso):
        states = get_country_states(iso)
        return {"data": states}


@bp.route("/countries/<string:country>/cities")
class CountryCities(MethodView):
    @bp.response(200, CitiesSchema())
    def get(self, country):
        cities = get_cities_by_country(country)
        return {"data": cities}


@bp.route("/countries/<string:country>/<string:state>/cities")
class StateCities(MethodView):
    @bp.response(200, CitiesSchema())
    def get(self, country, state):
        cities = get_cities_by_state(country, state)
        return cities
