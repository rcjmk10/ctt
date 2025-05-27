import api from './api';
import type { SettingsState } from '../types/store';

export const settingsService = {
  async getSettings(): Promise<SettingsState['settings']> {
    const response = await api.get('/settings');
    return response.data;
  },

  async updateSettings(settings: Partial<SettingsState['settings']>): Promise<SettingsState['settings']> {
    const response = await api.put('/settings', settings);
    return response.data;
  },
}; 