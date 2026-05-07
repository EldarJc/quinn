<script setup>
import { ref, computed, onMounted } from "vue";
import TagService from '@/api/tag.js';

const props = defineProps({
  minTags: { type: Number, default: 2 },
  maxTags: { type: Number, default: 5 }
});

const tagService = new TagService();
const selectedIds = defineModel({ default: () => [] });

const allTags = ref([]);
const currentPage = ref(1);
const isLoading = ref(false);
const hasMoreTags = ref(true);

const isMaxReached = computed(() => selectedIds.value.length >= props.maxTags);

const selectedTagObjects = computed(() => {
  return selectedIds.value
      .map(id => allTags.value.find(t => t.id === id))
      .filter(Boolean);
});

onMounted(() => loadTags());

const loadTags = async () => {
  if (isLoading.value || !hasMoreTags.value) return;

  isLoading.value = true;
  try {
    const { data } = await tagService.getTags(currentPage.value);

    if (data?.length) {
      allTags.value.push(...data);
      currentPage.value++;
    } else {
      hasMoreTags.value = false;
    }
  } catch (error) {
  } finally {
    isLoading.value = false;
  }
};

const toggleTag = (tag) => {
  if (selectedIds.value.includes(tag.id)) {
    selectedIds.value = selectedIds.value.filter(id => id !== tag.id);
  } else if (!isMaxReached.value) {
    selectedIds.value = [...selectedIds.value, tag.id];
  }
};
</script>

<template>
  <div class="space-y-5">
    <div class="flex items-center justify-between">
      <p class="text-sm text-slate-500">
        Select between <span class="font-semibold text-slate-700">{{ props.minTags }}</span> and <span class="font-semibold text-slate-700">{{ props.maxTags }}</span> tags to help people find your event.
      </p>
      <span class="text-xs font-bold px-3 py-1 rounded-full"
            :class="isMaxReached ? 'bg-orange-100 text-orange-700' : 'bg-slate-100 text-slate-600'">
         {{ selectedIds.length }} / {{ props.maxTags }} selected
         </span>
    </div>
    <div class="bg-slate-50 p-4 rounded-xl border border-slate-100 h-55 overflow-y-auto custom-scrollbar">
      <div class="flex flex-wrap gap-2.5">
        <button
            v-for="tag in allTags"
            :key="tag.id"
            @click="toggleTag(tag)"
            type="button"
            :disabled="!selectedIds.includes(tag.id) && isMaxReached"
            :class="[
               'px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 border',
               selectedIds.includes(tag.id)
               ? 'bg-[#608a89] text-white border-[#608a89] shadow-md shadow-[#608a89]/20 scale-[1.02]'
               : 'bg-white text-slate-600 border-slate-200 hover:border-[#608a89] hover:text-[#608a89] hover:shadow-sm disabled:opacity-50 disabled:hover:scale-100 disabled:cursor-not-allowed'
               ]"
        >
          {{ tag.name }}
        </button>
      </div>
      <button
          v-if="hasMoreTags || isLoading"
          @click="loadTags"
          type="button"
          :disabled="isLoading"
          class="w-full mt-4 py-2.5 text-sm font-semibold rounded-xl transition duration-200 border border-slate-200 bg-white"
          :class="isLoading ? 'text-slate-400 opacity-70 cursor-not-allowed' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
      >
        {{ isLoading ? 'Loading tags...' : 'Load more tags' }}
      </button>
    </div>
    <div v-if="selectedIds.length > 0" class="pt-4 border-t border-slate-100">
      <p class="text-xs font-bold text-slate-400 mb-3 uppercase tracking-wider">Your selection</p>
      <div class="flex flex-wrap gap-2">
        <div
            v-for="tag in selectedTagObjects"
            :key="'selected-'+tag.id"
            class="group inline-flex items-center gap-1.5 bg-slate-800 text-white px-3 py-1.5 rounded-lg text-sm font-medium shadow-sm transition-transform hover:-translate-y-0.5"
        >
          {{ tag.name }}
          <button
              @click="toggleTag(tag)"
              type="button"
              class="w-5 h-5 flex items-center justify-center rounded-full bg-white/20 hover:bg-red-500 hover:text-white transition-colors text-xs ml-1"
              aria-label="Remove tag"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  </div>
</template>