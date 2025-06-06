import api from './api';

/**
 * Service for lead-related API operations
 */
class LeadService {
  /**
   * Get all leads with pagination and filtering
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Paginated leads data
   */
  async getLeads(params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add pagination params
    if (params.page) queryParams.append('page', params.page);
    if (params.per_page) queryParams.append('per_page', params.per_page);
    
    // Add sorting params
    if (params.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params.sort_dir) queryParams.append('sort_dir', params.sort_dir);
    
    // Add filter params
    if (params.status) queryParams.append('status', params.status);
    if (params.source) queryParams.append('source', params.source);
    
    const queryString = queryParams.toString();
    const endpoint = `/leads${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
  
  /**
   * Get a lead by ID
   * @param {string} leadId - Lead ID
   * @returns {Promise<Object>} - Lead data
   */
  async getLead(leadId) {
    return api.get(`/leads/${leadId}`);
  }
  
  /**
   * Create a new lead
   * @param {Object} leadData - Lead data
   * @returns {Promise<Object>} - Created lead
   */
  async createLead(leadData) {
    return api.post('/leads', leadData);
  }
  
  /**
   * Update a lead
   * @param {string} leadId - Lead ID
   * @param {Object} leadData - Lead data to update
   * @returns {Promise<Object>} - Updated lead
   */
  async updateLead(leadId, leadData) {
    return api.patch(`/leads/${leadId}`, leadData);
  }
  
  /**
   * Delete a lead
   * @param {string} leadId - Lead ID
   * @returns {Promise<void>}
   */
  async deleteLead(leadId) {
    return api.delete(`/leads/${leadId}`);
  }
  
  /**
   * Get interactions for a lead
   * @param {string} leadId - Lead ID
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Paginated interactions data
   */
  async getLeadInteractions(leadId, params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add pagination params
    if (params.page) queryParams.append('page', params.page);
    if (params.per_page) queryParams.append('per_page', params.per_page);
    
    const queryString = queryParams.toString();
    const endpoint = `/leads/${leadId}/interactions${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
  
  /**
   * Create an interaction for a lead
   * @param {string} leadId - Lead ID
   * @param {Object} interactionData - Interaction data
   * @returns {Promise<Object>} - Created interaction
   */
  async createLeadInteraction(leadId, interactionData) {
    return api.post(`/leads/${leadId}/interactions`, interactionData);
  }
}

// Create and export lead service instance
const leadService = new LeadService();
export default leadService;

