import api from './api';

/**
 * Service for workflow-related API operations
 */
class WorkflowService {
  /**
   * Get all workflow configurations with pagination and filtering
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Paginated workflow configs data
   */
  async getWorkflowConfigs(params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add pagination params
    if (params.page) queryParams.append('page', params.page);
    if (params.per_page) queryParams.append('per_page', params.per_page);
    
    // Add filter params
    if (params.workflow_type) queryParams.append('workflow_type', params.workflow_type);
    if (params.active !== undefined) queryParams.append('active', params.active);
    
    const queryString = queryParams.toString();
    const endpoint = `/workflows/configs${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
  
  /**
   * Get a workflow configuration by ID
   * @param {string} configId - Workflow config ID
   * @returns {Promise<Object>} - Workflow config data
   */
  async getWorkflowConfig(configId) {
    return api.get(`/workflows/configs/${configId}`);
  }
  
  /**
   * Create a new workflow configuration
   * @param {Object} configData - Workflow config data
   * @returns {Promise<Object>} - Created workflow config
   */
  async createWorkflowConfig(configData) {
    return api.post('/workflows/configs', configData);
  }
  
  /**
   * Update a workflow configuration
   * @param {string} configId - Workflow config ID
   * @param {Object} configData - Workflow config data to update
   * @returns {Promise<Object>} - Updated workflow config
   */
  async updateWorkflowConfig(configId, configData) {
    return api.patch(`/workflows/configs/${configId}`, configData);
  }
  
  /**
   * Delete a workflow configuration
   * @param {string} configId - Workflow config ID
   * @returns {Promise<void>}
   */
  async deleteWorkflowConfig(configId) {
    return api.delete(`/workflows/configs/${configId}`);
  }
  
  /**
   * Get all workflow runs with pagination and filtering
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Paginated workflow runs data
   */
  async getWorkflowRuns(params = {}) {
    const queryParams = new URLSearchParams();
    
    // Add pagination params
    if (params.page) queryParams.append('page', params.page);
    if (params.per_page) queryParams.append('per_page', params.per_page);
    
    // Add sorting params
    if (params.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params.sort_dir) queryParams.append('sort_dir', params.sort_dir);
    
    // Add filter params
    if (params.workflow_config_id) queryParams.append('workflow_config_id', params.workflow_config_id);
    if (params.status) queryParams.append('status', params.status);
    
    const queryString = queryParams.toString();
    const endpoint = `/workflows/runs${queryString ? `?${queryString}` : ''}`;
    
    return api.get(endpoint);
  }
  
  /**
   * Get a workflow run by ID
   * @param {string} runId - Workflow run ID
   * @returns {Promise<Object>} - Workflow run data
   */
  async getWorkflowRun(runId) {
    return api.get(`/workflows/runs/${runId}`);
  }
  
  /**
   * Trigger a workflow run manually
   * @param {string} workflowConfigId - Workflow config ID
   * @param {string} entityId - Entity ID (e.g., lead_id)
   * @returns {Promise<Object>} - Created workflow run
   */
  async triggerWorkflowRun(workflowConfigId, entityId) {
    const queryParams = new URLSearchParams({
      workflow_config_id: workflowConfigId,
      entity_id: entityId
    });
    
    return api.post(`/workflows/runs/trigger?${queryParams.toString()}`);
  }
}

// Create and export workflow service instance
const workflowService = new WorkflowService();
export default workflowService;

