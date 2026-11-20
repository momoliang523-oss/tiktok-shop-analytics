/**
 * API service for communicating with backend
 */
import axios from 'axios'

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.error('Unauthorized access')
    } else if (error.response?.status === 500) {
      // Handle server error
      console.error('Server error')
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const api = {
  // Health check
  health: () => apiClient.get('/health'),

  // Sales Analytics
  getSalesTrend: (params: any) => apiClient.get('/api/v1/analytics/sales/trend', { params }),
  getSalesRanking: (params: any) => apiClient.get('/api/v1/analytics/sales/ranking', { params }),

  // Products Analytics
  getProductPerformance: (params: any) => apiClient.get('/api/v1/analytics/products/performance', { params }),
  getSkuRanking: (params: any) => apiClient.get('/api/v1/analytics/products/sku-ranking', { params }),
  getProductAssociation: (params: any) => apiClient.get('/api/v1/analytics/products/association', { params }),
  getPatternAnalysis: (params: any) => apiClient.get('/api/v1/analytics/products/pattern-analysis', { params }),
  getSkuInventory: (params: any) => apiClient.get('/api/v1/analytics/products/inventory', { params }),

  // Customers Analytics
  getCustomerSegments: (params: any) => apiClient.get('/api/v1/analytics/customers/segments', { params }),
  getCustomerRfm: (params: any) => apiClient.get('/api/v1/analytics/customers/rfm', { params }),

  // Marketing Analytics
  getCampaigns: (params: any) => apiClient.get('/api/v1/analytics/marketing/campaigns', { params }),
  getRoi: (params: any) => apiClient.get('/api/v1/analytics/marketing/roi', { params }),

  // Live Analytics
  getLiveOverview: (params: any) => apiClient.get('/api/v1/analytics/live/overview', { params }),
  getLiveProducts: (params: any) => apiClient.get('/api/v1/analytics/live/products', { params }),
  getLiveHosts: (params: any) => apiClient.get('/api/v1/analytics/live/hosts', { params }),

  // Traffic Analytics
  getTrafficChannels: (params: any) => apiClient.get('/api/v1/analytics/traffic/channels', { params }),
  getTrafficFunnel: (params: any) => apiClient.get('/api/v1/analytics/traffic/funnel', { params }),
  getLtvCac: (params: any) => apiClient.get('/api/v1/analytics/traffic/ltv-cac', { params }),
  getChannelValue: (params: any) => apiClient.get('/api/v1/analytics/traffic/channel-value', { params }),
  getSegmentation: (params: any) => apiClient.get('/api/v1/analytics/traffic/segmentation', { params }),

  // Advanced Analytics
  getCorrelation: (params: any) => apiClient.get('/api/v1/analytics/advanced/correlation', { params }),
  createClustering: (data: any) => apiClient.post('/api/v1/analytics/advanced/clustering', data),
  getPrediction: (params: any) => apiClient.get('/api/v1/analytics/advanced/prediction', { params }),

  // Reports
  generateReport: (data: any) => apiClient.post('/api/v1/reports/generate', data),
  getReportStatus: (taskId: string) => apiClient.get(`/api/v1/reports/status/${taskId}`),
  downloadReport: (taskId: string) => apiClient.get(`/api/v1/reports/download/${taskId}`, {
    responseType: 'blob',
  }),

  // Data Import
  uploadFile: (formData: FormData) => apiClient.post('/api/v1/data/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getUploadStatus: (uploadId: string) => apiClient.get(`/api/v1/data/upload/${uploadId}`),
}

export default apiClient
