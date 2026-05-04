import apiClient from '@/api/apiClient';

class LocationService {
    getCountries() {
        return apiClient.get('/locations/countries');
    }

    getStates(iso3) {
        return apiClient.get(`/locations/countries/${iso3}/states`);
    }

    getCitiesByCountry(country) {
        return apiClient.get(`/locations/countries/${country}/cities`);
    }

    getCitiesByState(country, state) {
        return apiClient.get(`/locations/countries/${country}/${state}/cities`);
    }
}

export default LocationService;