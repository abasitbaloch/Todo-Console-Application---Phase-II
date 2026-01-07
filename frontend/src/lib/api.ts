import { authService } from './client-auth';
import { Task, TaskCreate, TaskUpdate } from './types'; // Import types to be safe

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const token = authService.getToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      authService.logout();
      if (typeof window !== 'undefined') {
        window.location.href = '/';
      }
      throw new Error('Unauthorized');
    }
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'API request failed');
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  getTasks: () => fetchWithAuth('/tasks/'),

  createTask: (title: string, description?: string) =>
    fetchWithAuth('/tasks/', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    }),

  // CHANGED: taskId is now string, and accepts partial updates
  updateTask: (taskId: string, updates: TaskUpdate) =>
    fetchWithAuth(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    }),

  // CHANGED: taskId is now string
  deleteTask: (taskId: string) =>
    fetchWithAuth(`/tasks/${taskId}`, {
      method: 'DELETE',
    }),
};