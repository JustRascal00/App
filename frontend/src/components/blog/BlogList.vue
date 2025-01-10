<template>
    <div class="blog-list">
      <div class="filters mb-6">
        <input
          type="date"
          v-model="filters.startDate"
          class="mr-2 rounded-md border-gray-300"
        />
        <input
          type="date"
          v-model="filters.endDate"
          class="rounded-md border-gray-300"
        />
      </div>
      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="blog in blogs"
          :key="blog.id"
          class="bg-white rounded-lg shadow-md overflow-hidden"
        >
          <img
            :src="blog.main_image"
            :alt="blog.title"
            class="w-full h-48 object-cover"
          />
          <div class="p-4">
            <h2 class="text-xl font-semibold mb-2">{{ blog.title }}</h2>
            <p class="text-gray-600 mb-4">{{ blog.description }}</p>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">
                {{ new Date(blog.created_at).toLocaleDateString() }}
              </span>
              <router-link
                :to="{ name: 'blog-detail', params: { id: blog.id }}"
                class="text-blue-600 hover:underline"
              >
                Read more
              </router-link>
            </div>
          </div>
        </article>
      </div>
      <div class="mt-6 flex justify-center">
        <button
          v-if="hasMore"
          @click="loadMore"
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Loading...' : 'Load More' }}
        </button>
      </div>
    </div>
  </template>
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  interface Blog {
    id: number;
    title: string;
    main_image: string;
    description: string;
    created_at: string;
  }
  const blogs = ref<Blog[]>([]);
  const isLoading = ref(false);
  const hasMore = ref(true);
  const page = ref(1);
  const filters = ref({
    startDate: '',
    endDate: ''
  });
  const fetchBlogs = async () => {
    try {
      isLoading.value = true;
      const response = await fetch(`/api/blogs?page=${page.value}`);
      const data = await response.json();
      blogs.value = [...blogs.value, ...data.results];
      hasMore.value = data.next !== null;
      page.value++;
    } catch (error) {
      console.error('Error fetching blogs:', error);
    } finally {
      isLoading.value = false;
    }
  };
  const loadMore = () => {
    if (!isLoading.value) {
      fetchBlogs();
    }
  };
  onMounted(() => {
    fetchBlogs();
  });
  </script>