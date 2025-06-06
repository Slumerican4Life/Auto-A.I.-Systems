import React, { createContext, useContext, useState, useEffect } from 'react';

// Create the auth context
const AuthContext = createContext();

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is already logged in on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        // Check if there's a token in localStorage
        const token = localStorage.getItem('auth_token');
        
        if (token) {
          // In a real app, you would validate the token with your backend
          // For now, we'll just simulate a user
          const userData = {
            id: 'usr_123456',
            email: 'demo@example.com',
            name: 'Demo User',
            company_id: 'cmp_123456',
            role: 'admin'
          };
          
          setUser(userData);
        }
      } catch (err) {
        console.error('Authentication error:', err);
        setError(err.message);
        // Clear any invalid tokens
        localStorage.removeItem('auth_token');
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  // Login function
  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    
    try {
      // In a real app, you would call your API here
      // For now, we'll simulate a successful login
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Check credentials (in a real app, this would be done by the server)
      if (email === 'demo@example.com' && password === 'password') {
        const userData = {
          id: 'usr_123456',
          email: 'demo@example.com',
          name: 'Demo User',
          company_id: 'cmp_123456',
          role: 'admin'
        };
        
        // Save token to localStorage
        localStorage.setItem('auth_token', 'simulated_jwt_token');
        
        setUser(userData);
        return userData;
      } else {
        throw new Error('Invalid email or password');
      }
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (email, password, name, companyName) => {
    setLoading(true);
    setError(null);
    
    try {
      // In a real app, you would call your API here
      // For now, we'll simulate a successful registration
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const userData = {
        id: 'usr_' + Math.random().toString(36).substr(2, 9),
        email,
        name,
        company_id: 'cmp_' + Math.random().toString(36).substr(2, 9),
        role: 'admin'
      };
      
      // Save token to localStorage
      localStorage.setItem('auth_token', 'simulated_jwt_token');
      
      setUser(userData);
      return userData;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
  };

  // Context value
  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

