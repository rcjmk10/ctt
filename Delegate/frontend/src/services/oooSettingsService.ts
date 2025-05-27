import api from './api';
import type { OOOSetting } from '../types/oooSetting';

export const oooSettingsService = {
  async getOOOSettings(): Promise<OOOSetting[]> {
    const response = await api.get('/ooo-settings');
    return response.data;
  },

  async createOOOSetting(setting: Omit<OOOSetting, 'id'>): Promise<OOOSetting> {
    const response = await api.post('/ooo-settings', setting);
    return response.data;
  },

  async updateOOOSetting(id: string, setting: Partial<OOOSetting>): Promise<OOOSetting> {
    const response = await api.put(`/ooo-settings/${id}`, setting);
    return response.data;
  },

  async deleteOOOSetting(id: string): Promise<void> {
    await api.delete(`/ooo-settings/${id}`);
  },
}; 