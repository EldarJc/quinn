<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useEventStore } from '@/stores/event';

import HeroSearch from '@/components/HeroSearch.vue';
import EventFilters from '@/components/event/EventFilters.vue';
import EventCard from '@/components/event/EventCard.vue';
import CardSkeleton from '@/components/CardSkeleton.vue';
import NoResults from '@/components/NoResults.vue';

const eventStore = useEventStore();
const { events, loading, error, filters, hasMore } = storeToRefs(eventStore);
const { fetchEvents, loadNextPage, resetFilters, setSearch } = eventStore;

const searchInput = ref(filters.value.search);
const loadMoreSentinel = ref(null);
let observer = null;

watch(searchInput, (newVal, oldVal, onCleanup) => {
  const timer = setTimeout(() => {
    setSearch(newVal);
  }, 500);

  onCleanup(() => {
    clearTimeout(timer);
  });
});

onMounted(() => {
  if (events.value.length === 0) {
    fetchEvents(false);
  }

  observer = new IntersectionObserver((entries) => {
    const target = entries[0];
    if (target.isIntersecting && hasMore.value && !loading.value) {
      loadNextPage();
    }
  }, {
    root: null,
    rootMargin: '100px',
    threshold: 0.1
  });

  watch(loadMoreSentinel, (newVal) => {
    if (newVal) observer.observe(newVal);
  }, { flush: 'post' });
});

onUnmounted(() => {
  if (observer) observer.disconnect();
});
</script>

<template>
  <div class="pb-12">
    <HeroSearch
        v-model="searchInput"
        title="Discover Your Next Experience"
        description="From local meetups to global conferences, find events that match your passions."
        placeholder="Search for events, workshops, meetups..."
    />
    <div class="w-7xl px-8 mt-12">
      <div class="flex gap-8">
        <aside class="w-1/4 shrink-0 max-w-xs">
          <div class="sticky top-24">
            <EventFilters
                :filters="filters"
                @reset="resetFilters"
                @filter-changed="fetchEvents(false)"
            />
          </div>
        </aside>
        <main class="grow">
          <div v-if="error" class="text-red-700 p-4 mb-6 text-center">
            {{ error }}
          </div>
          <div v-if="loading && events.length === 0" class="grid grid-cols-3 gap-6">
            <CardSkeleton v-for="i in 9" :key="i" />
          </div>
          <div v-else-if="events.length > 0">
            <div class="grid grid-cols-3 gap-6">
              <EventCard v-for="event in events" :key="event.id" :event="event" />
            </div>
            <div ref="loadMoreSentinel" class="h-20 w-full flex items-center justify-center mt-8">
              <svg v-if="loading" class="animate-spin h-8 w-8 text-teal-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          </div>
          <NoResults v-else @reset="resetFilters" />
        </main>
      </div>
    </div>
  </div>
</template>