import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';

// Create the authentication context
const AuthContext = createContext(null);

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  // Function to check if user is authenticated
  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('access_token');

      if (!token) {
        setIsAuthenticated(false);
        setUser(null);
        setLoading(false);
        return;
      }

      const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.data) {
        setIsAuthenticated(true);
        setUser({
          username: response.data.username || response.data,
          balance: response.data.balance || 0,
          ...response.data
        });
      } else {
        setIsAuthenticated(false);
        setUser(null);
      }
    } catch (error) {
      console.error('Authentication check failed:', error);
      setIsAuthenticated(false);
      setUser(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } finally {
      setLoading(false);
    }
  };

  const login = (tokens) => {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    setIsAuthenticated(true);
    checkAuthStatus();
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
    setUser(null);
    navigate('/');
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  useEffect(() => {
    if (loading) return;

    const publicPages = ['/', '/about', '/signup'];
    const authRequiredPages = ['/profile', '/slots', '/blackjack', '/dice'];
    const authForbiddenPages = ['/signup'];
    const path = location.pathname;

    if (!isAuthenticated && authRequiredPages.includes(path)) {
      navigate('/signup');
    } else if (isAuthenticated && authForbiddenPages.includes(path)) {
      navigate('/profile');
    }
  }, [isAuthenticated, loading, location.pathname, navigate]);

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    checkAuthStatus
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
