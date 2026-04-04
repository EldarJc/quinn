<script setup>
import { Form, Field, ErrorMessage } from "vee-validate";
import * as yup from "yup";
import { useRouter } from "vue-router";
import {useUserStore} from "@/stores/user.js";

const schema = yup.object({
  username: yup.string().required("Username is required!"),
  password: yup.string().required("Password is required!"),
});

const router = useRouter();
const userStore = useUserStore();
userStore.error = null;

async function handleLogin(values) {
  try {
    await userStore.login(values);
    await router.push("/");
    userStore.error = null;
  } catch (error) {}
}

</script>


<template>
  <div class="flex items-center justify-center">
    <div class="w-110 mx-auto p-8 bg-gray-50 shadow-xl rounded-xl border border-gray-200">
      <h2 class="text-2xl font-bold text-center text-gray-500 mb-5">Log In</h2>
      <div v-if="userStore.error "
           class="text-center text-lg mb-4 text-red-700 rounded">
        {{userStore.error.message}}
      </div>
      <Form :validation-schema="schema" @submit="handleLogin">
        <div>
          <Field name="username" type="text" placeholder="Username" class=" w-full px-4 py-3 text-lg border-2 form-control border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-300" />
          <ErrorMessage name="username" class="text-red-500 text-sm" />
        </div>
        <div>
          <Field name="password" type="password" placeholder="Password"  class="w-full px-4 py-3 mt-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-300" />
          <ErrorMessage name="password" class="text-red-500 text-sm" />
        </div>
        <div class="flex items-center justify-between mt-2">
          <label class="flex items-center">
            <input type="checkbox" class="mr-2">
            <span class="text-sm text-gray-600">Remember me</span>
          </label>
          <RouterLink to="/" class="text-sm text-olive-500 hover:underline">Forgot password?</RouterLink>
        </div>
        <button type="submit" class="mt-3 text-lg font-semibold
                bg-gray-800 w-full text-white rounded-lg
                px-6 py-3 block shadow-xl hover:text-white hover:bg-black">Log In</button>
      </Form>
      <p class="text-sm text-center text-gray-500 mt-6">Don't have an account? <RouterLink to="/register"
                                                                                  class="text-olive-500 hover:underline">Create One</RouterLink></p>
    </div>
  </div>
</template>