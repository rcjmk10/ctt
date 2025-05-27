import { createTheme } from '@mui/material/styles';
import { useAppSelector } from './useAppSelector';

export function useTheme() {
  const settings = useAppSelector((state) => state.settings.settings);
  const darkMode = settings.darkMode;

  return createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
    },
  });
} 