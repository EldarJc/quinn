import { defineStore } from 'pinia';
import EventService from '@/api/event';

const eventService = new EventService();

export const useEventStore = defineStore('events', {
    state: () => ({
        events: [],
        loading: false,
        error: null,
        hasMore: true,
        page: 1,
        filters: {
            search: '',
            country: '',
            state: '',
            city: '',
            tags: [],
            sort: 'date_asc',
            event_type: ''
        }
    }),

    actions: {
        async fetchEvents(loadMore = false) {
            if (this.loading) return;
            this.loading = true;
            this.error = null;

            try {
                if (!loadMore) {
                    this.page = 1;
                    this.events = [];
                }

                const params = new URLSearchParams();
                params.append('page', this.page);

                Object.entries(this.filters).forEach(([key, value]) => {
                    if (value !== '' && value !== null && value !== undefined) {
                        if (Array.isArray(value)) {
                            value.forEach(v => params.append(key, v));
                        } else {
                            params.append(key, value);
                        }
                    }
                });

                const response = await eventService.getEvents(params);

                const fetchedEvents = response.data.items || response.data || [];

                if (loadMore) {
                    this.events.push(...fetchedEvents);
                } else {
                    this.events = fetchedEvents;
                }

                const paginationHeader = response.headers['x-pagination'];
                if (paginationHeader) {
                    const paginationData = JSON.parse(paginationHeader);
                    this.hasMore = this.page < paginationData.total_pages;
                } else {
                    this.hasMore = fetchedEvents.length === 20;
                }

            } catch (err) {
                this.error = err.message || 'Failed to load events';
            } finally {
                this.loading = false;
            }
        },

        loadNextPage() {
            if (this.hasMore && !this.loading) {
                this.page++;
                this.fetchEvents(true);
            }
        },

        resetFilters() {
            this.filters = {
                search: '',
                country: '',
                state: '',
                city: '',
                tags: [],
                sort: 'date_asc',
                event_type: ''
            };
            this.fetchEvents(false);
        },

        setSearch(val) {
            this.filters.search = val;
            this.fetchEvents(false);
        }
    }
});