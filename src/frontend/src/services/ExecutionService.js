import axios from 'axios';

const API_URL = '/api/execution';

/**
 * Service for interacting with the code execution API
 */
class ExecutionService {
  /**
   * Execute code with test cases
   * @param {string} code - The code to execute
   * @param {Array} testCases - Test cases to run
   * @param {string} language - Programming language (default: python)
   * @returns {Promise} - Promise with execution results
   */
  async executeCode(code, testCases, language = 'python') {
    try {
      const response = await axios.post(`${API_URL}/execute`, {
        code,
        test_cases: testCases,
        language
      });
      
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  }
  
  /**
   * Validate code for security issues
   * @param {string} code - The code to validate
   * @param {Array} testCases - Test cases to run (optional)
   * @param {string} language - Programming language (default: python)
   * @returns {Promise} - Promise with validation results
   */
  async validateCode(code, testCases = [], language = 'python') {
    try {
      const response = await axios.post(`${API_URL}/validate`, {
        code,
        test_cases: testCases,
        language
      });
      
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  }
  
  /**
   * Execute a submission
   * @param {number} submissionId - ID of the submission to execute
   * @returns {Promise} - Promise with execution results
   */
  async executeSubmission(submissionId) {
    try {
      const response = await axios.post(`${API_URL}/submissions/${submissionId}/execute`);
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  }
  
  /**
   * Get execution metrics
   * @returns {Promise} - Promise with execution metrics
   */
  async getMetrics() {
    try {
      const response = await axios.get(`${API_URL}/metrics`);
      return response.data;
    } catch (error) {
      throw this._handleError(error);
    }
  }
  
  /**
   * Handle API errors
   * @param {Error} error - The error object
   * @returns {Error} - Processed error with message
   * @private
   */
  _handleError(error) {
    let errorMessage = 'An unexpected error occurred';
    
    if (error.response) {
      // Server responded with error
      const serverError = error.response.data;
      errorMessage = serverError.detail || serverError.message || 'Server error';
    } else if (error.request) {
      // Request made but no response
      errorMessage = 'No response from server. Please check your connection.';
    } else {
      // Error in request setup
      errorMessage = error.message;
    }
    
    return new Error(errorMessage);
  }
}

export default new ExecutionService();