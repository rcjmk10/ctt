import axios from 'axios';
import type { ApiResponse, OOOSetting, Delegation, AuditLog } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// OOO Settings API
export const oooSettingsApi = {
  getMySettings: () => api.get<ApiResponse<OOOSetting[]>>('/ooo-settings/my'),
  getMyActiveSettings: () => api.get<ApiResponse<OOOSetting[]>>('/ooo-settings/my/active'),
  getUserSettings: (userId: string) => api.get<ApiResponse<OOOSetting[]>>(`/ooo-settings/user/${userId}`),
  createSetting: (data: Partial<OOOSetting>) => api.post<ApiResponse<OOOSetting>>('/ooo-settings', data),
  updateSetting: (id: string, data: Partial<OOOSetting>) => api.put<ApiResponse<OOOSetting>>(`/ooo-settings/${id}`, data),
  deleteSetting: (id: string) => api.delete<ApiResponse<void>>(`/ooo-settings/${id}`),
};

// Delegations API
export const delegationsApi = {
  getMyDelegations: () => api.get<ApiResponse<Delegation[]>>('/delegations/my'),
  getMyActiveDelegations: () => api.get<ApiResponse<Delegation[]>>('/delegations/my/active'),
  getDelegationsToMe: () => api.get<ApiResponse<Delegation[]>>('/delegations/to-me'),
  getUserDelegations: (userId: string) => api.get<ApiResponse<Delegation[]>>(`/delegations/user/${userId}`),
  createDelegation: (data: Partial<Delegation>) => api.post<ApiResponse<Delegation>>('/delegations', data),
  updateDelegation: (id: string, data: Partial<Delegation>) => api.put<ApiResponse<Delegation>>(`/delegations/${id}`, data),
  deleteDelegation: (id: string) => api.delete<ApiResponse<void>>(`/delegations/${id}`),
};

// Audit Logs API
export const auditLogsApi = {
  getEntityLogs: (entityType: string, entityId: string) => 
    api.get<ApiResponse<AuditLog[]>>(`/audit-logs/entity/${entityType}/${entityId}`),
  getActorLogs: (actorId: string) => 
    api.get<ApiResponse<AuditLog[]>>(`/audit-logs/actor/${actorId}`),
  getLogsByTimeRange: (start: string, end: string) => 
    api.get<ApiResponse<AuditLog[]>>(`/audit-logs/time-range?start=${start}&end=${end}`),
  getEntityLogsByTimeRange: (entityType: string, start: string, end: string) => 
    api.get<ApiResponse<AuditLog[]>>(`/audit-logs/entity/${entityType}/time-range?start=${start}&end=${end}`),
};

export default api; 