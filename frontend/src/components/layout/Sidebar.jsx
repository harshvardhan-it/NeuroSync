import { NavLink } from "react-router-dom";
import DatasetHistory from
  "../dashboard/DatasetHistory";
const items = [
  {
    label: "Workspace",
    path: "/workspace",
  },
  {
    label: "Overview",
    path: "/dashboard",
  },
];

export default function Sidebar() {
  return (
    <aside
      className="
        fixed
        left-0
        top-0
        w-[220px]
        h-screen
        border-r
        flex
        flex-col
        z-50
      "
      style={{
        borderColor:
          "rgba(255,255,255,0.06)",

        background:
          "rgba(10,10,10,0.82)",

        backdropFilter:
          "blur(24px)",
      }}
    >
      {/* Logo */}
      <div className="px-5 py-5">
        <div className="flex items-center gap-3">
          <div
            className="
              w-10
              h-10
              rounded-xl
              flex
              items-center
              justify-center
              font-bold
              text-black
            "
            style={{
              background:
                "linear-gradient(135deg,#E7B75F,#B3264A)",
            }}
          >
            N
          </div>

          <div>
            <div
              className="
                font-display
                font-bold
                text-lg
              "
            >
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

      {/* Section */}
      <div className="px-5 mb-3">
        <div
          className="
            text-xs
            uppercase
            tracking-[0.25em]
          "
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          Workspace
        </div>
      </div>

      {/* Navigation */}
      <nav className="px-3">
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `
              flex
              items-center
              px-5
              py-3
              rounded-2xl
              mb-2
              transition-all
              duration-300
              ${
                isActive
                  ? "bg-white/10"
                  : "hover:bg-white/5"
              }
            `
            }
          >
            <span className="font-medium">
              {item.label}
            </span>
          </NavLink>
        ))}
      </nav>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Dataset History */}
      <DatasetHistory />

      {/* User Card */}
      <div className="p-4">
        <div
          className="
            p-4
            rounded-2xl
          "
          style={{
            background:
              "rgba(255,255,255,0.03)",

            border:
              "1px solid rgba(255,255,255,0.06)",
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
            AI Executive
          </div>
        </div>
      </div>
    </aside>
  );
}