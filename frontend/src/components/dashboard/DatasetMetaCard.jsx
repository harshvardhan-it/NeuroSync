export default function DatasetMetaCard({
  dataset,
}) {
  if (!dataset) return null;

  return (
    <div
      className="
        rounded-[28px]
        p-6
        mb-6
        grid
        grid-cols-2
        md:grid-cols-4
        gap-4
      "
      style={{
        background:
          "rgba(255,255,255,0.03)",

        border:
          "1px solid rgba(255,255,255,0.08)",

        backdropFilter:
          "blur(24px)",

        boxShadow:
          "0 20px 60px rgba(0,0,0,0.25)",
      }}
    >
      <MetaItem
        label="Dataset"
        value={dataset.name}
      />

      <MetaItem
        label="Rows"
        value={dataset.rows}
      />

      <MetaItem
        label="Columns"
        value={dataset.columns}
      />

      <MetaItem
        label="Uploaded"
        value={dataset.uploaded}
      />
    </div>
  );
}

function MetaItem({
  label,
  value,
}) {
  return (
    <div>
      <div
        className="
          text-xs
          uppercase
          tracking-[0.2em]
          mb-2
        "
        style={{
          color:
            "var(--text-secondary)",
        }}
      >
        {label}
      </div>

      <div
        className="
          text-xl
          font-semibold
        "
      >
        {value}
      </div>
    </div>
  );
}