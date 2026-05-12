<script setup>
const props = defineProps({
  event: { type: Object, required: true }
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const [datePart, timePart] = dateString.split(' ');
  const [day, month, year] = datePart.split('-');
  const date = new Date(`${year}-${month}-${day}T${timePart}`);

  return new Intl.DateTimeFormat('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  }).format(date);
};

const formatLocation = (loc) => {
  if (!loc) return 'Online Event';
  const parts = [loc.city, loc.country].filter(Boolean);
  return parts.join(', ') || 'Online Event';
};
</script>

<template>
  <RouterLink :to="{name:'event-details',params: {id: event.id, slug: event.slug}
      }"  class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300 border border-gray-200 flex flex-col h-full group">
    <div class="relative h-48 w-full overflow-hidden bg-gray-100">
      <img
          :src="event.image_path"
          :alt="event.title"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <div class="absolute top-4 left-4">
            <span class="px-3 py-1 bg-white/95 text-teal-700 text-xs font-bold rounded-md uppercase tracking-wider shadow-sm">
            {{ event.event_type }}
            </span>
      </div>
    </div>
    <div class="p-5 flex flex-col grow">
      <div class="flex items-center text-sm text-teal-600 font-medium mb-3 space-x-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>{{ formatDate(event.start_date) }}</span>
      </div>
      <h3 class="text-lg font-bold text-gray-900 mb-2 line-clamp-2 leading-tight group-hover:text-teal-700 transition-colors">
        {{ event.title }}
      </h3>
      <p class="text-gray-600 text-sm mb-4 line-clamp-2 grow">
        {{ event.description }}
      </p>
      <div class="mt-auto space-y-4">
        <div class="flex items-center text-sm text-gray-500" v-if="event.location">
          <svg class="w-4 h-4 mr-2 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span class="truncate">{{ formatLocation(event.location) }}</span>
        </div>
        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <div class="flex flex-wrap gap-1">
                  <span v-for="tag in event.tags.slice(0, 2)" :key="tag.id" class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                  {{ tag.name }}
                  </span>
            <span v-if="event.tags.length > 2" class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                  +{{ event.tags.length - 2 }}
                  </span>
          </div>
        </div>
      </div>
    </div>
  </RouterLink>
</template>