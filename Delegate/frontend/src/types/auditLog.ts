export interface AuditLog {
  id: string;
  entityType: string;
  entityId: string;
  action: string;
  userId: string;
  userEmail: string;
  timestamp: string;
  details: Record<string, unknown>;
} 