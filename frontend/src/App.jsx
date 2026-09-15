import { Routes, Route, Navigate } from "react-router";

import DashboardLayout from "./components/DashboardLayout/DashboardLayout";

import Overview from "./pages/Overview/Overview";
import Accounts from "./pages/Accounts/Accounts";


function App() {
  return (
    <Routes>

      <Route element={<DashboardLayout />}>

        <Route
          path="/overview"
          element={<Overview />}
        />

        <Route
          path="/accounts"
          element={<Accounts />}
        />

      </Route>


      <Route
        path="/"
        element={<Navigate to="/overview" />}
      />

    </Routes>
  );
}

export default App;