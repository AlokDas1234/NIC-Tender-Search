import React from "react";
import ScraperStatus from "../components/ScraperStatus";

const Dashboard = () => {
  return (
    <div>
      <h2>Scraper Dashboard</h2>

      {/* Other components like upload, run buttons */}

      <ScraperStatus />
    </div>
  );
};

export default Dashboard;
