import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { delegationsApi } from '../services/api';
import type { Delegation } from '../types';

export const useDelegations = () => {
  const queryClient = useQueryClient();

  const myDelegations = useQuery({
    queryKey: ['delegations', 'my'],
    queryFn: async () => {
      const response = await delegationsApi.getMyDelegations();
      return response.data.data;
    },
  });

  const myActiveDelegations = useQuery({
    queryKey: ['delegations', 'my', 'active'],
    queryFn: async () => {
      const response = await delegationsApi.getMyActiveDelegations();
      return response.data.data;
    },
  });

  const delegationsToMe = useQuery({
    queryKey: ['delegations', 'to-me'],
    queryFn: async () => {
      const response = await delegationsApi.getDelegationsToMe();
      return response.data.data;
    },
  });

  const createDelegation = useMutation({
    mutationFn: async (data: Partial<Delegation>) => {
      const response = await delegationsApi.createDelegation(data);
      return response.data.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['delegations'] });
    },
  });

  const updateDelegation = useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Delegation> }) => {
      const response = await delegationsApi.updateDelegation(id, data);
      return response.data.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['delegations'] });
    },
  });

  const deleteDelegation = useMutation({
    mutationFn: async (id: string) => {
      await delegationsApi.deleteDelegation(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['delegations'] });
    },
  });

  return {
    myDelegations,
    myActiveDelegations,
    delegationsToMe,
    createDelegation,
    updateDelegation,
    deleteDelegation,
  };
}; 