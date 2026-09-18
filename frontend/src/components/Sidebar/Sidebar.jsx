import { NavLink } from "react-router";
import {
  LayoutDashboard,
  Users,
  ChevronLeft,
  ChevronRight,
  ChevronUp
} from "lucide-react";
import "./Sidebar.css";

function Sidebar({ isCollapsed, setIsCollapsed }) {
  const navItems = [
    { name: "Overview", path: "/overview", icon: LayoutDashboard },
    { name: "Accounts", path: "/accounts", icon: Users },
  ];

  return (
    <aside className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
      {/* Brand Header */}
      <div className="sidebar-header">
        <div className="logo-icon-wrap">
          <svg width="34" height="34" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 2L32 10.0825V26.2474L18 34.33L4 26.2474V10.0825L18 2Z" fill="none" stroke="url(#paint0_linear)" strokeWidth="2.5" />
            <path d="M18 2V18.165M18 18.165L32 10.0825M18 18.165L4 10.0825M18 18.165V34.33" stroke="url(#paint1_linear)" strokeWidth="2.2" strokeLinecap="round" />
            <defs>
              <linearGradient id="paint0_linear" x1="4" y1="2" x2="32" y2="34" gradientUnits="userSpaceOnUse">
                <stop stopColor="#6366F1" />
                <stop offset="0.5" stopColor="#EC4899" />
                <stop offset="1" stopColor="#F59E0B" />
              </linearGradient>
              <linearGradient id="paint1_linear" x1="4" y1="10" x2="32" y2="26" gradientUnits="userSpaceOnUse">
                <stop stopColor="#818CF8" />
                <stop offset="1" stopColor="#C084FC" />
              </linearGradient>
            </defs>
          </svg>
        </div>

        {!isCollapsed && (
          <div className="logo-text">
            <span className="logo-title">AWS Dasboard</span>
            <span className="logo-subtitle">Analyzer</span>
          </div>
        )}
      </div>

      {/* Navigation List: Overview and Accounts only */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
              title={isCollapsed ? item.name : undefined}
            >
              <Icon className="nav-icon" />
              {!isCollapsed && <span>{item.name}</span>}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer / User Profile & Collapse */}
      <div className="sidebar-footer">
        {!isCollapsed && (
          <div className="user-profile-card">
            <div className="user-avatar-initials">AD</div>
            <div className="user-info">
              <span className="user-name">Admin</span>
            </div>
            <ChevronUp size={16} color="#64748b" />
          </div>
        )}

        <button
          className="collapse-btn"
          onClick={() => setIsCollapsed(!isCollapsed)}
          title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
        >
          {isCollapsed ? (
            <ChevronRight size={18} />
          ) : (
            <>
              <ChevronLeft size={18} />
              <span>Collapse</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;