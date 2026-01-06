import React from "react";
import API from "./api"; // Make sure this points to your axios setup

function ScraperControl() {
  const startScraper = async () => {
    try {
      const res = await API.post("run-scraper/"); // Calls your Django start endpoint
      alert("✅ Scraper started");
      console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Failed to start scraper");
    }
  };

  return (
    <div>
      <h3>Scraper Control</h3>
      <button onClick={startScraper}>Start Scrape</button>
    </div>
  );
}

export default ScraperControl;
