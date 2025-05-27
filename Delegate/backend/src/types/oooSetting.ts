export interface OOOSetting {
  id: string;
  userId: string;
  startDate: string;
  endDate: string;
  message: string;
  status: 'active' | 'pending' | 'expired';
  createdAt: string;
  updatedAt: string;
} 