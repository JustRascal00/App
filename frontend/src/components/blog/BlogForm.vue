<template>
    <div class="blog-form max-w-4xl mx-auto">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="title" class="block text-sm font-medium">Title</label>
          <input
            id="title"
            v-model="formData.title"
            type="text"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label for="main_image" class="block text-sm font-medium">Main Image</label>
          <input
            id="main_image"
            type="file"
            @change="handleImageUpload"
            accept="image/*"
            class="mt-1 block w-full"
          />
        </div>
        <div>
          <label for="description" class="block text-sm font-medium">Description</label>
          <editor
            v-model="formData.description"
            api-key="your-tinymce-api-key"
            :init="{
              plugins: 'link image code',
              toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright | link image | code'
            }"
          />
        </div>
        <div>
          <label for="category" class="block text-sm font-medium">Category</label>
          <select
            id="category"
            v-model="formData.category"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          >
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.title }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium">Tags</label>
          <div class="mt-1 flex flex-wrap gap-2">
            <div
              v-for="tag in tags"
              :key="tag.id"
              class="flex items-center"
            >
              <input
                type="checkbox"
                :id="'tag-' + tag.id"
                :value="tag.id"
                v-model="formData.tags"
                class="mr-2"
              />
              <label :for="'tag-' + tag.id">{{ tag.title }}</label>
            </div>
          </div>
        </div>
        <button
          type="submit"
          class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Saving...' : 'Save Blog' }}
        </button>
      </form>
    </div>
  </template>
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import Editor from '@tinymce/tinymce-vue';
  interface Category {
    id: number;
    title: string;
  }
  interface Tag {
    id: number;
    title: string;
  }
  const formData = ref({
    title: '',
    main_image: null as File | null,
    description: '',
    category: '',
    tags: [] as number[]
  });
  const categories = ref<Category[]>([]);
  const tags = ref<Tag[]>([]);
  const isLoading = ref(false);
  const handleImageUpload = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      formData.value.main_image = target.files[0];
    }
  };
  const handleSubmit = async () => {
    try {
      isLoading.value = true;
      const formDataToSend = new FormData();
      Object.entries(formData.value).forEach(([key, value]) => {
        if (value !== null) {
          if (key === 'tags') {
            formDataToSend.append(key, JSON.stringify(value));
          } else {
            formDataToSend.append(key, value);
          }
        }
      });
      await fetch('/api/blogs/', {
        method: 'POST',
        body: formDataToSend
      });
      
      // Reset form or redirect
    } catch (error) {
      console.error('Error saving blog:', error);
    } finally {
      isLoading.value = false;
    }
  };
  onMounted(async () => {
    try {
      const [categoriesResponse, tagsResponse] = await Promise.all([
        fetch('/api/categories/'),
        fetch('/api/tags/')
      ]);
      categories.value = await categoriesResponse.json();
      tags.value = await tagsResponse.json();
    } catch (error) {
      console.error('Error fetching form data:', error);
    }
  });
  </script>