import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";


function CostByAccount({ accounts }) {

  const totalCost = accounts.reduce(
    (total, account) => total + account.total_cost,
    0
  );


  return (
    <div className="cost-by-account">

      <h2>Cost by Account</h2>


      <div className="cost-account-content">

        {/* Pie Chart */}

        <div className="cost-account-chart">

          <ResponsiveContainer width="100%" height={350}>

            <PieChart>

              <Pie
                data={accounts}
                dataKey="total_cost"
                nameKey="account_name"
                cx="50%"
                cy="50%"
                outerRadius={140}
                label={({ percent }) =>
                  `${(percent * 100).toFixed(1)}%`
                }
              >

                {accounts.map((account, index) => (
                  <Cell
                    key={account.account_id}
                    fill={`hsl(${index * 70}, 65%, 55%)`}
                  />
                ))}

              </Pie>

              <Tooltip
                formatter={(value) =>
                  `$${Number(value).toFixed(2)}`
                }
              />

            </PieChart>

          </ResponsiveContainer>

        </div>


        {/* Account Table */}

        <div className="cost-account-table">

          <div className="table-header">

            <span>Account</span>

            <span>Cost</span>

            <span>% of Total</span>

          </div>


          {accounts.map((account) => {

            const percentage =
              totalCost === 0
                ? 0
                : (account.total_cost / totalCost) * 100;


            return (
              <div
                className="table-row"
                key={account.account_id}
              >

                <span>
                  {account.account_name}
                </span>

                <span>
                  ${account.total_cost.toFixed(2)}
                </span>

                <span>
                  {percentage.toFixed(1)}%
                </span>

              </div>
            );

          })}


          {/* Total */}

          <div className="table-total">

            <span>Total</span>

            <span>
              ${totalCost.toFixed(2)}
            </span>

            <span>100%</span>

          </div>

        </div>

      </div>

    </div>
  );
}

export default CostByAccount;