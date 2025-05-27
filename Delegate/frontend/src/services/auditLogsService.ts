import api from './api';
import type { AuditLog } from '../types/auditLog';

export interface AuditLogFilters {
  entityType: string;
  entityId: string;
  startDate: string | null;
  endDate: string | null;
}

export const auditLogsService = {
  async getAuditLogs(filters: AuditLogFilters): Promise<AuditLog[]> {
    const params = new URLSearchParams();
    if (filters.entityType) params.append('entityType', filters.entityType);
    if (filters.entityId) params.append('entityId', filters.entityId);
    if (filters.startDate) params.append('startDate', filters.startDate);
    if (filters.endDate) params.append('endDate', filters.endDate);

    const response = await api.get(`/audit-logs?${params.toString()}`);
    return response.data;
  },
}; 