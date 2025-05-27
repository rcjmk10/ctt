import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControlLabel,
  Switch,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useState } from 'react';
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import {
  fetchDelegations,
  createDelegation,
  updateDelegation,
  deleteDelegation,
} from '../store/slices/delegationsSlice';
import type { Delegation } from '../types/delegation';
import type { RootState } from '../types/store';

interface DelegationFormData {
  delegateId: string;
  startDate: string;
  endDate: string;
  status: 'active' | 'pending' | 'expired';
}

const initialFormData: DelegationFormData = {
  delegateId: '',
  startDate: '',
  endDate: '',
  status: 'active',
};

export const DelegationsPage = () => {
  const dispatch = useAppDispatch();
  const { delegations, loading, error } = useAppSelector((state: RootState) => state.delegations);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingDelegation, setEditingDelegation] = useState<Delegation | null>(null);
  const [formData, setFormData] = useState<DelegationFormData>(initialFormData);

  const handleOpenDialog = (delegation?: Delegation) => {
    if (delegation) {
      setEditingDelegation(delegation);
      setFormData({
        delegateId: delegation.delegateId,
        startDate: delegation.startDate,
        endDate: delegation.endDate,
        status: delegation.status,
      });
    } else {
      setEditingDelegation(null);
      setFormData(initialFormData);
    }
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingDelegation(null);
    setFormData(initialFormData);
  };

  const handleSubmit = async () => {
    try {
      if (editingDelegation) {
        await dispatch(updateDelegation({
          id: editingDelegation.id,
          delegation: formData,
        })).unwrap();
      } else {
        const now = new Date().toISOString();
        await dispatch(createDelegation({
          ...formData,
          delegatorId: 'current-user-id', // This should come from auth context
          createdAt: now,
          updatedAt: now,
        })).unwrap();
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Failed to save delegation:', error);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this delegation?')) {
      try {
        await dispatch(deleteDelegation(id)).unwrap();
      } catch (error) {
        console.error('Failed to delete delegation:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Delegations</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Delegation
        </Button>
      </Box>

      {loading ? (
        <Typography>Loading...</Typography>
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <Box>
          {delegations.map((delegation) => (
            <Card key={delegation.id} sx={{ mb: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Box>
                    <Typography variant="h6">
                      {delegation.delegateId}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      {new Date(delegation.startDate).toLocaleDateString()} - {new Date(delegation.endDate).toLocaleDateString()}
                    </Typography>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={delegation.status === 'active'}
                          onChange={() => handleOpenDialog(delegation)}
                        />
                      }
                      label="Active"
                    />
                  </Box>
                  <Box>
                    <IconButton onClick={() => handleOpenDialog(delegation)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton onClick={() => handleDelete(delegation.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          ))}
          {delegations.length === 0 && (
            <Typography>No delegations found.</Typography>
          )}
        </Box>
      )}

      <Dialog open={isDialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingDelegation ? 'Edit Delegation' : 'Add Delegation'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              label="Delegate ID"
              value={formData.delegateId}
              onChange={(e) => setFormData({ ...formData, delegateId: e.target.value })}
              fullWidth
            />
            <TextField
              label="Start Date"
              type="date"
              value={formData.startDate}
              onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
            <TextField
              label="End Date"
              type="date"
              value={formData.endDate}
              onChange={(e) => setFormData({ ...formData, endDate: e.target.value })}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
            <FormControlLabel
              control={
                <Switch
                  checked={formData.status === 'active'}
                  onChange={(e) => setFormData({
                    ...formData,
                    status: e.target.checked ? 'active' : 'expired',
                  })}
                />
              }
              label="Active"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingDelegation ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}; 