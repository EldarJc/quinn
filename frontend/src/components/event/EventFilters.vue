<script setup>
import { onMounted, ref } from 'vue';
import { useLocationStore } from '@/stores/location';
import TagService from '@/api/tag';

const props = defineProps({
  filters: { type: Object, required: true }
});

const eventTypes = [
  { value: "ONLINE", label: "Online" },
  { value: "MEETUP", label: "Meetup" },
  { value: "WORKSHOP", label: "Workshop" },
  { value: "CONFERENCE", label: "Conference" },
  { value: "WEBINAR", label: "Webinar" },
  { value: "TRIP", label: "Trip" }
];

const emit = defineEmits(['reset', 'filter-changed']);

const locationStore = useLocationStore();
const tagService = new TagService();

const availableTags = ref([]);
const loadingTags = ref(false);

const currentTagPage = ref(1);
const hasMoreTags = ref(true);

const fetchTags = async () => {
  if (loadingTags.value || !hasMoreTags.value) return;

  loadingTags.value = true;
  try {
    const res = await tagService.getTags(currentTagPage.value);
    const fetchedTags = res.data?.items || res.data || [];

    if (fetchedTags.length > 0) {
      const newTags = [...availableTags.value, ...fetchedTags];
      availableTags.value = Array.from(new Map(newTags.map(item => [item.id, item])).values());
      currentTagPage.value++;
    } else {
      hasMoreTags.value = false;
    }

    if (fetchedTags.length < 50) {
      hasMoreTags.value = false;
    }
  } catch (e) {
  } finally {
    loadingTags.value = false;
  }
};

const onTagScroll = (e) => {
  const { scrollTop, scrollHeight, clientHeight } = e.target;
  if (scrollHeight - scrollTop - clientHeight < 20) {
    fetchTags();
  }
};

onMounted(async () => {
  await locationStore.fetchCountries();
  await fetchTags();
});

const onCountryChange = async () => {
  props.filters.state = '';
  props.filters.city = '';
  locationStore.clearData();

  if (props.filters.country) {
    const country = locationStore.countries.find(c => c.name === props.filters.country);
    if (country) {
      await locationStore.fetchStates(country.Iso3);
      if (locationStore.states.length === 0) {
        await locationStore.fetchCitiesByCountry(props.filters.country);
      }
    }
  }

  emit('filter-changed');
};

const onStateChange = async () => {
  props.filters.city = '';
  if (props.filters.country && props.filters.state) {
    await locationStore.fetchCitiesByState(props.filters.country, props.filters.state);
  }

  emit('filter-changed');
};

const toggleTag = (tagId) => {
  const index = props.filters.tags.indexOf(tagId);
  if (index === -1) {
    props.filters.tags.push(tagId);
  } else {
    props.filters.tags.splice(index, 1);
  }

  emit('filter-changed');
};
</script>

<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-semibold text-gray-900">Filters</h2>
      <button
          @click="$emit('reset')"
          class="text-sm text-teal-600 hover:text-teal-800 font-medium transition"
      >
        Clear all
      </button>
    </div>
    <div class="space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
        <select
            v-model="filters.sort"
            @change="$emit('filter-changed')"
            class="w-full rounded-lg border-gray-300 text-gray-700 focus:border-teal-500 focus:ring-teal-500 bg-gray-50 p-2"
        >
          <option value="date_asc">Upcoming First</option>
          <option value="date_desc">Latest Dates</option>
          <option value="newest">Newest Created</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Event Type</label>
        <select
            v-model="filters.event_type"
            @change="$emit('filter-changed')"
            class="w-full rounded-lg border-gray-300 text-gray-700 focus:border-teal-500 focus:ring-teal-500 bg-gray-50 p-2"
        >
          <option value="" disabled selected>Select type</option>
          <option v-for="type in eventTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Country</label>
        <select
            v-model="filters.country"
            @change="onCountryChange"
            class="w-full rounded-lg border-gray-300 text-gray-700 focus:border-teal-500 focus:ring-teal-500 bg-gray-50 p-2"
        >
          <option value="">Anywhere</option>
          <option v-for="c in locationStore.countries" :key="c.Iso3" :value="c.name">
            {{ c.name }}
          </option>
        </select>
      </div>
      <div v-if="filters.country && locationStore.states.length">
        <label class="block text-sm font-medium text-gray-700 mb-2">State/Region</label>
        <select
            v-model="filters.state"
            @change="onStateChange"
            class="w-full rounded-lg border-gray-300 text-gray-700 focus:border-teal-500 focus:ring-teal-500 bg-gray-50"
        >
          <option value="">All States</option>
          <option v-for="s in locationStore.states" :key="s.state_code" :value="s.name">
            {{ s.name }}
          </option>
        </select>
      </div>
      <div v-if="filters.country && locationStore.cities.length">
        <label class="block text-sm font-medium text-gray-700 mb-2">City</label>
        <select
            v-model="filters.city"
            @change="$emit('filter-changed')"
            class="w-full rounded-lg border-gray-300 text-gray-700 focus:border-teal-500 focus:ring-teal-500 bg-gray-50"
        >
          <option value="">All Cities</option>
          <option v-for="city in locationStore.cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Tags</label>
        <div
            class="flex flex-wrap gap-2 max-h-60 overflow-y-auto pr-1"
            @scroll="onTagScroll"
        >
          <button
              v-for="tag in availableTags"
              :key="tag.id"
              @click="toggleTag(tag.id)"
              :class="[
                  'px-3 py-1.5 rounded-full text-xs font-medium transition-colors border',
                  filters.tags.includes(tag.id)
                  ? 'bg-teal-50 text-teal-700 border-teal-200'
                  : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'
                  ]"
          >
            {{ tag.name }}
          </button>
          <div v-if="loadingTags" class="w-full text-center text-sm text-gray-500 italic py-2">
            Loading tags...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>