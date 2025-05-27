import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  Divider,
} from '@mui/material';
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import { updateSettings } from '../store/slices/settingsSlice';
import type { RootState } from '../types/store';

export const SettingsPage = () => {
  const dispatch = useAppDispatch();
  const { settings, loading, error } = useAppSelector((state: RootState) => state.settings);

  const handleToggleSetting = async (key: keyof typeof settings) => {
    try {
      await dispatch(updateSettings({
        [key]: !settings[key],
      })).unwrap();
    } catch (error) {
      console.error('Failed to update setting:', error);
    }
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Settings
      </Typography>

      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Notifications
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.notifications}
                  onChange={() => handleToggleSetting('notifications')}
                />
              }
              label="Notifications"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.emailNotifications}
                  onChange={() => handleToggleSetting('emailNotifications')}
                  disabled={!settings.notifications}
                />
              }
              label="Email Notifications"
            />
          </Box>
        </CardContent>
      </Card>

      <Divider sx={{ my: 3 }} />

      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Appearance
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.darkMode}
                  onChange={() => handleToggleSetting('darkMode')}
                />
              }
              label="Dark Mode"
            />
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}; 