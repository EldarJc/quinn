<script setup>
import { Form, Field, ErrorMessage } from "vee-validate";
import * as yup from "yup";
import TagsSelect from "@/components/TagsSelect.vue";
import DragDrop from "@/components/DragDrop.vue";
import LocationForm from "@/components/LocationForm.vue";
import EventService from "@/api/event.js";
import router from "@/router/routes.js";

const eventService = new EventService();

const schema = yup.object({
  title: yup.string().required("Title is required!"),
  description: yup.string().required("Description is required!"),
  event_type: yup.string().required("Event type is required!"),
  max_attendees: yup.number()
      .transform((value) => Number.isNaN(value) ? null : value)
      .nullable()
      .positive("Must be a positive number"),
  start_date: yup.date().required("Start date is required!"),
  end_date: yup.date().required("End date is required!"),
  tags: yup.array().required("Tags are required!").min(2, "Select at least 2 tags!").max(5, "Max 5 tags allowed!"),

  location: yup.object().when('event_type', {
    is: (val) => val && !['ONLINE', 'WEBINAR'].includes(val),
    then: (schema) => schema.shape({
      country: yup.string().required("Country is required!"),
      state: yup.string().nullable().notRequired(),
      city: yup.string().required("City is required!"),
      address: yup.string().required("Address is required!")
    }),
    otherwise: (schema) => schema.nullable().notRequired()
  })
});

const eventTypes = [
  { value: "ONLINE", label: "Online" },
  { value: "MEETUP", label: "Meetup" },
  { value: "WORKSHOP", label: "Workshop" },
  { value: "CONFERENCE", label: "Conference" },
  { value: "WEBINAR", label: "Webinar" },
  { value: "TRIP", label: "Trip" }
];

async function handleSubmit(values, { setErrors }) {
  const {image, ...payload} = values;
  try {
    const response = await eventService.create(payload);
    const newEventId = response.data.id;
    const newEventSlug = response.data.slug;

    if (image){
      const formData = new FormData();
      formData.append('image', image);
      await eventService.updateImage(newEventId, formData);
    }

    await router.push({
      name: 'event-details',
      params: {id:newEventId, slug: newEventSlug}
    });

  } catch (error) {
    setErrors(error);
  }
}
</script>

<template>
  <div class="max-w-7xl px-8">
    <div class="mb-4">
      <h1 class="text-3xl font-bold text-slate-800 tracking-tight">Create New Event</h1>
      <p class="text-slate-500 mt-2">Set up your event in just a few steps.</p>
    </div>
    <Form :validation-schema="schema" @submit="handleSubmit" v-slot="{ values, isSubmitting }">
      <div class="grid grid-cols-12 gap-8">
        <div class="col-span-6 space-y-6">
          <div class="bg-white rounded-2xl shadow-sm border border-slate-200/60 p-6">
            <h2 class="text-xl font-semibold text-slate-800 mb-3 flex items-center gap-2">
              <span class="w-8 h-8 rounded-lg bg-[#608a89]/10 text-[#608a89] flex items-center justify-center text-sm">1</span>
              Basic Details
            </h2>
            <div class="space-y-5">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Event Title <span class="text-red-500">*</span></label>
                <Field name="title" type="text" placeholder="e.g. Summer Tech Meetup 2026" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200"/>
                <ErrorMessage name="title" class="text-red-500 text-sm mt-1 block" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Description <span class="text-red-500">*</span></label>
                <Field name="description" as="textarea" rows="4" placeholder="What is this event about?" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200 resize-none"/>
                <ErrorMessage name="description" class="text-red-500 text-sm mt-1 block" />
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-1">Type <span class="text-red-500">*</span></label>
                  <Field name="event_type" as="select" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200">
                    <option value="" disabled>Select type</option>
                    <option v-for="type in eventTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
                  </Field>
                  <ErrorMessage name="event_type" class="text-red-500 text-sm mt-1 block"/>
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-1">Max Attendees</label>
                  <Field name="max_attendees" type="number" placeholder="Unlimited" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200"/>
                  <ErrorMessage name="max_attendees" class="text-red-500 text-sm mt-1 block" />
                </div>
              </div>
              <div class="pt-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">Cover Image</label>
                <Field name="image" v-slot="{value, handleChange}">
                  <DragDrop :model-value="value" @update:model-value="handleChange" />
                </Field>
              </div>
            </div>
          </div>
        </div>
        <div class="col-span-6 space-y-6">
          <div class="bg-white rounded-2xl shadow-sm border border-slate-200/60 p-6">
            <h2 class="text-xl font-semibold text-slate-800 mb-6 flex items-center gap-2">
              <span class="w-8 h-8 rounded-lg bg-[#608a89]/10 text-[#608a89] flex items-center justify-center text-sm">2</span>
              Set Event Duration
            </h2>
            <div class="grid grid-cols-2 gap-6">
              <div>
                <label for="start_date" class="block text-sm font-medium text-slate-700 mb-2">Start Date <span class="text-red-500">*</span></label>
                <Field name="start_date" type="datetime-local" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200"/>
                <ErrorMessage name="start_date" class="text-red-500 text-sm mt-1 block" />
              </div>
              <div>
                <label for="end_date" class="block text-sm font-medium text-slate-700 mb-2">End Date <span class="text-red-500">*</span></label>
                <Field name="end_date" type="datetime-local" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 focus:bg-white focus:outline-none focus:border-[#608a89] focus:ring-4 focus:ring-[#608a89]/10 transition-all duration-200"/>
                <ErrorMessage name="end_date" class="text-red-500 text-sm mt-1 block" />
              </div>
            </div>
          </div>
          <div v-if="values.event_type && !['ONLINE', 'WEBINAR'].includes(values.event_type)" class="bg-white rounded-2xl shadow-sm border border-slate-200/60 p-6">
            <LocationForm />
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-slate-200/60 p-6">
            <h2 class="text-xl font-semibold text-slate-800 mb-6 flex items-center gap-2">
              <span class="w-8 h-8 rounded-lg bg-[#608a89]/10 text-[#608a89] flex items-center justify-center text-sm">3</span>
              Event Tags
            </h2>
            <Field name="tags" v-slot="{value, handleChange}">
              <TagsSelect :model-value="value" @update:model-value="handleChange" />
            </Field>
            <ErrorMessage name="tags" class="text-red-500 text-sm mt-2 block" />
          </div>
        </div>
      </div>
      <div class="mt-8 pt-6 border-t border-slate-200 flex items-center justify-end gap-4">
        <button type="button" @click="router.push('/')" class="px-6 py-3 text-slate-600 font-medium hover:bg-slate-100 rounded-xl transition duration-200">
          Cancel
        </button>
        <button type="submit" :disabled="isSubmitting" class="px-8 py-3 bg-[#608a89] text-white font-semibold rounded-xl shadow-md shadow-[#608a89]/20 hover:bg-[#4f7372] hover:-translate-y-0.5 transition-all duration-200 flex items-center disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none">
          <span v-if="isSubmitting" class="animate-spin mr-3 h-5 w-5 border-2 border-white/30 border-t-white rounded-full"></span>
          {{ isSubmitting ? 'Creating Event...' : 'Create Event' }}
        </button>
      </div>
    </Form>
  </div>
</template>