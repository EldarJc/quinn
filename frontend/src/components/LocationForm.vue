<script setup>
import { onMounted } from 'vue';
import { Field, useField } from "vee-validate";
import { useLocationStore } from '@/stores/location';

const locationStore = useLocationStore();
const { value: selectedCountry } = useField('location.country');

onMounted(async () => {
  await locationStore.fetchCountries();
});

const countryUpdate = async (event) => {
  const countryName = event.target.value;
  locationStore.clearData();

  if (!countryName) return;

  const countryObj = locationStore.countries.find(c => c.name === countryName);
  if (!countryObj) return;

  await locationStore.fetchStates(countryObj.Iso3);

  if (locationStore.states.length === 0) {
    await locationStore.fetchCitiesByCountry(countryObj.name);
  }
};

const stateUpdate = async (event) => {
  const stateName = event.target.value;

  locationStore.cities = [];

  if (!stateName || !selectedCountry.value) return;

  await locationStore.fetchCitiesByState(selectedCountry.value, stateName);
};
</script>

<template>
  <div class="space-y-6">
    <h2 class="text-xl font-semibold text-slate-800 flex items-center gap-2">
      <span class="w-8 h-8 rounded-lg bg-[#608a89]/10 text-[#608a89] flex items-center justify-center text-sm">📍</span>
      Location Details
    </h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">Country</label>
        <Field name="location.country" as="select" @change="countryUpdate" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200">
          <option value="" disabled>Select country</option>
          <option v-for="country in locationStore.countries" :key="country.Iso3" :value="country.name">
            {{ country.name }}
          </option>
        </Field>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">State / Region</label>
        <Field name="location.state" as="select" @change="stateUpdate" :disabled="!selectedCountry || locationStore.states.length === 0" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 disabled:opacity-60 disabled:bg-slate-100 disabled:cursor-not-allowed transition-all duration-200">
          <option value="">Select state</option>
          <option v-for="state in locationStore.states" :key="state.state_code" :value="state.name">
            {{ state.name }}
          </option>
        </Field>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">City</label>
        <Field name="location.city" as="select" :disabled="!selectedCountry || locationStore.cities.length === 0" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 disabled:opacity-60 disabled:bg-slate-100 disabled:cursor-not-allowed transition-all duration-200">
          <option value="">Select city</option>
          <option v-for="city in locationStore.cities" :key="city" :value="city">
            {{ city }}
          </option>
        </Field>
      </div>
      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">Street Address</label>
        <Field name="location.address" type="text" required placeholder="e.g. 123 Main St" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200" />
      </div>
    </div>
  </div>
</template>