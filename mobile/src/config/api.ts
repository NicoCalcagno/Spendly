/**
 * API Configuration
 * Update API_URL based on your environment
 */

// For iOS Simulator: use localhost
// For Android Emulator: use 10.0.2.2
// For physical device: use your computer's IP address (e.g., 192.168.1.x)

export const API_URL = __DEV__
  ? 'http://localhost:8000/api/v1'  // Change to your IP if testing on physical device
  : 'https://your-production-api.com/api/v1';

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/auth/login',
  REGISTER: '/users/register',
  ME: '/users/me',

  // Categories
  CATEGORIES: '/categories/',
  CATEGORY: (id: string) => `/categories/${id}`,

  // Expenses
  EXPENSES: '/expenses/',
  EXPENSE: (id: string) => `/expenses/${id}`,
};
