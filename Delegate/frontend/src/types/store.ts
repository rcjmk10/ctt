import type { AuditLog } from './auditLog';
import type { Delegation } from './delegation';
import type { OOOSetting } from './oooSetting';

export interface SettingsState {
  settings: {
    notifications: boolean;
    emailNotifications: boolean;
    darkMode: boolean;
  };
  loading: boolean;
  error: string | null;
}

export interface AuditLogsState {
  logs: AuditLog[];
  loading: boolean;
  error: string | null;
  filters: {
    entityType: string;
    entityId: string;
    startDate: string | null;
    endDate: string | null;
  };
}

export interface OOOSettingsState {
  settings: OOOSetting[];
  loading: boolean;
  error: string | null;
}

export interface DelegationsState {
  delegations: Delegation[];
  loading: boolean;
  error: string | null;
}

export interface RootState {
  settings: SettingsState;
  auditLogs: AuditLogsState;
  oooSettings: OOOSettingsState;
  delegations: DelegationsState;
} 