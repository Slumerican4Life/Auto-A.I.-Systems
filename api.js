import axios from 'axios';

// Create axios instance with base URL and default headers
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized errors (token expired)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const login = async (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await api.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const updateUser = async (userData) => {
  const response = await api.put('/auth/me', userData);
  return response.data;
};

export const changePassword = async (oldPassword, newPassword) => {
  const response = await api.post('/auth/password', { old_password: oldPassword, new_password: newPassword });
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/auth/logout');
  localStorage.removeItem('token');
  return response.data;
};

// Lead API
export const createLead = async (leadData) => {
  const response = await api.post('/leads', leadData);
  return response.data;
};

export const getLeads = async (filters = {}) => {
  const response = await api.get('/leads', { params: filters });
  return response.data;
};

export const getLead = async (leadId) => {
  const response = await api.get(`/leads/${leadId}`);
  return response.data;
};

export const updateLead = async (leadId, leadData) => {
  const response = await api.put(`/leads/${leadId}`, leadData);
  return response.data;
};

export const deleteLead = async (leadId) => {
  const response = await api.delete(`/leads/${leadId}`);
  return response.data;
};

export const getLeadInteractions = async (leadId) => {
  const response = await api.get(`/leads/${leadId}/interactions`);
  return response.data;
};

export const createLeadInteraction = async (leadId, interactionData) => {
  const response = await api.post(`/leads/${leadId}/interactions`, interactionData);
  return response.data;
};

export const generateAndSendMessage = async (leadId, messageType, channel) => {
  const response = await api.post(`/leads/${leadId}/message`, null, {
    params: { message_type: messageType, channel },
  });
  return response.data;
};

// Review API
export const createReviewRequest = async (reviewData) => {
  const response = await api.post('/reviews/request', reviewData);
  return response.data;
};

export const getReviews = async (filters = {}) => {
  const response = await api.get('/reviews', { params: filters });
  return response.data;
};

export const getReview = async (reviewId) => {
  const response = await api.get(`/reviews/${reviewId}`);
  return response.data;
};

export const updateReview = async (reviewId, reviewData) => {
  const response = await api.put(`/reviews/${reviewId}`, reviewData);
  return response.data;
};

export const sendReferralOffer = async (reviewId) => {
  const response = await api.post(`/reviews/${reviewId}/send-referral`);
  return response.data;
};

export const getReferrals = async (filters = {}) => {
  const response = await api.get('/reviews/referrals', { params: filters });
  return response.data;
};

export const getReferral = async (referralId) => {
  const response = await api.get(`/reviews/referrals/${referralId}`);
  return response.data;
};

export const validateReferralCode = async (code) => {
  const response = await api.post('/reviews/referrals/validate', null, {
    params: { code },
  });
  return response.data;
};

export const useReferral = async (referralId, leadId) => {
  const response = await api.post(`/reviews/referrals/${referralId}/use`, null, {
    params: { lead_id: leadId },
  });
  return response.data;
};

// Content API
export const createContent = async (contentData) => {
  const response = await api.post('/content', contentData);
  return response.data;
};

export const getContentList = async (filters = {}) => {
  const response = await api.get('/content', { params: filters });
  return response.data;
};

export const getContent = async (contentId) => {
  const response = await api.get(`/content/${contentId}`);
  return response.data;
};

export const updateContent = async (contentId, contentData) => {
  const response = await api.put(`/content/${contentId}`, contentData);
  return response.data;
};

export const deleteContent = async (contentId) => {
  const response = await api.delete(`/content/${contentId}`);
  return response.data;
};

export const generateContent = async (generateRequest) => {
  const response = await api.post('/content/generate', generateRequest);
  return response.data;
};

export const publishContent = async (contentId, publishRequest) => {
  const response = await api.post(`/content/${contentId}/publish`, publishRequest);
  return response.data;
};

export const scheduleContentGeneration = async (contentType, topic, frequency, options = {}) => {
  const response = await api.post('/content/schedule', null, {
    params: {
      content_type: contentType,
      topic,
      frequency,
      ...options,
    },
  });
  return response.data;
};

// Analytics API
export const fetchDashboardMetrics = async (startDate, endDate) => {
  const response = await api.get('/analytics/dashboard', {
    params: {
      start_date: startDate.toISOString(),
      end_date: endDate.toISOString(),
    },
  });
  return response.data;
};

export const fetchLeadMetrics = async (startDate, endDate, source) => {
  const response = await api.get('/analytics/leads', {
    params: {
      start_date: startDate.toISOString(),
      end_date: endDate.toISOString(),
      source,
    },
  });
  return response.data;
};

export const fetchReviewMetrics = async (startDate, endDate, platform) => {
  const response = await api.get('/analytics/reviews', {
    params: {
      start_date: startDate.toISOString(),
      end_date: endDate.toISOString(),
      platform,
    },
  });
  return response.data;
};

export const fetchReferralMetrics = async (startDate, endDate) => {
  const response = await api.get('/analytics/referrals', {
    params: {
      start_date: startDate.toISOString(),
      end_date: endDate.toISOString(),
    },
  });
  return response.data;
};

export const fetchContentMetrics = async (startDate, endDate, contentType) => {
  const response = await api.get('/analytics/content', {
    params: {
      start_date: startDate.toISOString(),
      end_date: endDate.toISOString(),
      content_type: contentType,
    },
  });
  return response.data;
};

export const fetchRecentActivity = async (limit = 10) => {
  const response = await api.get('/analytics/activity', {
    params: { limit },
  });
  return response.data;
};

export const trackLeadMetric = async (leadId, status, source) => {
  const response = await api.post('/analytics/track/lead', null, {
    params: { lead_id: leadId, status, source },
  });
  return response.data;
};

export const trackReviewMetric = async (customerId, status, platform, rating) => {
  const response = await api.post('/analytics/track/review', null, {
    params: { customer_id: customerId, status, platform, rating },
  });
  return response.data;
};

export const trackReferralMetric = async (referralId, status, customerId, referredLeadId) => {
  const response = await api.post('/analytics/track/referral', null, {
    params: {
      referral_id: referralId,
      status,
      customer_id: customerId,
      referred_lead_id: referredLeadId,
    },
  });
  return response.data;
};

export const trackContentMetric = async (contentId, status, contentType, platform) => {
  const response = await api.post('/analytics/track/content', null, {
    params: {
      content_id: contentId,
      status,
      content_type: contentType,
      platform,
    },
  });
  return response.data;
};

export const trackContentEngagement = async (contentId, engagementType, value, platform, metadata) => {
  const response = await api.post('/analytics/track/content/engagement', metadata, {
    params: {
      content_id: contentId,
      engagement_type: engagementType,
      value,
      platform,
    },
  });
  return response.data;
};

export default api;

