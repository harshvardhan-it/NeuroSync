import {
BrowserRouter,
Routes,
Route,
Navigate,
} from "react-router-dom";

import {
AuthProvider,
useAuth,
} from "./context/AuthContext";

import AuthPage from "./components/auth/AuthPage";
import DashboardPage from "./pages/DashboardPage";
import InsightsPage from "./pages/InsightsPage";
import AnomaliesPage from "./pages/AnomaliesPage";
import ForecastsPage from "./pages/ForecastsPage";

function FullPageLoader() {
return (
<div
style={{
minHeight: "100vh",
background: "#06070d",
display: "flex",
alignItems: "center",
justifyContent: "center",
}}
>
<div
style={{
width: 40,
height: 40,
borderRadius: "50%",
border:
"2px solid rgba(255,255,255,0.08)",
borderTop:
"2px solid #22d3ee",
animation:
"spin 1s linear infinite",
}}
/> </div>
);
}

function PrivateRoute({
children,
}) {
const {
user,
loading,
} = useAuth();

if (loading) {
return <FullPageLoader />;
}

return user ? (
children
) : ( <Navigate
   to="/auth"
   replace
 />
);
}

function PublicRoute({
children,
}) {
const {
user,
loading,
} = useAuth();

if (loading) {
return <FullPageLoader />;
}

return !user ? (
children
) : ( <Navigate
   to="/dashboard"
   replace
 />
);
}

export default function App() {
return ( <AuthProvider> <BrowserRouter> <Routes>

```
      <Route
        path="/auth"
        element={
          <PublicRoute>
            <AuthPage />
          </PublicRoute>
        }
      />

      <Route
        path="/dashboard"
        element={<DashboardPage />}
      />

      <Route
        path="/insights"
        element={<InsightsPage />}
      />

      <Route
        path="/anomalies"
        element={<AnomaliesPage />}
      />
      <Route
        path="/forecasts"
        element={<ForecastsPage />}
      />

      <Route
        path="*"
        element={
          <Navigate
            to="/auth"
            replace
          />
        }
      />

    </Routes>
  </BrowserRouter>
</AuthProvider>


);
}
