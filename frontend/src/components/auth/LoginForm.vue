<template>
    <div class="login-form">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="username" class="block text-sm font-medium">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div class="flex justify-between items-center">
          <button
            type="submit"
            class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Logging in...' : 'Login' }}
          </button>
          <a
            href="#"
            @click.prevent="$emit('showResetPassword')"
            class="text-sm text-blue-600 hover:underline"
          >
            Forgot Password?
          </a>
        </div>
      </form>
    </div>
  </template>
  <script setup lang="ts">
  import { ref } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  const auth = useAuthStore();
  const username = ref('');
  const password = ref('');
  const isLoading = ref(false);
  const handleSubmit = async () => {
    try {
      isLoading.value = true;
      await auth.login(username.value, password.value);
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      isLoading.value = false;
    }
  };
  </script>