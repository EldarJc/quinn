import { defineStore } from 'pinia';
import LocationService from '@/api/location';

const locationService = new LocationService();

export const useLocationStore = defineStore('location', {
    state: () => ({
        countries: [],
        states: [],
        cities: []
    }),

    actions: {
        async fetchCountries() {
            if (this.countries.length > 0) return;
            try {
                const response = await locationService.getCountries();
                this.countries = response.data.data || response.data || [];
            } catch (error) {}
        },

        async fetchStates(countryIso) {
            this.states = [];
            try {
                const response = await locationService.getStates(countryIso);
                this.states = response.data.data || response.data || [];
            } catch (error) {}
        },

        async fetchCitiesByCountry(countryName) {
            this.cities = [];
            try {
                const response = await locationService.getCitiesByCountry(countryName);
                this.cities = response.data.data || response.data || [];
            } catch (error) {}
        },

        async fetchCitiesByState(countryName, stateName) {
            this.cities = [];
            try {
                const response = await locationService.getCitiesByState(countryName, stateName);
                this.cities = response.data.data || response.data || [];
            } catch (error) {}
        },

        clearData() {
            this.states = [];
            this.cities = [];
        }
    }
});