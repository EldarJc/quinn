<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';
import router from '@/router/routes'
import { useUserStore } from '@/stores/user';

const schema = yup.object({
  username: yup.string().required("Username is required!"),
  first_name: yup.string().required("First Name is required!"),
  last_name: yup.string().required("Last Name is required!"),
  email: yup.string().email("Enter a valid email").required("Email is required!"),
  password: yup.string().min(8, 'Password must be at least 8 characters').required("Password is required!"),
});

const userStore = useUserStore();
userStore.error = null;

async function onSubmit(values, { setErrors }) {
  try {
    await userStore.register(values);
    await router.push({ name: 'login'});
  } catch (error) {
    setErrors(error);
  }
}
</script>

<template>
  <div class="flex items-center justify-center">
    <div class="max-w-110 w-full bg-white rounded px-8 py-10">
      <div class="text-center mb-6">
        <h1 class="text-2xl font-normal tracking-wide">Create your Quinn account</h1>
      </div>

      <p class="text-gray-500 text-center text-lg mb-6">
        Join <span class="font-bold">Quinn</span> to meet new people and pursue passions, together.
      </p>

      <Form :validation-schema="schema" class="space-y-5" @submit="onSubmit">

        <div>
          <Field name="username" type="text" placeholder="Username"
                 class="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-300" />
          <ErrorMessage name="username" class="text-red-500 text-sm" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <Field name="first_name" type="text" placeholder="First name"
                   class="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-300" />
            <ErrorMessage name="first_name" class="text-red-500 text-sm" />
          </div>
          <div>
            <Field name="last_name" type="text" placeholder="Last name"
                   class="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-300" />
            <ErrorMessage name="last_name" class="text-red-500 text-sm" />
          </div>
        </div>

        <div>
          <Field name="email" type="email" placeholder="Email"
                 class="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-300" />
          <ErrorMessage name="email" class="text-red-500 text-sm" />
        </div>

        <div>
          <Field name="password" type="password" placeholder="Password"
                 class="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-300" />
          <ErrorMessage name="password" class="text-red-500 text-sm" />
        </div>

        <button type="submit" class="mt-6 text-lg font-semibold bg-gray-800 w-full text-white rounded-lg px-6 py-3 disabled:opacity-50">
          Register
        </button>
      </Form>
    </div>
  </div>
</template>