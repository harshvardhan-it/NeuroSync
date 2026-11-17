export default function InsightSummary({ insights = [] }) {
  return (
    <section className="glass-card p-6">
      <p className="text-sm" style={{ color: "var(--text-secondary)" }}>Selected dataset</p>
      <h2 className="text-2xl font-display font-bold mt-2">Insight Summary</h2>
      <p className="mt-4 leading-7" style={{ color: "var(--text-secondary)" }}>
        {insights.length
          ? `${insights.length} observations were generated from this dataset. Review the calculated KPIs and analysis observations below.`
          : "The analysis pipeline did not return any insight observations for this dataset."}
      </p>
    </section>
  );
}
