import { useState, useRef, useEffect } from "react";
import { useLocation } from "react-router";
import {
  Calendar,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  RefreshCw
} from "lucide-react";
import "./Header.css";

const MONTH_NAMES = [
  { short: "Jan", full: "January", num: "01" },
  { short: "Feb", full: "February", num: "02" },
  { short: "Mar", full: "March", num: "03" },
  { short: "Apr", full: "April", num: "04" },
  { short: "May", full: "May", num: "05" },
  { short: "Jun", full: "June", num: "06" },
  { short: "Jul", full: "July", num: "07" },
  { short: "Aug", full: "August", num: "08" },
  { short: "Sep", full: "September", num: "09" },
  { short: "Oct", full: "October", num: "10" },
  { short: "Nov", full: "November", num: "11" },
  { short: "Dec", full: "December", num: "12" },
];

function formatDisplayRange(dateStr) {
  if (!dateStr) return "Select Date";
  const parts = dateStr.split("-");
  const year = parseInt(parts[0], 10);
  const monthIdx = parseInt(parts[1], 10) - 1;

  if (isNaN(year) || isNaN(monthIdx) || monthIdx < 0 || monthIdx > 11) {
    return dateStr;
  }

  const lastDay = new Date(year, monthIdx + 1, 0).getDate();
  const monthShort = MONTH_NAMES[monthIdx].short;
  return `01 ${monthShort} ${year} - ${lastDay} ${monthShort} ${year}`;
}

function Header({ selectedMonth, onMonthChange, onRefresh }) {
  const location = useLocation();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(() =>
    new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  );
  const dropdownRef = useRef(null);

  // Extract selected year and month
  const currentYear = selectedMonth ? selectedMonth.substring(0, 4) : "2025";
  const currentMonthNum = selectedMonth ? selectedMonth.substring(5, 7) : "08";

  // Active year in picker view (defaults to selected year)
  const [viewYear, setViewYear] = useState(currentYear);

  useEffect(() => {
    if (selectedMonth) {
      setViewYear(selectedMonth.substring(0, 4));
    }
  }, [selectedMonth]);

  const isAccounts = location.pathname.includes("accounts");

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleRefreshClick = () => {
    setIsRefreshing(true);
    if (onRefresh) onRefresh();
    setTimeout(() => {
      setIsRefreshing(false);
      setLastUpdated(
        new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      );
    }, 600);
  };

  const handleSelectMonth = (monthNum) => {
    const newMonthDate = `${viewYear}-${monthNum}-01`;
    onMonthChange(newMonthDate);
    setDropdownOpen(false);
  };

  const handleCustomDateChange = (e) => {
    const val = e.target.value;
    if (val) {
      onMonthChange(val);
      setDropdownOpen(false);
    }
  };

  return (
    <header className="top-header">
      <div className="header-title-group">
        <h1 className="header-page-title">
          {isAccounts ? "Accounts" : "Overview"}
        </h1>
        <p className="header-page-subtitle">
          {isAccounts
            ? "Manage and monitor connected AWS accounts & costs"
            : "AWS cost analytics and usage breakdown"}
        </p>
      </div>

      <div className="header-actions">
        {/* Date & Month Picker Dropdown */}
        <div className="date-picker-wrap" ref={dropdownRef}>
          <button
            className={`date-picker-button ${dropdownOpen ? "open" : ""}`}
            onClick={() => setDropdownOpen(!dropdownOpen)}
            type="button"
          >
            <Calendar size={16} color="#5b4dff" />
            <span>{formatDisplayRange(selectedMonth)}</span>
            <ChevronDown size={14} color="#64748b" />
          </button>

          {dropdownOpen && (
            <div className="date-picker-dropdown">
              {/* Year Navigation */}
              <div className="year-picker-header">
                <button
                  type="button"
                  className="year-nav-btn"
                  onClick={() =>
                    setViewYear(String(Math.max(2024, parseInt(viewYear, 10) - 1)))
                  }
                  disabled={viewYear === "2024"}
                  title="Previous Year"
                >
                  <ChevronLeft size={16} />
                </button>

                <div className="year-tabs">
                  <button
                    type="button"
                    className={`year-tab-btn ${viewYear === "2024" ? "active" : ""}`}
                    onClick={() => setViewYear("2024")}
                  >
                    2024
                  </button>
                  <button
                    type="button"
                    className={`year-tab-btn ${viewYear === "2025" ? "active" : ""}`}
                    onClick={() => setViewYear("2025")}
                  >
                    2025
                  </button>
                </div>

                <button
                  type="button"
                  className="year-nav-btn"
                  onClick={() =>
                    setViewYear(String(Math.min(2025, parseInt(viewYear, 10) + 1)))
                  }
                  disabled={viewYear === "2025"}
                  title="Next Year"
                >
                  <ChevronRight size={16} />
                </button>
              </div>

              {/* 12 Months Grid */}
              <div className="months-grid">
                {MONTH_NAMES.map((m) => {
                  const isSelected =
                    currentYear === viewYear && currentMonthNum === m.num;
                  return (
                    <button
                      key={m.num}
                      type="button"
                      className={`month-cell-btn ${isSelected ? "active" : ""}`}
                      onClick={() => handleSelectMonth(m.num)}
                    >
                      {m.short}
                    </button>
                  );
                })}
              </div>

              {/* Custom Date Input */}
              <div className="custom-date-section">
                <span className="custom-date-label">Or select specific date:</span>
                <input
                  type="date"
                  className="custom-date-input"
                  min="2024-01-01"
                  max="2025-12-31"
                  value={selectedMonth}
                  onChange={handleCustomDateChange}
                />
              </div>
            </div>
          )}
        </div>

        {/* Refresh Action */}
        <button
          className="header-icon-btn"
          onClick={handleRefreshClick}
          title="Refresh Data"
          type="button"
        >
          <RefreshCw
            size={16}
            style={{
              animation: isRefreshing ? "spin 0.6s linear infinite" : "none",
            }}
          />
        </button>

        {/* User Avatar */}
        <div className="header-user-avatar" title="Admin">
          AD
        </div>
      </div>
    </header>
  );
}

export default Header;