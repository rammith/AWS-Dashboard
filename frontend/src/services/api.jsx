const API_BASE_URL = import.meta.env.VITE_API_URL ||"http://localhost:8000";

/**
 * Fetch total overview statistics for the given month (YYYY-MM-DD)
 */
export async function getOverviewTotal(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/overview/total?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch overview data: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch cost breakdown by account for the given month
 */
export async function getCostByAccount(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/overview/cost-by-account?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch cost by account: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch daily cost trend for the given month
 */
export async function getCostTrend(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/overview/cost_trend?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch cost trend: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch cost breakdown by AWS service for the given month
 */
export async function getCostByService(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/overview/cost_by_service?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch cost by service: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch cost distribution by environment for the given month
 */
export async function getCostByEnvironment(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/overview/cost_by_environment?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch cost by environment: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch accounts summary metrics for the given month
 */
export async function getAccountsSummary(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/accounts/summary?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch accounts summary: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch full list of accounts with cost and trend for the given month
 */
export async function getAccounts(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/accounts?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch accounts: ${response.statusText}`);
  }
  return response.json();
}


export async function getCostForecast(month) {
  const response = await fetch(
    `${API_BASE_URL}/api/overview/cost_forecast?month=${month}`
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch cost forecast: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Currency formatter for US Dollars (e.g. $3,392.56)
 */
export function formatCurrency(amount, decimals = 2) {
  if (amount === undefined || amount === null || isNaN(amount)) return "$0.00";
  const num = Number(amount);
  return "$" + num.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * Compact currency formatter (e.g. $3.39K or $1.2M)
 */
export function formatCompactCurrency(amount) {
  if (amount === undefined || amount === null || isNaN(amount)) return "$0";
  const num = Number(amount);
  if (num >= 1000000) {
    return `$${(num / 1000000).toFixed(2)}M`;
  } else if (num >= 1000) {
    return `$${(num / 1000).toFixed(2)}K`;
  }
  return formatCurrency(num, 0);
}

// Aliases for seamless backward compatibility
export const formatINR = formatCurrency;
export const formatLakh = formatCompactCurrency;