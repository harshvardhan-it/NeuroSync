import { useState } from "react";
import { useAuth } from "../../context/AuthContext";

export default function AuthPage() {
const [mode, setMode] = useState("login");

const [name, setName] = useState("");
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");

const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

const { login, register } = useAuth();

const handleSubmit = async () => {
setLoading(true);
setError("");

```
try {
  if (mode === "login") {
    await login(email, password);
  } else {
    await register(name, email, password);
  }
} catch (err) {
  setError(
    err?.response?.data?.detail ||
      "Something went wrong"
  );
} finally {
  setLoading(false);
}
```

};

return ( <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[var(--bg-base)]">
{/* Background Glows */}
<div
className="absolute inset-0"
style={{
background: `             radial-gradient(
              ellipse 55% 45% at 28% 38%,
              rgba(34,211,238,0.18),
              transparent
            ),
            radial-gradient(
              ellipse 45% 50% at 74% 66%,
              rgba(167,139,250,0.10),
              transparent
            )
          `,
}}
/>
<div
  className="absolute w-[600px] h-[600px] rounded-full blur-[120px]"
  style={{
    background:
      "rgba(34,211,238,0.08)",
  }}
/>
```
  {/* Auth Card */}
  <div
    className="relative z-10 animate-fadeUp w-[400px] rounded-2xl p-8"
    style={{
      background: "rgba(255,255,255,0.028)",
      border: "1px solid rgba(255,255,255,0.07)",
      backdropFilter: "blur(24px)",
    }}
  >
    {/* Logo */}
    <div className="flex flex-col items-center mb-8">
      <div
        className="w-[34px] h-[34px] rounded-[9px] flex items-center justify-center mb-4 text-black font-bold"
        style={{
          background:
            "linear-gradient(135deg,#22d3ee,#a78bfa)",
        }}
      >
        ⬡
      </div>

      <h1 className="font-display font-extrabold text-[21px] text-[var(--text-primary)]">
        NeuroSync{" "}
        <span style={{ color: "var(--cyan)" }}>
          AI
        </span>
      </h1>

      <p
        className="mt-2 text-center text-[12px]"
        style={{
          color: "var(--text-secondary)",
        }}
      >
        Productivity analytics,
        powered by AI
      </p>
    </div>

    {/* Tabs */}
    <div
      className="flex p-1 rounded-lg mb-6"
      style={{
        background:
          "rgba(255,255,255,0.04)",
      }}
    >
      <button
        onClick={() => setMode("login")}
        className="flex-1 py-2 rounded-md text-sm transition-all"
        style={{
          background:
            mode === "login"
              ? "rgba(255,255,255,0.08)"
              : "transparent",
          color:
            mode === "login"
              ? "var(--text-primary)"
              : "var(--text-secondary)",
        }}
      >
        Sign In
      </button>

      <button
        onClick={() => setMode("register")}
        className="flex-1 py-2 rounded-md text-sm transition-all"
        style={{
          background:
            mode === "register"
              ? "rgba(255,255,255,0.08)"
              : "transparent",
          color:
            mode === "register"
              ? "var(--text-primary)"
              : "var(--text-secondary)",
        }}
      >
        Create Account
      </button>
    </div>

    {/* Register Name */}
    {mode === "register" && (
      <div className="mb-4">
        <label
          className="block mb-2 text-[11px] font-medium"
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          Full Name
        </label>

        <input
          type="text"
          value={name}
          onChange={(e) =>
            setName(e.target.value)
          }
          placeholder="Enter your name"
          className="w-full px-4 py-3 rounded-lg text-sm outline-none"
          style={{
            background:
              "rgba(255,255,255,0.05)",
            border:
              "1px solid rgba(255,255,255,0.07)",
            color:
              "var(--text-primary)",
          }}
        />
      </div>
    )}

    {/* Email */}
    <div className="mb-4">
      <label
        className="block mb-2 text-[11px] font-medium"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Email Address
      </label>

      <input
        type="email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
        placeholder="Enter your email"
        className="w-full px-4 py-3 rounded-lg text-sm outline-none"
        style={{
          background:
            "rgba(255,255,255,0.05)",
          border:
            "1px solid rgba(255,255,255,0.07)",
          color:
            "var(--text-primary)",
        }}
      />
    </div>

    {/* Password */}
    <div className="mb-5">
      <label
        className="block mb-2 text-[11px] font-medium"
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        Password
      </label>

      <input
        type="password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
        placeholder="Enter your password"
        className="w-full px-4 py-3 rounded-lg text-sm outline-none"
        style={{
          background:
            "rgba(255,255,255,0.05)",
          border:
            "1px solid rgba(255,255,255,0.07)",
          color:
            "var(--text-primary)",
        }}
      />
    </div>

    {/* Error */}
    {error && (
      <div
        className="mb-4 text-sm"
        style={{
          color:
            "var(--danger)",
        }}
      >
        {error}
      </div>
    )}

    {/* CTA */}
    <button
      onClick={handleSubmit}
      disabled={loading}
      className="w-full py-3 rounded-lg font-display font-bold text-sm transition-all"
      style={{
        background:
          "linear-gradient(135deg,#22d3eedd,#a78bfadd)",
        color: "#ffffff",
        opacity: loading ? 0.7 : 1,
        cursor:
          loading
            ? "not-allowed"
            : "pointer",
      }}
    >
      {loading
        ? "Loading..."
        : "Enter Dashboard →"}
    </button>

    {/* Footer */}
    <p
      className="text-center mt-6 text-[11px]"
      style={{
        color: "var(--text-muted)",
      }}
    >
      Portfolio ·{" "}
      <span
        style={{
          color: "var(--cyan)",
        }}
      >
        Harshvardhan
      </span>{" "}
      · v1.0
    </p>
  </div>
</div>


);
}
