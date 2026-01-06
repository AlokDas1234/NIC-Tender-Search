import React, { useEffect, useState } from "react";
import API from "./api";

const ScraperStatus = () => {
  const [status, setStatus] = useState({
    is_running: false,
    searching_state_name: "",
    searching_key: "",
    task_id: null,
  });

  const fetchStatus = async () => {
    try {
      const res = await API.get("scraper-status/");
      setStatus(res.data);
    } catch (err) {
      console.error("Failed to fetch scraper status", err);
    }
  };

  useEffect(() => {
    fetchStatus(); // initial load

    const interval = setInterval(() => {
      fetchStatus();
    }, 3000); // poll every 3 sec

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ border: "1px solid #ccc", padding: 16, marginTop: 20 }}>
      <h3>Scraper Status</h3>

      <p>
        Status:{" "}
        {status.is_running ? (
          <span style={{ color: "green" }}>🟢 Running</span>
        ) : (
          <span style={{ color: "gray" }}>⚪ Idle</span>
        )}
      </p>

      {status.is_running && (
        <>
          <p>
            <strong>State:</strong> {status.searching_state_name}  <strong>Keyword:</strong> {status.searching_key}
          </p>
         
        </>
      )}
    </div>
  );
};

export default ScraperStatus;
