import DashboardLayout from "../components/layout/DashboardLayout";

export default function DashboardPage() {
return ( <DashboardLayout> <div className="grid grid-cols-3 gap-6">

```
    <div className="glass-card p-6">
      <h3>Health Score</h3>

      <div className="text-4xl mt-4 font-bold">
        92
      </div>
    </div>

    <div className="glass-card p-6">
      <h3>Risk Score</h3>

      <div className="text-4xl mt-4 font-bold">
        18
      </div>
    </div>

    <div className="glass-card p-6">
      <h3>Status</h3>

      <div className="text-4xl mt-4 font-bold">
        Healthy
      </div>
    </div>

  </div>
</DashboardLayout>


);
}
