import { useEffect, useState } from "react";

import {
  loginUser,
  registerUser,
  getCurrentUser,
} from "../api/client";
import { AuthContext } from "./auth-context";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(
    () => Boolean(localStorage.getItem("neurosync_token"))
  );

  useEffect(() => {
    const token = localStorage.getItem("neurosync_token");

    if (!token) {
      return;
    }

    getCurrentUser()
      .then((res) => {
        setUser(res.data.data);
      })
      .catch(() => {
        localStorage.removeItem("neurosync_token");
        localStorage.removeItem("token");
        setUser(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const login = async (email, password) => {
    try {
      const res = await loginUser({ email, password });
      const accessToken = res.data.data.access_token;

      localStorage.setItem("neurosync_token", accessToken);
      localStorage.removeItem("token");

      const me = await getCurrentUser();
      setUser(me.data.data);
    } catch (err) {
      console.error("LOGIN ERROR:", err);
      throw err;
    }
  };

  const register = async (name, email, password) => {
    const res = await registerUser({ name, email, password });
    const accessToken = res.data.data.access_token;

    localStorage.setItem("neurosync_token", accessToken);
    localStorage.removeItem("token");

    const me = await getCurrentUser();
    setUser(me.data.data);
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
    <AuthContext.Provider
      value={{ user, loading, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}
