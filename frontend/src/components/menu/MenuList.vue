<template>
    <div class="menu-list space-y-4">
      <h2 class="text-2xl font-bold mb-4">Menu Management</h2>
      
      <div class="grid gap-4">
        <div v-for="menu in menus" :key="menu.id" class="bg-white p-4 rounded-lg shadow">
          <div class="flex justify-between items-center">
            <div>
              <h3 class="font-medium">{{ menu.title }}</h3>
              <p class="text-sm text-gray-500">
                Order: {{ menu.order }}
                <span v-if="menu.url" class="ml-2">URL: {{ menu.url }}</span>
                <span v-if="menu.category" class="ml-2">Category: {{ menu.category.title }}</span>
              </p>
            </div>
            <div class="space-x-2">
              <button
                @click="editMenu(menu)"
                class="text-blue-600 hover:text-blue-800"
              >
                Edit
              </button>
              <button
                @click="deleteMenu(menu.id)"
                class="text-red-600 hover:text-red-800"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
      <button
        @click="showForm = true"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Add Menu Item
      </button>
      <!-- Menu Form Modal -->
      <div v-if="showForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg max-w-lg w-full">
          <h3 class="text-lg font-medium mb-4">
            {{ editingMenu ? 'Edit Menu Item' : 'Add Menu Item' }}
          </h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium">Title</label>
              <input
                v-model="formData.title"
                type="text"
                required
                class="mt-1 w-full border rounded-md p-2"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium">Order</label>
              <input
                v-model.number="formData.order"
                type="number"
                required
                class="mt-1 w-full border rounded-md p-2"
              />
            </div>
            <div>
              <label class="block text-sm font-medium">URL (optional)</label>
              <input
                v-model="formData.url"
                type="url"
                class="mt-1 w-full border rounded-md p-2"
              />
            </div>
            <div>
              <label class="block text-sm font-medium">Category (optional)</label>
              <select
                v-model="formData.category"
                class="mt-1 w-full border rounded-md p-2"
              >
                <option value="">None</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.title }}
                </option>
              </select>
            </div>
            <div class="flex justify-end space-x-2">
              <button
                type="button"
                @click="closeForm"
                class="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                :disabled="isLoading"
              >
                {{ isLoading ? 'Saving...' : 'Save' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  interface Category {
    id: number;
    title: string;
  }
  interface Menu {
    id: number;
    title: string;
    order: number;
    url?: string;
    category?: Category;
  }
  const menus = ref<Menu[]>([]);
  const categories = ref<Category[]>([]);
  const showForm = ref(false);
  const isLoading = ref(false);
  const editingMenu = ref<Menu | null>(null);
  const formData = ref({
    title: '',
    order: 0,
    url: '',
    category: ''
  });
  const fetchMenus = async () => {
    try {
      const response = await fetch('/api/menus/');
      menus.value = await response.json();
    } catch (error) {
      console.error('Error fetching menus:', error);
    }
  };
  const fetchCategories = async () => {
    try {
      const response = await fetch('/api/categories/');
      categories.value = await response.json();
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };
  const editMenu = (menu: Menu) => {
    editingMenu.value = menu;
    formData.value = {
      title: menu.title,
      order: menu.order,
      url: menu.url || '',
      category: menu.category?.id || ''
    };
    showForm.value = true;
  };
  const deleteMenu = async (id: number) => {
    if (!confirm('Are you sure you want to delete this menu item?')) return;
    
    try {
      await fetch(`/api/menus/${id}`, { method: 'DELETE' });
      await fetchMenus();
    } catch (error) {
      console.error('Error deleting menu:', error);
    }
  };
  const handleSubmit = async () => {
    try {
      isLoading.value = true;
      const url = editingMenu.value
        ? `/api/menus/${editingMenu.value.id}`
        : '/api/menus/';
      
      const method = editingMenu.value ? 'PUT' : 'POST';
      
      await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData.value),
      });
      await fetchMenus();
      closeForm();
    } catch (error) {
      console.error('Error saving menu:', error);
    } finally {
      isLoading.value = false;
    }
  };
  const closeForm = () => {
    showForm.value = false;
    editingMenu.value = null;
    formData.value = {
      title: '',
      order: 0,
      url: '',
      category: ''
    };
  };
  onMounted(() => {
    fetchMenus();
    fetchCategories();
  });
  </script>