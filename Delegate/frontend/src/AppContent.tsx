import { Routes, Route, Navigate } from 'react-router-dom';
import { OOOSettingsPage } from './pages/OOOSettingsPage';
import { DelegationsPage } from './pages/DelegationsPage';
import { AuditLogsPage } from './pages/AuditLogsPage';
import { SettingsPage } from './pages/SettingsPage';
import { Layout } from './components/Layout';

export const AppContent = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/ooo-settings" replace />} />
        <Route path="/ooo-settings" element={<OOOSettingsPage />} />
        <Route path="/delegations" element={<DelegationsPage />} />
        <Route path="/audit-logs" element={<AuditLogsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Layout>
  );
}; 