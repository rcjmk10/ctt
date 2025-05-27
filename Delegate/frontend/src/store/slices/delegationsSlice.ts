import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { delegationsService } from '../../services/delegationsService';
import type { Delegation } from '../../types/delegation';
import type { DelegationsState } from '../../types/store';

const initialState: DelegationsState = {
  delegations: [],
  loading: false,
  error: null,
};

export const fetchDelegations = createAsyncThunk(
  'delegations/fetchDelegations',
  async () => {
    return await delegationsService.getDelegations();
  }
);

export const createDelegation = createAsyncThunk(
  'delegations/createDelegation',
  async (delegation: Omit<Delegation, 'id'>) => {
    return await delegationsService.createDelegation(delegation);
  }
);

export const updateDelegation = createAsyncThunk(
  'delegations/updateDelegation',
  async ({ id, delegation }: { id: string; delegation: Partial<Delegation> }) => {
    return await delegationsService.updateDelegation(id, delegation);
  }
);

export const deleteDelegation = createAsyncThunk(
  'delegations/deleteDelegation',
  async (id: string) => {
    await delegationsService.deleteDelegation(id);
    return id;
  }
);

const delegationsSlice = createSlice({
  name: 'delegations',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fetch Delegations
      .addCase(fetchDelegations.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDelegations.fulfilled, (state, action) => {
        state.loading = false;
        state.delegations = action.payload;
      })
      .addCase(fetchDelegations.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch delegations';
      })
      // Create Delegation
      .addCase(createDelegation.fulfilled, (state, action) => {
        state.delegations.push(action.payload);
      })
      // Update Delegation
      .addCase(updateDelegation.fulfilled, (state, action) => {
        const index = state.delegations.findIndex((d: Delegation) => d.id === action.payload.id);
        if (index !== -1) {
          state.delegations[index] = action.payload;
        }
      })
      // Delete Delegation
      .addCase(deleteDelegation.fulfilled, (state, action) => {
        state.delegations = state.delegations.filter((d: Delegation) => d.id !== action.payload);
      });
  },
});

export const delegationsReducer = delegationsSlice.reducer; 