import { useEffect, useState } from "react";
import { loginUser, registerUser, getCurrentUser } from "../api/client";
import { AuthContext } from "./authContext";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(() =>
    Boolean(localStorage.getItem("neurosync_token"))
  );

  useEffect(() => {
    const token = localStorage.getItem("neurosync_token");
    if (!token) return undefined;

    let active = true;

    getCurrentUser()
      .then((response) => {
        if (active) setUser(response.data.data);
      })
      .catch(() => {
        localStorage.removeItem("neurosync_token");
        localStorage.removeItem("token");
        if (active) setUser(null);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  const login = async (email, password) => {
    const response = await loginUser({ email, password });
    const accessToken = response.data.data.access_token;

    localStorage.setItem("neurosync_token", accessToken);
    localStorage.removeItem("token");

    const currentUser = await getCurrentUser();
    setUser(currentUser.data.data);
  };

  const register = async (name, email, password) => {
    const response = await registerUser({ name, email, password });
    const accessToken = response.data.data.access_token;

    localStorage.setItem("neurosync_token", accessToken);
    localStorage.removeItem("token");

    const currentUser = await getCurrentUser();
    setUser(currentUser.data.data);
  };

  const logout = () => {
    localStorage.removeItem("neurosync_token");
    localStorage.removeItem("token");
    localStorage.removeItem("dataset_id");
    localStorage.removeItem("dataset_meta");
    setUser(null);
    window.location.href = "/auth";
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
