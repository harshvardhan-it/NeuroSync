import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

export default function DashboardLayout({
children,
}) {
return ( <div className="flex min-h-screen"> <Sidebar />

```
  <div className="ml-[220px]">
    <TopBar />
    <main className="p-8">
      {children}
    </main>
  </div>
</div>


);
}
