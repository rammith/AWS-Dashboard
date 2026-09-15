import { useState, useEffect } from "react";
import { useOutletContext } from "react-router";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";
import {
  Wallet,
  Users,
  Activity
} from "lucide-react";

import {
  getOverviewTotal,
  getCostTrend,
  getCostByAccount,
  getCostByService,
  getCostByEnvironment,
  getCostForecast,
  formatINR,
  formatLakh
} from "../../services/api";
import "./Overview.css";

function Overview() {
  const { selectedMonth, refreshKey, isRefreshing } = useOutletContext();

  const [totalData, setTotalData] = useState(null);
  const [costTrend, setCostTrend] = useState([]);
  const [costByAccount, setCostByAccount] = useState([]);
  const [costByService, setCostByService] = useState([]);
  const [costByEnvironment, setCostByEnvironment] = useState([]);
  const [costForecast, setCostForecast] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const accountPalette = [
    "#5b4dff",
    "#3b82f6",
    "#10b981",
    "#f59e0b",
    "#ec4899",
    "#6b7280"
  ];

  const envPalette = [
    "#5b4dff",
    "#06b6d4",
    "#10b981",
    "#8b5cf6",
    "#f59e0b"
  ];

  const serviceColors = [
    "#5b4dff",
    "#3b82f6",
    "#06b6d4",
    "#10b981",
    "#f59e0b",
    "#ec4899"
  ];

  useEffect(() => {
    async function loadOverviewData() {
      try {
        setLoading(true);
        setError(null);

        const [totalRes, trendRes, accountRes, serviceRes, envRes, forecastRes] =
          await Promise.all([
            getOverviewTotal(selectedMonth),
            getCostTrend(selectedMonth),
            getCostByAccount(selectedMonth),
            getCostByService(selectedMonth),
            getCostByEnvironment(selectedMonth),
            getCostForecast(selectedMonth),
          ]);

        setTotalData(totalRes);
        setCostTrend(trendRes || []);
        setCostByAccount(accountRes || []);
        setCostByService(serviceRes || []);
        setCostByEnvironment(envRes || []);
        setCostForecast(forecastRes || null);
      } catch (err) {
        console.error("Failed to load overview data:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadOverviewData();
  }, [selectedMonth, refreshKey]);

  if (loading && !totalData) {
    return (
      <div className="state-container">
        <div className="spinner"></div>
        <p>Loading overview analytics...</p>
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

  // Format trend data for X-axis display
  const formattedTrend = costTrend.map((item) => {
    const d = new Date(item.date);
    const dayStr = isNaN(d)
      ? item.date
      : d.toLocaleDateString("en-US", { day: "numeric", month: "short" });
    return {
      date: dayStr,
      rawDate: item.date,
      cost: Number(item.total_cost),
    };
  });

  const totalCostVal = totalData?.total_cost || 0;
  const formattedForecast = costForecast
    ? [
        {
          month: new Date(selectedMonth).toLocaleDateString("en-US", {
            month: "short",
            year: "numeric",
          }),
          cost: Number(totalCostVal),
          type: "Actual",
        },
        {
          month: new Date(costForecast.month).toLocaleDateString("en-US", {
            month: "short",
            year: "numeric",
          }),
          cost: Number(costForecast.forecast_cost || 0),
          type: "Forecast",
        },
      ]
    : [];

  return (
    <div
      className="page-container overview-container"
      style={{
        opacity: isRefreshing ? 0.4 : 1,
        transition: "opacity 0.2s ease",
      }}
    >
      {/* 1. Top Summary Metric Cards */}
      <div className="overview-metrics-grid">
        <div className="overview-metric-card">
          <div className="metric-info">
            <span className="metric-title">Total Cost</span>
            <span className="metric-value-large">
              {formatINR(totalData?.total_cost)}
            </span>
          </div>
          <div className="metric-icon-wrap metric-icon-purple">
            <Wallet size={24} />
          </div>
        </div>

        <div className="overview-metric-card">
          <div className="metric-info">
            <span className="metric-title">Total Accounts</span>
            <span className="metric-value-large">
              {totalData?.total_accounts ?? 0}
            </span>
          </div>
          <div className="metric-icon-wrap metric-icon-blue">
            <Users size={24} />
          </div>
        </div>

        <div className="overview-metric-card">
          <div className="metric-info">
            <span className="metric-title">Average Daily Cost</span>
            <span className="metric-value-large">
              {formatINR(totalData?.average_daily_cost)}
            </span>
          </div>
          <div className="metric-icon-wrap metric-icon-green">
            <Activity size={24} />
          </div>
        </div>
      </div>

      {/* 2. Daily Cost Trend Chart */}
      <div className="overview-card">
        <div className="overview-card-header">
          <div>
            <h2 className="overview-card-title">Daily Cost Trend</h2>
            <span className="overview-card-sub">
              Daily cloud expenditures across all accounts
            </span>
          </div>
        </div>

        <div style={{ width: "100%", height: 260 }}>
          {formattedTrend.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={formattedTrend}
                margin={{ top: 10, right: 20, left: 10, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="costGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#5b4dff" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#5b4dff" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#f1f5f9"
                />
                <XAxis
                  dataKey="date"
                  tickLine={false}
                  axisLine={false}
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                  tickFormatter={(val) => formatINR(val)}
                />
                <Tooltip
                  formatter={(val) => [formatINR(val), "Cost"]}
                  contentStyle={{
                    borderRadius: 8,
                    fontSize: 13,
                    border: "1px solid #e2e8f0",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="cost"
                  stroke="#5b4dff"
                  strokeWidth={2.5}
                  fillOpacity={1}
                  fill="url(#costGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="state-container">
              <p>No trend data available for this month.</p>
            </div>
          )}
        </div>
      </div>

      {/* 3. Cost by Account & Cost by Environment Grid */}
      <div className="overview-two-col">
        {/* Cost by Account */}
        <div className="overview-card">
          <div className="overview-card-header">
            <div>
              <h2 className="overview-card-title">Cost by Account</h2>
              <span className="overview-card-sub">
                Distribution across AWS accounts
              </span>
            </div>
          </div>

          <div className="donut-breakdown-wrap">
            <div className="donut-chart-box">
              <ResponsiveContainer width={190} height={190}>
                <PieChart>
                  <Pie
                    data={costByAccount}
                    dataKey="total_cost"
                    nameKey="account_name"
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    stroke="none"
                    paddingAngle={2}
                  >
                    {costByAccount.map((_, index) => (
                      <Cell
                        key={`cell-acc-${index}`}
                        fill={accountPalette[index % accountPalette.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip formatter={(val) => formatINR(val)} />
                </PieChart>
              </ResponsiveContainer>

              <div className="donut-center-info">
                <span className="donut-center-value">
                  {formatLakh(totalCostVal)}
                </span>
                <span className="donut-center-label">Total</span>
              </div>
            </div>

            <div className="donut-breakdown-list">
              {costByAccount.map((acc, index) => {
                const percent =
                  totalCostVal > 0
                    ? ((acc.total_cost / totalCostVal) * 100).toFixed(1)
                    : 0;
                return (
                  <div key={acc.account_id} className="breakdown-row">
                    <div className="breakdown-left">
                      <span
                        className="breakdown-dot"
                        style={{
                          backgroundColor:
                            accountPalette[index % accountPalette.length],
                        }}
                      ></span>
                      <span className="breakdown-name">{acc.account_name}</span>
                    </div>
                    <div className="breakdown-right">
                      <span className="breakdown-cost">
                        {formatINR(acc.total_cost)}
                      </span>
                      <span className="breakdown-percent">{percent}%</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Cost by Environment */}
        <div className="overview-card">
          <div className="overview-card-header">
            <div>
              <h2 className="overview-card-title">Cost by Environment</h2>
              <span className="overview-card-sub">
                Distribution by deployment environment
              </span>
            </div>
          </div>

          <div className="donut-breakdown-wrap">
            <div className="donut-chart-box">
              <ResponsiveContainer width={190} height={190}>
                <PieChart>
                  <Pie
                    data={costByEnvironment}
                    dataKey="total_cost"
                    nameKey="environment"
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    stroke="none"
                    paddingAngle={2}
                  >
                    {costByEnvironment.map((_, index) => (
                      <Cell
                        key={`cell-env-${index}`}
                        fill={envPalette[index % envPalette.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip formatter={(val) => formatINR(val)} />
                </PieChart>
              </ResponsiveContainer>

              <div className="donut-center-info">
                <span className="donut-center-value">
                  {formatLakh(totalCostVal)}
                </span>
                <span className="donut-center-label">Total</span>
              </div>
            </div>

            <div className="donut-breakdown-list">
              {costByEnvironment.map((env, index) => {
                const percent =
                  totalCostVal > 0
                    ? ((env.total_cost / totalCostVal) * 100).toFixed(1)
                    : 0;
                return (
                  <div key={env.environment} className="breakdown-row">
                    <div className="breakdown-left">
                      <span
                        className="breakdown-dot"
                        style={{
                          backgroundColor:
                            envPalette[index % envPalette.length],
                        }}
                      ></span>
                      <span className="breakdown-name">{env.environment}</span>
                    </div>
                    <div className="breakdown-right">
                      <span className="breakdown-cost">
                        {formatINR(env.total_cost)}
                      </span>
                      <span className="breakdown-percent">{percent}%</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* 4. Cost by Service */}
      <div className="overview-card">
        <div className="overview-card-header">
          <div>
            <h2 className="overview-card-title">Cost by Service</h2>
            <span className="overview-card-sub">
              Breakdown across AWS cloud services
            </span>
          </div>
        </div>

        <div className="services-grid">
          {costByService.map((srv, index) => {
            const percent =
              totalCostVal > 0
                ? ((srv.total_cost / totalCostVal) * 100).toFixed(1)
                : 0;
            const barColor = serviceColors[index % serviceColors.length];

            return (
              <div key={srv.service} className="service-item-card">
                <div className="service-item-header">
                  <span className="service-title">{srv.service}</span>
                  <span className="service-cost-tag">
                    {formatINR(srv.total_cost)}
                  </span>
                </div>

                <div className="service-bar-track">
                  <div
                    className="service-bar-fill"
                    style={{
                      width: `${percent}%`,
                      backgroundColor: barColor,
                    }}
                  ></div>
                </div>

                <div className="service-footer-stats">
                  <span>Share of total cost</span>
                  <span>{percent}%</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 5. Cost Forecast Chart */}
      <div className="overview-card">
        <div className="overview-card-header">
          <div>
            <h2 className="overview-card-title">Cost Forecast</h2>
            <span className="overview-card-sub">
              Projected cost for the next month based on historical spending
            </span>
          </div>
        </div>

        <div style={{ width: "100%", height: 260 }}>
          {formattedForecast.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={formattedForecast}
                margin={{ top: 10, right: 20, left: 10, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="forecastGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#f1f5f9"
                />
                <XAxis
                  dataKey="month"
                  tickLine={false}
                  axisLine={false}
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tick={{ fill: "#94a3b8", fontSize: 12 }}
                  tickFormatter={(val) => formatINR(val)}
                />
                <Tooltip
                  formatter={(val, _, item) => [formatINR(val), item.payload.type]}
                  contentStyle={{
                    borderRadius: 8,
                    fontSize: 13,
                    border: "1px solid #e2e8f0",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="cost"
                  stroke="#10b981"
                  strokeWidth={2.5}
                  fillOpacity={1}
                  fill="url(#forecastGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="state-container">
              <p>No forecast data available.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Overview;