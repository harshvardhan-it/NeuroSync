/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ["Syne", "sans-serif"],
        body: ["DM Sans", "sans-serif"],
        mono: ["DM Mono", "monospace"],
      },
      colors: {
        cyan: "#22d3ee",
        violet: "#a78bfa",
        success: "#34d399",
        warning: "#fbbf24",
        danger: "#f87171",
      },
      animation: {
        "fade-up": "fadeUp 0.4s ease forwards",
        "spin-slow": "spin 1s linear infinite",
      },
    },
  },
  plugins: [],
};