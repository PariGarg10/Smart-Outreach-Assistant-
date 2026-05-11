import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function Dashboard() {
  const [metrics, setMetrics] = useState({});

  useEffect(() => {
    axios.get(`${API_BASE_URL}/metrics/`)
      .then(res => setMetrics(res.data));
  }, []);

  return (
    <div style={{ marginBottom: "30px" }}>
      <h2>📊 Dashboard</h2>
      <p>Total: {metrics.total}</p>
      <p>Sent: {metrics.sent}</p>
      <p>Pending: {metrics.pending}</p>
    </div>
  );
}