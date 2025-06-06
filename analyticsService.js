import api from './api';

/**
 * Service for analytics-related API operations
 */
class AnalyticsService {
  /**
   * Get dashboard analytics data
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Dashboard analytics data
   */
  async getDashboardAnalytics(params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add date range params
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);
    
    // Add comparison param
    if (params.compare_to_previous !== undefined) {
      queryParams.append('compare_to_previous', params.compare_to_previous);
    }
    
    const queryString = queryParams.toString();
    const endpoint = `/analytics/dashboard${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
  
  /**
   * Get workflow analytics data
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Workflow analytics data
   */
  async getWorkflowAnalytics(params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add date range params
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);
    
    // Add filter params
    if (params.workflow_type) queryParams.append('workflow_type', params.workflow_type);
    
    const queryString = queryParams.toString();
    const endpoint = `/analytics/workflows${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
  
  /**
   * Get lead analytics data
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Lead analytics data
   */
  async getLeadAnalytics(params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add date range params
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);
    
    // Add filter params
    if (params.source) queryParams.append('source', params.source);
    
    const queryString = queryParams.toString();
    const endpoint = `/analytics/leads${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
  
  /**
   * Get content analytics data
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Content analytics data
   */
  async getContentAnalytics(params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add date range params
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);
    
    // Add filter params
    if (params.type) queryParams.append('type', params.type);
    
    const queryString = queryParams.toString();
    const endpoint = `/analytics/content${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
}

// Create and export analytics service instance
const analyticsService = new AnalyticsService();
export default analyticsService;

