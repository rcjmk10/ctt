import { useState, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';

interface UserSettings {
  notificationsEnabled: boolean;
  emailNotificationsEnabled: boolean;
  darkModeEnabled: boolean;
}

const DEFAULT_SETTINGS: UserSettings = {
  notificationsEnabled: true,
  emailNotificationsEnabled: true,
  darkModeEnabled: false,
};

export const useSettings = () => {
  const queryClient = useQueryClient();
  const [settings, setSettings] = useState<UserSettings>(() => {
    const savedSettings = localStorage.getItem('userSettings');
    return savedSettings ? JSON.parse(savedSettings) : DEFAULT_SETTINGS;
  });

  useEffect(() => {
    localStorage.setItem('userSettings', JSON.stringify(settings));
  }, [settings]);

  const updateSettings = useMutation({
    mutationFn: async (newSettings: Partial<UserSettings>) => {
      // TODO: Implement settings update API
      return newSettings;
    },
    onSuccess: (newSettings) => {
      setSettings((prev) => ({ ...prev, ...newSettings }));
      queryClient.invalidateQueries({ queryKey: ['user', 'me'] });
    },
  });

  const toggleNotifications = () => {
    setSettings((prev) => ({
      ...prev,
      notificationsEnabled: !prev.notificationsEnabled,
      emailNotificationsEnabled: !prev.notificationsEnabled ? false : prev.emailNotificationsEnabled,
    }));
  };

  const toggleEmailNotifications = () => {
    setSettings((prev) => ({
      ...prev,
      emailNotificationsEnabled: !prev.emailNotificationsEnabled,
    }));
  };

  const toggleDarkMode = () => {
    setSettings((prev) => ({
      ...prev,
      darkModeEnabled: !prev.darkModeEnabled,
    }));
  };

  return {
    settings,
    updateSettings,
    toggleNotifications,
    toggleEmailNotifications,
    toggleDarkMode,
  };
}; 