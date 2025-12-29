import axios, { AxiosInstance } from 'axios';
import * as SecureStore from 'expo-secure-store';
import { API_URL, API_ENDPOINTS } from '../config/api';
import {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  User,
  Category,
  Expense,
  ExpenseListResponse,
  CreateExpenseRequest,
} from '../types';

const TOKEN_KEY = 'auth_token';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      async (config) => {
        const token = await this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          await this.clearToken();
        }
        return Promise.reject(error);
      }
    );
  }

  // Token management
  async saveToken(token: string): Promise<void> {
    await SecureStore.setItemAsync(TOKEN_KEY, token);
  }

  async getToken(): Promise<string | null> {
    return await SecureStore.getItemAsync(TOKEN_KEY);
  }

  async clearToken(): Promise<void> {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
  }

  // Auth endpoints
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>(API_ENDPOINTS.LOGIN, data);
    await this.saveToken(response.data.access_token);
    return response.data;
  }

  async register(data: RegisterRequest): Promise<User> {
    const response = await this.api.post<User>(API_ENDPOINTS.REGISTER, data);
    return response.data;
  }

  async getMe(): Promise<User> {
    const response = await this.api.get<User>(API_ENDPOINTS.ME);
    return response.data;
  }

  async logout(): Promise<void> {
    await this.clearToken();
  }

  // Categories endpoints
  async getCategories(): Promise<Category[]> {
    const response = await this.api.get<Category[]>(API_ENDPOINTS.CATEGORIES);
    return response.data;
  }

  async createCategory(data: { name: string; color: string; icon: string; description: string }): Promise<Category> {
    const response = await this.api.post<Category>(API_ENDPOINTS.CATEGORIES, data);
    return response.data;
  }

  async updateCategory(id: string, data: { name: string; color: string }): Promise<Category> {
    const response = await this.api.put<Category>(API_ENDPOINTS.CATEGORY(id), data);
    return response.data;
  }

  async deleteCategory(id: string): Promise<void> {
    await this.api.delete(API_ENDPOINTS.CATEGORY(id));
  }

  // Expenses endpoints
  async getExpenses(page: number = 1, limit: number = 20): Promise<ExpenseListResponse> {
    const skip = (page - 1) * limit;
    const response = await this.api.get<ExpenseListResponse>(API_ENDPOINTS.EXPENSES, {
      params: { skip, limit },
    });
    return response.data;
  }

  async createExpense(data: CreateExpenseRequest): Promise<Expense> {
    const response = await this.api.post<Expense>(API_ENDPOINTS.EXPENSES, data);
    return response.data;
  }

  async deleteExpense(id: string): Promise<void> {
    await this.api.delete(API_ENDPOINTS.EXPENSE(id));
  }
}

export default new ApiService();
