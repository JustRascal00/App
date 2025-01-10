import { defineStore } from 'pinia';
import axios from 'axios';
import jwtDecode from 'jwt-decode';
interface User {
  id: number;
  username: string;
  email: string;
  profile_image?: string;
}
interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
}
export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    accessToken: null,
    isAuthenticated: false,
  }),
  actions: {
    async login(username: string, password: string) {
      try {
        const response = await axios.post('/api/auth/login', { username, password });
        this.accessToken = response.data.access_token;
        this.user = jwtDecode(response.data.access_token);
        this.isAuthenticated = true;
        localStorage.setItem('token', response.data.access_token);
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    async register(userData: { username: string; email: string; password: string }) {
      try {
        await axios.post('/api/auth/register', userData);
      } catch (error) {
        console.error('Registration failed:', error);
        throw error;
      }
    },
    async resetPassword(email: string) {
      try {
        await axios.post('/api/auth/reset-password', { email });
      } catch (error) {
        console.error('Password reset failed:', error);
        throw error;
      }
    },
    logout() {
      this.user = null;
      this.accessToken = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token');
    }
  }
});