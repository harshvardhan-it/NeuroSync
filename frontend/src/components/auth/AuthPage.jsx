

import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import AuthScene from "./AuthScene";

export default function AuthPage() {
  const { login, register } = useAuth();

  const [mode, setMode] = useState("login");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
    setError("");

    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register(
          name,
          email,
          password
        );
      }
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
        "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="
        relative
        min-h-screen
        overflow-hidden
        bg-[var(--bg-base)]
        flex
        items-center
        justify-center
        px-6
      "
    >
      <AuthScene />

      <div
        className="
          relative
          z-10
          w-full
          max-w-7xl
          grid
          lg:grid-cols-2
          gap-16
          items-center
        "
      >
        {/* Left Hero */}
        <div
          className="
            hidden
            lg:block
            animate-fadeUp
          "
        >
          <div
            className="
              analysis-label
              mb-6
            "
            style={{
              color:
                "var(--gold-primary)",
            }}
          >
            NEUROSYNC AI
          </div>

          <h1
            className="
              hero-title
              text-7xl
              xl:text-8xl
            "
          >
            <span className="glow-text">
              Think.
            </span>

            <br />

            Analyze.

            <br />

            Decide.
          </h1>

          <p
            className="
              mt-8
              max-w-xl
              text-lg
              leading-8
            "
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Executive intelligence
            powered by AI.
            Transform raw data into
            strategic decisions.
          </p>

          <div
            className="
              mt-12
              flex
              gap-8
            "
          >
            <Metric
              value="AI"
              label="Decision Engine"
            />

            <Metric
              value="24/7"
              label="Analysis"
            />

            <Metric
              value="∞"
              label="Insights"
            />
          </div>
        </div>

        {/* Auth Card */}
        <div
          className="
            animate-fadeUp
            w-full
            max-w-md
            mx-auto
          "
        >
          <div
            className="
              relative
              overflow-hidden
              rounded-[32px]
              p-8
            "
            style={{
              background:
                "rgba(255,255,255,0.03)",

              border:
                "1px solid rgba(255,255,255,0.08)",

              backdropFilter:
                "blur(24px)",

              boxShadow:
                "0 25px 80px rgba(0,0,0,0.35)",
            }}
          >
            {/* Logo */}
            <div
              className="
                flex
                flex-col
                items-center
                mb-8
              "
            >
              <div
                className="
                  w-14
                  h-14
                  rounded-2xl
                  flex
                  items-center
                  justify-center
                  font-bold
                  text-black
                  text-xl
                  mb-5
                "
                style={{
                  background:
                    "linear-gradient(135deg,#E7B75F,#B3264A)",
                }}
              >
                ⬡
              </div>

              <h2
                className="
                  font-display
                  text-3xl
                  font-bold
                "
              >
                NeuroSync AI
              </h2>

              <p
                className="
                  mt-2
                  text-sm
                "
                style={{
                  color:
                    "var(--text-secondary)",
                }}
              >
                Executive Intelligence Platform
              </p>
            </div>

            {/* Tabs */}
            <div
              className="
                flex
                rounded-2xl
                p-1
                mb-8
              "
              style={{
                background:
                  "rgba(255,255,255,0.04)",
              }}
            >
              <button
                onClick={() =>
                  setMode("login")
                }
                className="
                  flex-1
                  py-3
                  rounded-xl
                  transition-all
                  font-medium
                "
                style={{
                  background:
                    mode === "login"
                      ? "linear-gradient(135deg,#E7B75F,#B3264A)"
                      : "transparent",

                  color:
                    mode === "login"
                      ? "#000"
                      : "var(--text-secondary)",
                }}
              >
                Sign In
              </button>

              <button
                onClick={() =>
                  setMode(
                    "register"
                  )
                }
                className="
                  flex-1
                  py-3
                  rounded-xl
                  transition-all
                  font-medium
                "
                style={{
                  background:
                    mode ===
                    "register"
                      ? "linear-gradient(135deg,#E7B75F,#B3264A)"
                      : "transparent",

                  color:
                    mode ===
                    "register"
                      ? "#000"
                      : "var(--text-secondary)",
                }}
              >
                Register
              </button>
            </div>

            {/* Error */}
            {error && (
              <div
                className="
                  mb-4
                  p-4
                  rounded-xl
                  text-sm
                "
                style={{
                  background:
                    "rgba(179,38,74,0.15)",

                  border:
                    "1px solid rgba(179,38,74,0.3)",

                  color:
                    "#ffb4c4",
                }}
              >
                {error}
              </div>
            )}

            {/* Register Name */}
            {mode ===
              "register" && (
              <InputField
                label="Full Name"
                value={name}
                setValue={setName}
                placeholder="John Doe"
                type="text"
              />
            )}

            <InputField
              label="Email"
              value={email}
              setValue={setEmail}
              placeholder="you@example.com"
              type="email"
            />

            <InputField
              label="Password"
              value={password}
              setValue={setPassword}
              placeholder="••••••••"
              type="password"
            />

            <button
              onClick={
                handleSubmit
              }
              disabled={
                loading
              }
              className="
                w-full
                py-4
                rounded-2xl
                font-bold
                transition-all
                mt-4
              "
              style={{
                background:
                  "linear-gradient(135deg,#E7B75F,#B3264A)",

                color:
                  "#000",

                opacity:
                  loading
                    ? 0.7
                    : 1,

                cursor:
                  loading
                    ? "not-allowed"
                    : "pointer",
              }}
            >
              {loading
                ? "Processing..."
                : "Enter Dashboard →"}
            </button>

            <p
              className="
                text-center
                mt-8
                text-xs
              "
              style={{
                color:
                  "var(--text-secondary)",
              }}
            >
              Portfolio ·
              {" "}
              <span
                style={{
                  color:
                    "var(--gold-primary)",
                }}
              >
                Harshvardhan
              </span>
              {" "}
              · v2.0
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function InputField({
  label,
  value,
  setValue,
  placeholder,
  type,
}) {
  return (
    <div className="mb-5">
      <label
        className="
          block
          mb-2
          text-sm
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {label}
      </label>

      <input
        type={type}
        value={value}
        onChange={(e) =>
          setValue(
            e.target.value
          )
        }
        placeholder={
          placeholder
        }
        className="
          w-full
          px-5
          py-4
          rounded-2xl
          outline-none
          transition-all
        "
        style={{
          background:
            "rgba(255,255,255,0.04)",

          border:
            "1px solid rgba(255,255,255,0.08)",

          color:
            "var(--text-primary)",
        }}
      />
    </div>
  );
}

function Metric({
  value,
  label,
}) {
  return (
    <div>
      <div
        className="
          text-3xl
          font-bold
          glow-text
        "
      >
        {value}
      </div>

      <div
        className="
          mt-2
          text-sm
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {label}
      </div>
    </div>
  );
}
