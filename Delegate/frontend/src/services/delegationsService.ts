import api from './api';
import type { Delegation } from '../types/delegation';

export const delegationsService = {
  async getDelegations(): Promise<Delegation[]> {
    const response = await api.get('/delegations');
    return response.data;
  },

  async createDelegation(delegation: Omit<Delegation, 'id'>): Promise<Delegation> {
    const response = await api.post('/delegations', delegation);
    return response.data;
  },

  async updateDelegation(id: string, delegation: Partial<Delegation>): Promise<Delegation> {
    const response = await api.put(`/delegations/${id}`, delegation);
    return response.data;
  },

  async deleteDelegation(id: string): Promise<void> {
    await api.delete(`/delegations/${id}`);
  },
}; 