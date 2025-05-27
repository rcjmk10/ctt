import { useCallback } from 'react';
import { useSnackbar } from 'notistack';

export const useApiError = () => {
  const { enqueueSnackbar } = useSnackbar();

  const handleError = useCallback((error: any) => {
    const message = error.response?.data?.message || error.message || 'An error occurred';
    enqueueSnackbar(message, { variant: 'error' });
  }, [enqueueSnackbar]);

  return { handleError };
}; 