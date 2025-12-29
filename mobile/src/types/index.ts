export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: string;
  name: string;
  description?: string;
  color: string;
  icon: string;
  is_default: boolean;
  created_at: string;
}

export interface Expense {
  id: string;
  amount: string;
  description: string;
  expense_date: string;
  payment_method: string;
  notes?: string;
  category_id?: string;
  category?: Category;
  ai_suggested_category_id?: string;
  ai_suggested_category?: Category;
  ai_confidence_score?: number;
  created_at: string;
  updated_at: string;
}

export interface ExpenseListResponse {
  items: Expense[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface CreateExpenseRequest {
  description: string;
  amount: number;
  expense_date: string;
  payment_method: string;
  notes?: string;
  category_id?: string;
}
