import { configureStore } from '@reduxjs/toolkit';
import { auditLogsReducer } from './slices/auditLogsSlice';
import { oooSettingsReducer } from './slices/oooSettingsSlice';
import { delegationsReducer } from './slices/delegationsSlice';
import { settingsReducer } from './slices/settingsSlice';
import type { RootState } from '../types/store';

const initialState: RootState = {
  settings: {
    settings: {
      notifications: true,
      emailNotifications: true,
      darkMode: false,
    },
    loading: false,
    error: null,
  },
  auditLogs: {
    logs: [],
    loading: false,
    error: null,
    filters: {
      entityType: '',
      entityId: '',
      startDate: null,
      endDate: null,
    },
  },
  oooSettings: {
    settings: [],
    loading: false,
    error: null,
  },
  delegations: {
    delegations: [],
    loading: false,
    error: null,
  },
};

export const store = configureStore({
  reducer: {
    auditLogs: auditLogsReducer,
    oooSettings: oooSettingsReducer,
    delegations: delegationsReducer,
    settings: settingsReducer,
  },
  preloadedState: initialState,
});

export type AppDispatch = typeof store.dispatch; 