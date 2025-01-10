<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Latest Blogs</h1>
    <BlogList />
  </div>
</template>
<script setup lang="ts">
import BlogList from '@/components/blog/BlogList.vue';
</script>