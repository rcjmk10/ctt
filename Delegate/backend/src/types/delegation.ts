export interface Delegation {
  id: string;
  delegatorId: string;
  delegateId: string;
  startDate: string;
  endDate: string;
  status: 'active' | 'pending' | 'expired';
  permissions: string[];
  createdAt: string;
  updatedAt: string;
} 