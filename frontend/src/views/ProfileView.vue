<template>
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-2xl mx-auto">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center space-x-4 mb-6">
            <img
              :src="user?.profile_image || '/placeholder-avatar.png'"
              alt="Profile"
              class="w-20 h-20 rounded-full object-cover"
            />
            <div>
              <h1 class="text-2xl font-bold">{{ user?.username }}</h1>
              <p class="text-gray-600">{{ user?.email }}</p>
            </div>
          </div>
          <router-link
            to="/profile/edit"
            class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 inline-block"
          >
            Edit Profile
          </router-link>
        </div>
        <div class="mt-8">
          <h2 class="text-xl font-semibold mb-4">My Blogs</h2>
          <div class="space-y-4">
            <article
              v-for="blog in userBlogs"
              :key="blog.id"
              class="bg-white rounded-lg shadow-md p-4"
            >
              <h3 class="text-lg font-medium mb-2">{{ blog.title }}</h3>
              <p class="text-gray-600 mb-2">{{ blog.description }}</p>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-500">
                  {{ new Date(blog.created_at).toLocaleDateString() }}
                </span>
                <div class="space-x-2">
                  <router-link
                    :to="{ name: 'blog-edit', params: { id: blog.id }}"
                    class="text-blue-600 hover:underline"
                  >
                    Edit
                  </router-link>
                  <button
                    @click="deleteBlog(blog.id)"
                    class="text-red-600 hover:underline"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  interface Blog {
    id: number;
    title: string;
    description: string;
    created_at: string;
  }
  const auth = useAuthStore();
  const userBlogs = ref<Blog[]>([]);
  const user = computed(() => auth.user);
  const fetchUserBlogs = async () => {
    try {
      const response = await fetch(`/api/blogs?author=${user.value?.id}`);
      userBlogs.value = await response.json();
    } catch (error) {
      console.error('Error fetching user blogs:', error);
    }
  };
  const deleteBlog = async (blogId: number) => {
    if (!confirm('Are you sure you want to delete this blog?')) return;
    try {
      await fetch(`/api/blogs/${blogId}`, {
        method: 'DELETE',
      });
      await fetchUserBlogs();
    } catch (error) {
      console.error('Error deleting blog:', error);
    }
  };
  onMounted(() => {
    if (user.value) {
      fetchUserBlogs();
    }
  });
  </script>