import type { OOOSetting } from '../../types/oooSetting';
import type { Delegation } from '../../types/delegation';

export interface EmailProviderService {
  // OOO Settings
  setOOOSetting(userId: string, setting: OOOSetting): Promise<void>;
  clearOOOSetting(userId: string): Promise<void>;
  getOOOSetting(userId: string): Promise<OOOSetting | null>;

  // Delegation
  createDelegation(delegation: Delegation): Promise<void>;
  removeDelegation(delegation: Delegation): Promise<void>;
  updateDelegation(delegation: Delegation): Promise<void>;
  getDelegations(userId: string): Promise<Delegation[]>;
}

export enum EmailProviderType {
  OUTLOOK_365 = 'outlook365',
  GMAIL = 'gmail',
  // Add more providers as needed
} 