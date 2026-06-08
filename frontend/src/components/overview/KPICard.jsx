import React from "react";

export default function KPICard({
  title,
  value,
  change,
}) {
  return (
    <div className="glass-card p-6">
      <div
        className="text-sm"
        style={{
          color: "var(--text-secondary)",
        }}
      >
        {title}
      </div>

      <div className="text-4xl font-bold mt-4">
        {value}
      </div>

      <div
        className="mt-2 text-sm"
        style={{
          color: "var(--success)",
        }}
      >
        {change}
      </div>
    </div>
  );
}