import { useQuery } from '@tanstack/react-query';
import { auditLogsApi } from '../services/api';
import type { AuditLog } from '../types';

export const useAuditLogs = () => {
  const getEntityLogs = (entityType: string, entityId: string) => {
    return useQuery({
      queryKey: ['audit-logs', 'entity', entityType, entityId],
      queryFn: async () => {
        const response = await auditLogsApi.getEntityLogs(entityType, entityId);
        return response.data.data;
      },
    });
  };

  const getActorLogs = (actorId: string) => {
    return useQuery({
      queryKey: ['audit-logs', 'actor', actorId],
      queryFn: async () => {
        const response = await auditLogsApi.getActorLogs(actorId);
        return response.data.data;
      },
    });
  };

  const getLogsByTimeRange = (start: string, end: string) => {
    return useQuery({
      queryKey: ['audit-logs', 'time-range', start, end],
      queryFn: async () => {
        const response = await auditLogsApi.getLogsByTimeRange(start, end);
        return response.data.data;
      },
    });
  };

  const getEntityLogsByTimeRange = (entityType: string, start: string, end: string) => {
    return useQuery({
      queryKey: ['audit-logs', 'entity', entityType, 'time-range', start, end],
      queryFn: async () => {
        const response = await auditLogsApi.getEntityLogsByTimeRange(entityType, start, end);
        return response.data.data;
      },
    });
  };

  return {
    getEntityLogs,
    getActorLogs,
    getLogsByTimeRange,
    getEntityLogsByTimeRange,
  };
}; 