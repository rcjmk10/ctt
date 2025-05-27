import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { oooSettingsService } from '../../services/oooSettingsService';
import type { OOOSetting } from '../../types/oooSetting';
import type { OOOSettingsState } from '../../types/store';

const initialState: OOOSettingsState = {
  settings: [],
  loading: false,
  error: null,
};

export const fetchOOOSettings = createAsyncThunk(
  'oooSettings/fetchOOOSettings',
  async () => {
    return await oooSettingsService.getOOOSettings();
  }
);

export const createOOOSetting = createAsyncThunk(
  'oooSettings/createOOOSetting',
  async (setting: Omit<OOOSetting, 'id'>) => {
    return await oooSettingsService.createOOOSetting(setting);
  }
);

export const updateOOOSetting = createAsyncThunk(
  'oooSettings/updateOOOSetting',
  async ({ id, setting }: { id: string; setting: Partial<OOOSetting> }) => {
    return await oooSettingsService.updateOOOSetting(id, setting);
  }
);

export const deleteOOOSetting = createAsyncThunk(
  'oooSettings/deleteOOOSetting',
  async (id: string) => {
    await oooSettingsService.deleteOOOSetting(id);
    return id;
  }
);

const oooSettingsSlice = createSlice({
  name: 'oooSettings',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fetch OOO Settings
      .addCase(fetchOOOSettings.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchOOOSettings.fulfilled, (state, action) => {
        state.loading = false;
        state.settings = action.payload;
      })
      .addCase(fetchOOOSettings.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch OOO settings';
      })
      // Create OOO Setting
      .addCase(createOOOSetting.fulfilled, (state, action) => {
        state.settings.push(action.payload);
      })
      // Update OOO Setting
      .addCase(updateOOOSetting.fulfilled, (state, action) => {
        const index = state.settings.findIndex((s: OOOSetting) => s.id === action.payload.id);
        if (index !== -1) {
          state.settings[index] = action.payload;
        }
      })
      // Delete OOO Setting
      .addCase(deleteOOOSetting.fulfilled, (state, action) => {
        state.settings = state.settings.filter((s: OOOSetting) => s.id !== action.payload);
      });
  },
});

export const oooSettingsReducer = oooSettingsSlice.reducer; 