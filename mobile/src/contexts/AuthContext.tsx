import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import apiService from '../services/api';
import { User, LoginRequest, RegisterRequest } from '../types';

interface AuthContextData {
  user: User | null;
  loading: boolean;
  signIn: (data: LoginRequest) => Promise<void>;
  signUp: (data: RegisterRequest) => Promise<void>;
  signOut: () => Promise<void>;
  isAuthenticated: boolean;
}

const defaultAuthContext: AuthContextData = {
  user: null,
  loading: false,
  signIn: async () => {},
  signUp: async () => {},
  signOut: async () => {},
  isAuthenticated: false,
};

const AuthContext = createContext<AuthContextData>(defaultAuthContext);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check if user is already logged in on app start
  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    setLoading(true);
    try {
      const token = await apiService.getToken();
      if (token && token !== 'null' && token !== 'undefined') {
        const userData = await apiService.getMe();
        setUser(userData);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Failed to load user:', error);
      await apiService.clearToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const signIn = async (data: LoginRequest) => {
    try {
      await apiService.login(data);
      const userData = await apiService.getMe();
      setUser(userData);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const signUp = async (data: RegisterRequest) => {
    try {
      await apiService.register(data);
      // Auto-login after registration
      await signIn({ email: data.email, password: data.password });
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  };

  const signOut = async () => {
    await apiService.logout();
    setUser(null);
  };

  const isAuthenticated = Boolean(user !== null && user !== undefined);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        signIn,
        signUp,
        signOut,
        isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
