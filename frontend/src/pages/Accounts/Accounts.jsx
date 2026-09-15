import { useState, useEffect } from "react";
import { useOutletContext } from "react-router";
import {
  Users,
  Wallet,
  Calculator,
  Search,
  Copy,
  Check,
  ArrowUpRight,
  ArrowDownRight
} from "lucide-react";

import {
  getAccountsSummary,
  getAccounts,
  formatINR
} from "../../services/api";
import "./Accounts.css";

function Accounts() {
  const { selectedMonth, refreshKey, isRefreshing } = useOutletContext();

  const [summary, setSummary] = useState(null);
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [envFilter, setEnvFilter] = useState("all");
  const [copiedId, setCopiedId] = useState(null);

  useEffect(() => {
    async function loadAccountsData() {
      try {
        setLoading(true);
        setError(null);

        const [summaryRes, accountsRes] = await Promise.all([
          getAccountsSummary(selectedMonth),
          getAccounts(selectedMonth),
        ]);

        setSummary(summaryRes);
        setAccounts(accountsRes || []);
      } catch (err) {
        console.error("Failed to load accounts data:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadAccountsData();
  }, [selectedMonth, refreshKey]);

  const handleCopy = (id) => {
    navigator.clipboard.writeText(id);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Filter accounts by search query and environment
  const filteredAccounts = accounts.filter((acc) => {
    const matchesSearch =
      acc.account_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      acc.account_id.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch) return false;

    if (envFilter !== "all") {
      if (acc.environment.toLowerCase() !== envFilter.toLowerCase()) {
        return false;
      }
    }

    return true;
  });

  if (loading && !summary) {
    return (
      <div className="state-container">
        <div className="spinner"></div>
        <p>Loading AWS accounts...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="state-container">
        <p style={{ color: "var(--danger)" }}>Error: {error}</p>
      </div>
    );
  }

  return (
    <div
      className="page-container accounts-container"
      style={{
        opacity: isRefreshing ? 0.4 : 1,
        transition: "opacity 0.2s ease",
      }}
    >
      {/* 1. Summary Cards */}
      <div className="accounts-metrics-grid">
        <div className="account-metric-card">
          <div className="account-metric-info">
            <span className="account-metric-label">Total Accounts</span>
            <span className="account-metric-val">
              {summary?.total_accounts ?? accounts.length}
            </span>
          </div>
          <div
            className="account-metric-icon"
            style={{ backgroundColor: "#f3f0ff", color: "#7c3aed" }}
          >
            <Users size={24} />
          </div>
        </div>

        <div className="account-metric-card">
          <div className="account-metric-info">
            <span className="account-metric-label">Total Monthly Cost</span>
            <span className="account-metric-val">
              {formatINR(summary?.total_monthly_cost)}
            </span>
          </div>
          <div
            className="account-metric-icon"
            style={{ backgroundColor: "#eff6ff", color: "#3b82f6" }}
          >
            <Wallet size={24} />
          </div>
        </div>

        <div className="account-metric-card">
          <div className="account-metric-info">
            <span className="account-metric-label">Avg. Cost / Account</span>
            <span className="account-metric-val">
              {formatINR(summary?.average_monthly_cost_per_account)}
            </span>
          </div>
          <div
            className="account-metric-icon"
            style={{ backgroundColor: "#ecfdf5", color: "#10b981" }}
          >
            <Calculator size={24} />
          </div>
        </div>
      </div>

      {/* 2. Search and Filter Toolbar */}
      <div className="accounts-toolbar">
        <div className="accounts-search-wrap">
          <Search className="accounts-search-icon" />
          <input
            type="text"
            className="accounts-search-input"
            placeholder="Search by account name or ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <select
          className="accounts-filter-select"
          value={envFilter}
          onChange={(e) => setEnvFilter(e.target.value)}
        >
          <option value="all">All Environments</option>
          <option value="production">Production</option>
          <option value="development">Development</option>
          <option value="qa/staging">QA / Staging</option>
          <option value="others">Others</option>
        </select>
      </div>

      {/* 3. Accounts Table */}
      <div className="accounts-table-card">
        <table className="accounts-table">
          <thead>
            <tr>
              <th>Account ID</th>
              <th>Account Name</th>
              <th>Environment</th>
              <th>Monthly Cost</th>
              <th>Trend</th>
            </tr>
          </thead>
          <tbody>
            {filteredAccounts.length > 0 ? (
              filteredAccounts.map((acc) => {
                const isIncrease = acc.trend_direction === "increase";
                const trendVal = acc.trend_percentage
                  ? `${acc.trend_percentage.toFixed(1)}%`
                  : "-";

                const envLower = acc.environment?.toLowerCase() || "";
                const envClass = envLower.includes("prod")
                  ? "acc-env-prod"
                  : envLower.includes("qa") || envLower.includes("stag")
                  ? "acc-env-qa"
                  : envLower.includes("dev")
                  ? "acc-env-dev"
                  : "acc-env-other";

                return (
                  <tr key={acc.account_id}>
                    {/* Account ID with copy */}
                    <td>
                      <div className="acc-id-cell">
                        <span>{acc.account_id}</span>
                        <button
                          className="acc-copy-btn"
                          onClick={() => handleCopy(acc.account_id)}
                          title="Copy Account ID"
                        >
                          {copiedId === acc.account_id ? (
                            <Check size={14} color="#10b981" />
                          ) : (
                            <Copy size={14} />
                          )}
                        </button>
                      </div>
                    </td>

                    {/* Account Name */}
                    <td>
                      <span className="acc-name-cell">{acc.account_name}</span>
                    </td>

                    {/* Environment */}
                    <td>
                      <span className={`acc-env-badge ${envClass}`}>
                        {acc.environment}
                      </span>
                    </td>

                    {/* Monthly Cost */}
                    <td>
                      <span className="acc-cost-cell">
                        {formatINR(acc.monthly_cost)}
                      </span>
                    </td>

                    {/* Trend */}
                    <td>
                      {acc.trend_percentage !== null && acc.trend_percentage !== undefined ? (
                        <div
                          className={`acc-trend-pill ${
                            isIncrease ? "acc-trend-up" : "acc-trend-down"
                          }`}
                        >
                          {isIncrease ? (
                            <ArrowUpRight size={14} />
                          ) : (
                            <ArrowDownRight size={14} />
                          )}
                          <span>{trendVal}</span>
                        </div>
                      ) : (
                        <span style={{ color: "#94a3b8" }}>-</span>
                      )}
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="5" style={{ textAlign: "center", padding: "32px", color: "#64748b" }}>
                  No accounts found matching your search.
                </td>
              </tr>
            )}
          </tbody>
        </table>

        {/* Footer */}
        <div className="accounts-table-footer">
          <span>
            Showing {filteredAccounts.length} of {accounts.length} accounts
          </span>
          <span>Selected month: {selectedMonth}</span>
        </div>
      </div>
    </div>
  );
}

export default Accounts;