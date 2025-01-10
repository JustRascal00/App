<template>
    <div class="register-form">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="username" class="block text-sm font-medium">Username</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label for="email" class="block text-sm font-medium">Email</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium">Password</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label for="confirmPassword" class="block text-sm font-medium">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <button
          type="submit"
          class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          :disabled="isLoading || !isValid"
        >
          {{ isLoading ? 'Registering...' : 'Register' }}
        </button>
      </form>
    </div>
  </template>
  <script setup lang="ts">
  import { ref, computed } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  const auth = useAuthStore();
  const isLoading = ref(false);
  const formData = ref({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const isValid = computed(() => {
    return (
      formData.value.username &&
      formData.value.email &&
      formData.value.password &&
      formData.value.password === formData.value.confirmPassword
    );
  });
  const handleSubmit = async () => {
    if (!isValid.value) return;
    
    try {
      isLoading.value = true;
      await auth.register({
        username: formData.value.username,
        email: formData.value.email,
        password: formData.value.password
      });
    } catch (error) {
      console.error('Registration error:', error);
    } finally {
      isLoading.value = false;
    }
  };
  </script>