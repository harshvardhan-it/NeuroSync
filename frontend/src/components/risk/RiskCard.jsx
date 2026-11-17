import RiskLevelBadge from "./RiskLevelBadge";

export default function RiskCard({ title, level, score, description, source }) {
  return (
    <div className="glass-card p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm" style={{ color: "var(--text-secondary)" }}>Risk category</p>
          <h3 className="text-2xl font-bold mt-2">{title}</h3>
          {source && <p className="text-xs mt-2" style={{ color: "var(--text-secondary)" }}>{source}</p>}
        </div>
        <RiskLevelBadge level={level} />
      </div>
      <div className="mt-6 rounded-xl p-4" style={{ background: "rgba(255,255,255,0.03)" }}>
        <p className="text-xs" style={{ color: "var(--text-secondary)" }}>Risk score</p>
        <div className="mt-2 text-3xl font-bold">{score}</div>
      </div>
      <p className="mt-5" style={{ color: "var(--text-secondary)", lineHeight: "1.7" }}>{description}</p>
    </div>
  );
}
