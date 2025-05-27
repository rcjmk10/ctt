export interface OOOSetting {
  id: string;
  userId: string;
  message: string;
  startDate: string;
  endDate: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Delegation {
  id: string;
  delegatorId: string;
  delegateId: string;
  startDate: string;
  endDate: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AuditLog {
  id: string;
  entityType: string;
  entityId: string;
  action: string;
  actorId: string;
  timestamp: string;
  details: string;
}

export interface User {
  id: string;
  email: string;
  displayName: string;
  roles: string[];
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
} 