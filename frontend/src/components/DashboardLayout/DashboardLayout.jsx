import { useState } from "react";
import { Outlet } from "react-router";
import Sidebar from "../Sidebar/Sidebar";
import Header from "../Header/Header";
import "./DashboardLayout.css";

function DashboardLayout() {
  const [selectedMonth, setSelectedMonth] = useState("2025-08-01");
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setRefreshKey((prev) => prev + 1);

    setTimeout(() => {
      setIsRefreshing(false);
    }, 600);
  };

  return (
    <div className="dashboard-layout">
      <Sidebar isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />

      <div className="main-area">
        <Header
          selectedMonth={selectedMonth}
          onMonthChange={setSelectedMonth}
          onRefresh={handleRefresh}
        />

        <main className="main-content">
          <Outlet
            context={{
              selectedMonth,
              setSelectedMonth,
              refreshKey,
              isRefreshing,
            }}
          />
        </main>
      </div>
    </div>
  );
}

export default DashboardLayout;