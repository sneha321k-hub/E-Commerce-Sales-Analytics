import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import AppShell from './components/AppShell'
import ProtectedRoute from './components/ProtectedRoute'
import SalesOverviewPage from './pages/SalesOverviewPage'
import ProductAnalyticsPage from './pages/ProductAnalyticsPage'
import CustomerAnalyticsPage from './pages/CustomerAnalyticsPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <AppShell />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/sales" replace />} />
          <Route path="sales" element={<SalesOverviewPage />} />
          <Route path="products" element={<ProductAnalyticsPage />} />
          <Route path="customers" element={<CustomerAnalyticsPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/sales" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
