import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { auditLogsService, type AuditLogFilters } from '../../services/auditLogsService';
import type { AuditLog } from '../../types/auditLog';
import type { AuditLogsState } from '../../types/store';

const initialState: AuditLogsState = {
  logs: [],
  filters: {
    entityType: '',
    entityId: '',
    startDate: null,
    endDate: null,
  },
  loading: false,
  error: null,
};

export const fetchAuditLogs = createAsyncThunk(
  'auditLogs/fetchAuditLogs',
  async (filters: AuditLogFilters) => {
    return await auditLogsService.getAuditLogs(filters);
  }
);

const auditLogsSlice = createSlice({
  name: 'auditLogs',
  initialState,
  reducers: {
    setFilters: (state, action) => {
      state.filters = action.payload;
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAuditLogs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAuditLogs.fulfilled, (state, action) => {
        state.loading = false;
        state.logs = action.payload;
      })
      .addCase(fetchAuditLogs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch audit logs';
      });
  },
});

export const { setFilters, clearFilters } = auditLogsSlice.actions;
export const auditLogsReducer = auditLogsSlice.reducer; 