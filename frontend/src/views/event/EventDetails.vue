<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import EventService from '@/api/event.js';
import ErrorMessage from "@/components/ErrorMessage.vue";

const route = useRoute();
const eventService = new EventService();

const event = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const eventId = route.params.id;
    const eventSlug = route.params.slug;
    const response = await eventService.getEvent(eventId, eventSlug);
    event.value = response.data;
  } catch (err) {
    error.value = err.message || err;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="py-12 font-sans">
    <ErrorMessage
        :show="error !== null"
        :errorMessage="error"
        @update:show="error = null"
    />
    <div class="w-7xl px-8">
      <div v-if="loading" class="grid grid-cols-12 gap-10 animate-pulse">
        <div class="col-span-8 space-y-6">
          <div class="h-8 bg-[#dce6f0] rounded-full w-32"></div>
          <div class="h-16 bg-[#dce6f0] rounded-2xl w-3/4"></div>
          <div class="h-100 bg-[#dce6f0] rounded-4xl w-full"></div>
        </div>
        <div class="col-span-4">
          <div class="h-125 bg-[#dce6f0] rounded-4xl w-full"></div>
        </div>
      </div>
      <div v-else-if="event" class="grid grid-cols-12 gap-10 animate-fade-in">
        <div class="col-span-8 flex flex-col">
          <div class="mb-8">
            <div class="flex flex-wrap gap-3 mb-5">
                     <span
                         v-for="(tag, id) in event.tags"
                         :key="id"
                         class="px-3 py-1.5 text-xs font-bold uppercase tracking-wider text-[#2c3e50] bg-[#dce6f0] rounded-full"
                     >
                     {{ tag.name || tag }}
                     </span>
            </div>
            <h1 class="text-4xl font-black text-[#2c3e50] leading-tight tracking-tight">
              {{ event.title }}
            </h1>
          </div>
          <div v-if="event.image_path" class="w-full aspect-video rounded-4xl overflow-hidden mb-12 shadow-lg shadow-slate-200/50 border border-white bg-white">
            <img
                :src="event.image_path"
                class="w-full h-full object-cover"
                alt="Event Image"
            />
          </div>
          <div class="mb-12">
            <h2 class="text-2xl font-bold mb-6 text-[#2c3e50] flex items-center gap-3">
              <span class="w-2 h-8 bg-[#2c3e50] rounded-full block"></span>
              About the event
            </h2>
            <div class="prose prose-lg max-w-none text-slate-600 leading-relaxed whitespace-pre-line">
              {{ event.description }}
            </div>
          </div>
          <div v-if="event.location" class="bg-white p-6 rounded-4xl border border-slate-100 shadow-md shadow-slate-200/50 flex items-center gap-6">
            <div class="w-16 h-16 bg-[#EAF2FA] rounded-2xl flex items-center justify-center text-[#2c3e50] shrink-0">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-1">Location</h3>
              <p class="text-xl font-bold text-[#2c3e50]">
                {{ event.location.address || event.location.name }}
              </p>
              <p class="text-slate-500 font-medium mt-1">
                {{ event.location.city }}, {{ event.location.country }}
              </p>
            </div>
          </div>
        </div>
        <div class="col-span-4">
          <div class="bg-white border border-slate-100 rounded-4xl p-8 sticky top-8 shadow-xl shadow-slate-200/40">
            <h3 class="text-xl font-bold mb-8 text-[#2c3e50]">Event Details</h3>
            <ul class="space-y-6">
              <li class="flex items-center gap-4">
                <div class="w-9 h-9 rounded-2xl bg-[#EAF2FA] flex items-center justify-center text-[#2c3e50] shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                  </svg>
                </div>
                <div>
                  <span class="block text-xs font-bold text-slate-400 uppercase tracking-wide">Type</span>
                  <span class="block text-md font-semibold text-[#2c3e50] mt-0.5">{{ event.event_type }}</span>
                </div>
              </li>
              <li class="w-full h-px bg-slate-100"></li>
              <li class="flex items-center gap-4">
                <div class="w-9 h-9 rounded-2xl bg-[#EAF2FA] flex items-center justify-center text-[#2c3e50] shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <span class="block text-xs font-bold text-slate-400 uppercase tracking-wide">Starts</span>
                  <span class="block text-md font-semibold text-[#2c3e50] mt-0.5">{{ event.start_date }}</span>
                </div>
              </li>
              <li class="flex items-center gap-4">
                <div class="w-9 h-9 rounded-2xl bg-[#EAF2FA] flex items-center justify-center text-[#2c3e50] shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div>
                  <span class="block text-xs font-bold text-slate-400 uppercase tracking-wide">Ends</span>
                  <span class="block text-md font-semibold text-[#2c3e50] mt-0.5">{{ event.end_date }}</span>
                </div>
              </li>
              <li class="w-full h-px bg-slate-100"></li>
              <li v-if="event.max_attendees" class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-2xl bg-[#EAF2FA] flex items-center justify-center text-[#2c3e50] shrink-0">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
                  </svg>
                </div>
                <div>
                  <span class="block text-xs font-bold text-slate-400 uppercase tracking-wide">Max attendees</span>
                  <span class="block text-lg font-semibold text-[#2c3e50] mt-0.5">{{ event.max_attendees }} people</span>
                </div>
              </li>
            </ul>
            <div class="mt-10">
              <button class="w-full px-6 py-4 text-lg font-bold text-white bg-[#2c3e50] rounded-2xl hover:bg-gray-500 transition-all active:scale-[0.98] shadow-md shadow-[#2c3e50]/20 hover:shadow-xl hover:shadow-[#2c3e50]/30">
                Join Event
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>