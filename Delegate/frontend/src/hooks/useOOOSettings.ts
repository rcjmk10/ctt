import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { oooSettingsApi } from '../services/api';
import type { OOOSetting } from '../types';

export const useOOOSettings = () => {
  const queryClient = useQueryClient();

  const mySettings = useQuery({
    queryKey: ['ooo-settings', 'my'],
    queryFn: async () => {
      const response = await oooSettingsApi.getMySettings();
      return response.data.data;
    },
  });

  const myActiveSettings = useQuery({
    queryKey: ['ooo-settings', 'my', 'active'],
    queryFn: async () => {
      const response = await oooSettingsApi.getMyActiveSettings();
      return response.data.data;
    },
  });

  const createSetting = useMutation({
    mutationFn: async (data: Partial<OOOSetting>) => {
      const response = await oooSettingsApi.createSetting(data);
      return response.data.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ooo-settings'] });
    },
  });

  const updateSetting = useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<OOOSetting> }) => {
      const response = await oooSettingsApi.updateSetting(id, data);
      return response.data.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ooo-settings'] });
    },
  });

  const deleteSetting = useMutation({
    mutationFn: async (id: string) => {
      await oooSettingsApi.deleteSetting(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ooo-settings'] });
    },
  });

  return {
    mySettings,
    myActiveSettings,
    createSetting,
    updateSetting,
    deleteSetting,
  };
}; 