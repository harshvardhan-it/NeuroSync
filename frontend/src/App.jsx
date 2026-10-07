import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";
import AuthPage from "./components/auth/AuthPage";
import WorkspacePage from "./pages/WorkspacePage";
import DashboardPage from "./pages/DashboardPage";
import InsightsPage from "./pages/InsightsPage";
import AnomaliesPage from "./pages/AnomaliesPage";
import ForecastsPage from "./pages/ForecastsPage";
import RiskPage from "./pages/RiskPage";

function FullPageLoader() {
  return (
    <div className="min-h-screen bg-[#06070d] flex items-center justify-center">
      <div
        className="w-10 h-10 rounded-full border-2 border-white/10 border-t-[#E7B75F] animate-spin"
        aria-label="Loading"
      />
    </div>
  );
}

function PrivateRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <FullPageLoader />;
  return user ? children : <Navigate to="/auth" replace />;
}

function PublicRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <FullPageLoader />;
  return !user ? children : <Navigate to="/dashboard" replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route
            path="/auth"
            element={
              <PublicRoute>
                <AuthPage />
              </PublicRoute>
            }
          />
          <Route path="/workspace" element={<PrivateRoute><WorkspacePage /></PrivateRoute>} />
          <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
          <Route path="/insights" element={<PrivateRoute><InsightsPage /></PrivateRoute>} />
          <Route path="/anomalies" element={<PrivateRoute><AnomaliesPage /></PrivateRoute>} />
          <Route path="/forecasts" element={<PrivateRoute><ForecastsPage /></PrivateRoute>} />
          <Route path="/risk" element={<PrivateRoute><RiskPage /></PrivateRoute>} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
