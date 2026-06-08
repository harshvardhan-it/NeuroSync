import {
  createContext,
  useContext,
  useState,
  useEffect,
} from "react";

import {
  loginUser,
  registerUser,
  getCurrentUser,
} from "../api/client";

const AuthContext = createContext();

export function AuthProvider({
  children,
}) {
  const [user, setUser] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const token =
      localStorage.getItem(
        "neurosync_token"
      );

    if (token) {
      getCurrentUser()
        .then((res) =>
          setUser(res.data)
        )
        .catch(() =>
          localStorage.removeItem(
            "neurosync_token"
          )
        )
        .finally(() =>
          setLoading(false)
        );
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (
    email,
    password
  ) => {
    const res =
      await loginUser({
        email,
        password,
      });

    localStorage.setItem(
      "neurosync_token",
      res.data.access_token
    );

    const me =
      await getCurrentUser();

    setUser(me.data);
  };

  const register = async (
    name,
    email,
    password
  ) => {
    const res =
      await registerUser({
        name,
        email,
        password,
      });

    localStorage.setItem(
      "neurosync_token",
      res.data.access_token
    );

    const me =
      await getCurrentUser();

    setUser(me.data);
  };

  const logout = () => {
    localStorage.removeItem(
      "neurosync_token"
    );

    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () =>
  useContext(AuthContext);