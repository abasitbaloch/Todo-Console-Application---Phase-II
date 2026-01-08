// backend/src/lib/api.ts
import { authService } from './client-auth';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://janabkakarot-todo-console-application.hf.space';

// Helper to ensure all URLs are HTTPS and have no double slashes
const getUrl = (path: string) => {
  const cleanBase = BASE_URL.replace('http://', 'https://').replace(/\/$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBase}${cleanPath}`;
};

export const api = {
  async getTasks() {
    const token = authService.getToken();
    const response = await fetch(getUrl('/tasks'), {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 401) authService.logout();
      throw new Error('Failed to fetch tasks');
    }
    return response.json();
  },

  async createTask(title: string, description?: string) {
    const token = authService.getToken();
    const response = await fetch(getUrl('/tasks'), {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, description }),
    });
    return response.json();
  },

  async toggleTask(taskId: string, completed: boolean) {
    const token = authService.getToken();
    const response = await fetch(getUrl(`/tasks/${taskId}`), {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ is_completed: completed }),
    });
    return response.json();
  },

  async deleteTask(taskId: string) {
    const token = authService.getToken();
    await fetch(getUrl(`/tasks/${taskId}`), {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }
};