export default function TopBar() {
return (
<div
className="
h-[72px]
px-8
flex
items-center
justify-between
border-b
"
style={{
borderColor:
"var(--border)",
}}
> <div>
<div
className="text-xs"
style={{
color:
"var(--text-secondary)",
}}
>
Workspace </div>

```
    <h1
      className="
        font-display
        text-xl
        font-bold
      "
    >
      NeuroSync Dashboard
    </h1>
  </div>

  <div className="flex items-center gap-3">
    <div
      className="
        px-3
        py-2
        rounded-lg
        text-sm
      "
      style={{
        background:
          "rgba(34,211,238,0.08)",
        color:
          "var(--cyan)",
      }}
    >
      Connected
    </div>
  </div>
</div>


);
}
