import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  MenuItem,
  Button,
  Chip,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useEffect } from 'react';
import { useAppDispatch } from '../hooks/useAppDispatch';
import { useAppSelector } from '../hooks/useAppSelector';
import { fetchAuditLogs, setFilters, clearFilters } from '../store/slices/auditLogsSlice';
import type { AuditLog } from '../types/auditLog';
import type { RootState } from '../types/store';

const ENTITY_TYPES = [
  { value: 'USER', label: 'User' },
  { value: 'OOO_SETTING', label: 'OOO Setting' },
  { value: 'DELEGATION', label: 'Delegation' },
];

export const AuditLogsPage = () => {
  const dispatch = useAppDispatch();
  const { logs, filters, loading, error } = useAppSelector((state: RootState) => state.auditLogs);

  useEffect(() => {
    dispatch(fetchAuditLogs(filters));
  }, [dispatch, filters]);

  const handleFilterChange = (field: keyof typeof filters, value: any) => {
    dispatch(setFilters({ ...filters, [field]: value }));
  };

  const handleClearFilters = () => {
    dispatch(clearFilters());
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'CREATE':
        return 'success';
      case 'UPDATE':
        return 'info';
      case 'DELETE':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Audit Logs
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Filters
          </Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 2 }}>
            <Box>
              <TextField
                select
                fullWidth
                label="Entity Type"
                value={filters.entityType}
                onChange={(e) => handleFilterChange('entityType', e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                {ENTITY_TYPES.map((type) => (
                  <MenuItem key={type.value} value={type.value}>
                    {type.label}
                  </MenuItem>
                ))}
              </TextField>
            </Box>
            <Box>
              <TextField
                fullWidth
                label="Entity ID"
                value={filters.entityId}
                onChange={(e) => handleFilterChange('entityId', e.target.value)}
              />
            </Box>
            <Box>
              <DatePicker
                label="Start Date"
                value={filters.startDate ? new Date(filters.startDate) : null}
                onChange={(date) => handleFilterChange('startDate', date?.toISOString() || null)}
                slotProps={{ textField: { fullWidth: true } }}
              />
            </Box>
            <Box>
              <DatePicker
                label="End Date"
                value={filters.endDate ? new Date(filters.endDate) : null}
                onChange={(date) => handleFilterChange('endDate', date?.toISOString() || null)}
                slotProps={{ textField: { fullWidth: true } }}
              />
            </Box>
          </Box>
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
            <Button onClick={handleClearFilters}>Clear Filters</Button>
          </Box>
        </CardContent>
      </Card>

      {loading ? (
        <Typography>Loading...</Typography>
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <Box>
          {logs.map((log: AuditLog) => (
            <Card key={log.id} sx={{ mb: 2 }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="subtitle1">
                    {log.entityType} - {log.entityId}
                  </Typography>
                  <Chip
                    label={log.action}
                    color={getActionColor(log.action) as any}
                    size="small"
                  />
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {new Date(log.timestamp).toLocaleString()}
                </Typography>
                <Typography variant="body2">
                  <strong>Actor ID:</strong> {log.userId}
                </Typography>
                {log.details && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    <strong>Details:</strong> {JSON.stringify(log.details)}
                  </Typography>
                )}
              </CardContent>
            </Card>
          ))}
          {logs.length === 0 && (
            <Typography>No audit logs found.</Typography>
          )}
        </Box>
      )}
    </Box>
  );
}; 