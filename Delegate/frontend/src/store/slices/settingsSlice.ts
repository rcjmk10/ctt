import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { settingsService } from '../../services/settingsService';
import type { SettingsState } from '../../types/store';

const initialState: SettingsState = {
  settings: {
    notifications: true,
    emailNotifications: true,
    darkMode: false,
  },
  loading: false,
  error: null,
};

export const fetchSettings = createAsyncThunk(
  'settings/fetchSettings',
  async () => {
    return await settingsService.getSettings();
  }
);

export const updateSettings = createAsyncThunk(
  'settings/updateSettings',
  async (settings: Partial<SettingsState['settings']>) => {
    return await settingsService.updateSettings(settings);
  }
);

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    toggleNotifications: (state) => {
      state.settings.notifications = !state.settings.notifications;
    },
    toggleEmailNotifications: (state) => {
      state.settings.emailNotifications = !state.settings.emailNotifications;
    },
    toggleDarkMode: (state) => {
      state.settings.darkMode = !state.settings.darkMode;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Settings
      .addCase(fetchSettings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSettings.fulfilled, (state, action) => {
        state.loading = false;
        state.settings = action.payload;
      })
      .addCase(fetchSettings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch settings';
      })
      // Update Settings
      .addCase(updateSettings.fulfilled, (state, action) => {
        state.settings = { ...state.settings, ...action.payload };
      });
  },
});

export const { toggleNotifications, toggleEmailNotifications, toggleDarkMode } = settingsSlice.actions;
export const settingsReducer = settingsSlice.reducer; 