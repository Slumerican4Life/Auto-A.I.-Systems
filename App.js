import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { AuthProvider, useAuth } from './contexts/AuthContext';
import DashboardLayout from './layouts/DashboardLayout';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import LeadsList from './pages/leads/LeadsList';
import LeadDetail from './pages/leads/LeadDetail';
import ReviewsList from './pages/reviews/ReviewsList';
import ReviewDetail from './pages/reviews/ReviewDetail';
import ReferralsList from './pages/reviews/ReferralsList';
import ContentList from './pages/content/ContentList';
import ContentDetail from './pages/content/ContentDetail';
import ContentGenerator from './pages/content/ContentGenerator';
import Analytics from './pages/analytics/Analytics';
import Settings from './pages/settings/Settings';
import NotFound from './pages/NotFound';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// Protected route component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return children;
};

// Layout wrapper for protected routes
const ProtectedLayout = ({ children }) => {
  return (
    <ProtectedRoute>
      <DashboardLayout>{children}</DashboardLayout>
    </ProtectedRoute>
  );
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected routes */}
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
            
            {/* Lead routes */}
            <Route path="/leads" element={<ProtectedLayout><LeadsList /></ProtectedLayout>} />
            <Route path="/leads/:id" element={<ProtectedLayout><LeadDetail /></ProtectedLayout>} />
            
            {/* Review routes */}
            <Route path="/reviews" element={<ProtectedLayout><ReviewsList /></ProtectedLayout>} />
            <Route path="/reviews/:id" element={<ProtectedLayout><ReviewDetail /></ProtectedLayout>} />
            <Route path="/referrals" element={<ProtectedLayout><ReferralsList /></ProtectedLayout>} />
            
            {/* Content routes */}
            <Route path="/content" element={<ProtectedLayout><ContentList /></ProtectedLayout>} />
            <Route path="/content/:id" element={<ProtectedLayout><ContentDetail /></ProtectedLayout>} />
            <Route path="/content/generate" element={<ProtectedLayout><ContentGenerator /></ProtectedLayout>} />
            
            {/* Analytics route */}
            <Route path="/analytics" element={<ProtectedLayout><Analytics /></ProtectedLayout>} />
            
            {/* Settings route */}
            <Route path="/settings" element={<ProtectedLayout><Settings /></ProtectedLayout>} />
            
            {/* 404 route */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Router>
        
        <ToastContainer position="top-right" autoClose={5000} />
      </AuthProvider>
      
      {process.env.NODE_ENV === 'development' && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}

export default App;

