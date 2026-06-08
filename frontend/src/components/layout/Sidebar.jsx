import { NavLink } from "react-router-dom";

const items = [
  {
    label: "Overview",
    path: "/dashboard",
  },
  {
    label: "Analysis",
    path: "/analysis",
  },
  {
    label: "Insights",
    path: "/insights",
  },
  {
    label: "Anomalies",
    path: "/anomalies",
  },
  {
    label: "Forecasts",
    path: "/forecasts",
  },
  {
    label: "Risk",
    path: "/risk",
  },
  {
    label: "Recommendations",
    path: "/recommendations",
  },
  {
    label: "Decisions",
    path: "/decisions",
  },
  {
    label: "Action Plan",
    path: "/action-plan",
  },
];

export default function Sidebar() {
return (
<aside
className="
w-[216px]
border-r
h-screen
flex
flex-col
"
style={{
borderColor: "var(--border)",
background:
"rgba(255,255,255,0.02)",
}}
> <div className="px-6 py-6"> <div className="flex items-center gap-3">
<div
className="
w-8
h-8
rounded-lg
flex
items-center
justify-center
font-bold
text-black
"
style={{
background:
"linear-gradient(135deg,#22d3ee,#a78bfa)",
}}
>
N </div>

```
      <div>
        <div className="font-display font-bold">
          NeuroSync
        </div>

        <div
          className="text-xs"
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          AI Platform
        </div>
      </div>
    </div>
  </div>

  <nav className="px-3 flex-1">
    {items.map((item) => (
      <NavLink
        key={item.path}
        to={item.path}
        className={({ isActive }) =>
          `
          flex
          items-center
          px-4
          py-3
          rounded-xl
          mb-1
          transition-all
          ${
            isActive
              ? "bg-white/10"
              : "hover:bg-white/5"
          }
        `
        }
      >
        {item.label}
      </NavLink>
    ))}
  </nav>

  <div
    className="m-4 p-4 rounded-xl"
    style={{
      background:
        "rgba(255,255,255,0.04)",
    }}
  >
    <div className="text-sm font-semibold">
      Harshvardhan
    </div>

    <div
      className="text-xs mt-1"
      style={{
        color:
          "var(--text-secondary)",
      }}
    >
      Portfolio Build
    </div>
  </div>
</aside>


);
}
