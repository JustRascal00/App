<template>
    <div class="comments-section space-y-6">
      <div v-if="isAuthenticated" class="mb-6">
        <button
          @click="showCommentForm = true"
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Add Comment
        </button>
      </div>
      <div class="space-y-4">
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="bg-white p-4 rounded-lg shadow"
        >
          <div class="flex justify-between items-start mb-2">
            <div>
              <span class="font-medium">{{ comment.author.username }}</span>
              <span class="text-sm text-gray-500 ml-2">
                {{ new Date(comment.created_at).toLocaleDateString() }}
              </span>
            </div>
            <div v-if="isCommentOwner(comment)" class="space-x-2">
              <button
                @click="editComment(comment)"
                class="text-blue-600 hover:underline text-sm"
              >
                Edit
              </button>
              <button
                @click="deleteComment(comment.id)"
                class="text-red-600 hover:underline text-sm"
              >
                Delete
              </button>
            </div>
          </div>
          <p class="text-gray-700">{{ comment.content }}</p>
          <div class="mt-2 flex items-center space-x-4">
            <button
              @click="likeComment(comment.id)"
              class="text-gray-500 hover:text-blue-600"
            >
              👍 {{ comment.likes }}
            </button>
            <button
              @click="dislikeComment(comment.id)"
              class="text-gray-500 hover:text-red-600"
            >
              👎 {{ comment.dislikes }}
            </button>
          </div>
        </div>
      </div>
      <!-- Comment Form Modal -->
      <div v-if="showCommentForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg max-w-lg w-full">
          <h3 class="text-lg font-medium mb-4">
            {{ editingComment ? 'Edit Comment' : 'Add Comment' }}
          </h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <textarea
              v-model="commentContent"
              rows="4"
              class="w-full border rounded-md p-2"
              required
            ></textarea>
            <div class="flex justify-end space-x-2">
              <button
                type="button"
                @click="closeCommentForm"
                class="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
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
  import { useAuthStore } from '@/stores/auth';
  interface Comment {
    id: number;
    content: string;
    author: {
      id: number;
      username: string;
    };
    created_at: string;
    likes: number;
    dislikes: number;
  }
  const props = defineProps<{
    blogId: number;
  }>();
  const auth = useAuthStore();
  const comments = ref<Comment[]>([]);
  const showCommentForm = ref(false);
  const commentContent = ref('');
  const editingComment = ref<Comment | null>(null);
  const isLoading = ref(false);
  const isAuthenticated = computed(() => auth.isAuthenticated);
  const isCommentOwner = (comment: Comment) => {
    return auth.user?.id === comment.author.id;
  };
  const fetchComments = async () => {
    try {
      const response = await fetch(`/api/blogs/${props.blogId}/comments`);
      comments.value = await response.json();
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };
  const handleSubmit = async () => {
    try {
      isLoading.value = true;
      const url = editingComment.value
        ? `/api/comments/${editingComment.value.id}`
        : '/api/comments';
      
      const method = editingComment.value ? 'PUT' : 'POST';
      
      await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: commentContent.value,
          blog_id: props.blogId,
        }),
      });
      await fetchComments();
      closeCommentForm();
    } catch (error) {
      console.error('Error saving comment:', error);
    } finally {
      isLoading.value = false;
    }
  };
  const editComment = (comment: Comment) => {
    editingComment.value = comment;
    commentContent.value = comment.content;
    showCommentForm.value = true;
  };
  const deleteComment = async (commentId: number) => {
    if (!confirm('Are you sure you want to delete this comment?')) return;
    
    try {
      await fetch(`/api/comments/${commentId}`, {
        method: 'DELETE',
      });
      await fetchComments();
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };
  const closeCommentForm = () => {
    showCommentForm.value = false;
    editingComment.value = null;
    commentContent.value = '';
  };
  const likeComment = async (commentId: number) => {
    try {
      await fetch(`/api/comments/${commentId}/like`, { method: 'POST' });
      await fetchComments();
    } catch (error) {
      console.error('Error liking comment:', error);
    }
  };
  const dislikeComment = async (commentId: number) => {
    try {
      await fetch(`/api/comments/${commentId}/dislike`, { method: 'POST' });
      await fetchComments();
    } catch (error) {
      console.error('Error disliking comment:', error);
    }
  };
  onMounted(() => {
    fetchComments();
  });
  </script>