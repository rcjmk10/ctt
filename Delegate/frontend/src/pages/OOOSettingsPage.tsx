import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Switch,
  FormControlLabel,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useState } from 'react';
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import {
  fetchOOOSettings,
  createOOOSetting,
  updateOOOSetting,
  deleteOOOSetting,
} from '../store/slices/oooSettingsSlice';
import type { OOOSetting } from '../types/oooSetting';
import type { RootState } from '../types/store';

interface OOOSettingFormData {
  startDate: string;
  endDate: string;
  message: string;
  status: 'active' | 'pending' | 'expired';
}

const initialFormData: OOOSettingFormData = {
  startDate: '',
  endDate: '',
  message: '',
  status: 'active',
};

export const OOOSettingsPage = () => {
  const dispatch = useAppDispatch();
  const { settings, loading, error } = useAppSelector((state: RootState) => state.oooSettings);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingSetting, setEditingSetting] = useState<OOOSetting | null>(null);
  const [formData, setFormData] = useState<OOOSettingFormData>(initialFormData);

  const handleOpenDialog = (setting?: OOOSetting) => {
    if (setting) {
      setEditingSetting(setting);
      setFormData({
        startDate: setting.startDate,
        endDate: setting.endDate,
        message: setting.message,
        status: setting.status,
      });
    } else {
      setEditingSetting(null);
      setFormData(initialFormData);
    }
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingSetting(null);
    setFormData(initialFormData);
  };

  const handleSubmit = async () => {
    try {
      if (editingSetting) {
        await dispatch(updateOOOSetting({
          id: editingSetting.id,
          setting: formData,
        })).unwrap();
      } else {
        const now = new Date().toISOString();
        await dispatch(createOOOSetting({
          ...formData,
          userId: 'current-user-id', // This should come from auth context
          createdAt: now,
          updatedAt: now,
        })).unwrap();
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Failed to save OOO setting:', error);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this OOO setting?')) {
      try {
        await dispatch(deleteOOOSetting(id)).unwrap();
      } catch (error) {
        console.error('Failed to delete OOO setting:', error);
      }
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Out of Office Settings</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add OOO Setting
        </Button>
      </Box>

      {loading ? (
        <Typography>Loading...</Typography>
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <Box>
          {settings.map((setting) => (
            <Card key={setting.id} sx={{ mb: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Box>
                    <Typography variant="h6">
                      {new Date(setting.startDate).toLocaleDateString()} - {new Date(setting.endDate).toLocaleDateString()}
                    </Typography>
                    <Typography variant="body1" sx={{ mt: 1 }}>
                      {setting.message}
                    </Typography>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={setting.status === 'active'}
                          onChange={() => handleOpenDialog(setting)}
                        />
                      }
                      label="Enabled"
                    />
                  </Box>
                  <Box>
                    <IconButton onClick={() => handleOpenDialog(setting)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton onClick={() => handleDelete(setting.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          ))}
          {settings.length === 0 && (
            <Typography>No OOO settings found.</Typography>
          )}
        </Box>
      )}

      <Dialog open={isDialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingSetting ? 'Edit OOO Setting' : 'Add OOO Setting'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
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
            <TextField
              label="Message"
              multiline
              rows={4}
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
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
              label="Enabled"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingSetting ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}; 