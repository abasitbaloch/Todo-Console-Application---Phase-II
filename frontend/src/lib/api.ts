import { authService } from './client-auth';

// Ensure the URL is HTTPS and has NO trailing slash at the end
const BASE_URL = 'https://janabkakarot-todo-console-application.hf.space';

const getUrl = (path: string) => {
  // Ensure path starts with / and remove any double slashes
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  // IMPORTANT: Remove any trailing slash from the final URL
  return `${BASE_URL}${cleanPath}`.replace(/\/$/, "");
};

export const api = {
  async getTasks() {
    const token = authService.getToken();
    const url = getUrl('/tasks');

    console.log("Fetching tasks from:", url);

    const response = await fetch(url, {
      method: 'GET',
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
  }
};