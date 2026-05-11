import { useState } from "react";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function Upload() {
  const [data, setData] = useState([]);
  const [smtpEmail, setSmtpEmail] = useState(localStorage.getItem("smtp_email") || "");
  const [smtpAppPassword, setSmtpAppPassword] = useState(localStorage.getItem("smtp_app_password") || "");
  const [openaiApiKey, setOpenaiApiKey] = useState(localStorage.getItem("openai_api_key") || "");
  const [result, setResult] = useState(null);
  const [sending, setSending] = useState(false);

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setSending(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("smtp_email", smtpEmail);
    formData.append("smtp_app_password", smtpAppPassword);
    formData.append("openai_api_key", openaiApiKey);
    localStorage.setItem("smtp_email", smtpEmail);
    localStorage.setItem("smtp_app_password", smtpAppPassword);
    localStorage.setItem("openai_api_key", openaiApiKey);

    try {
      const res = await axios.post(`${API_BASE_URL}/upload-csv-and-send/`, formData);
      setData([]);
      setResult(res.data);
      alert(
        `Done. Sent ${res.data.sent_count}/${res.data.total_rows} emails. Failed: ${res.data.failed_count}`
      );
    } catch (err) {
      const detail =
        err?.response?.data?.detail ||
        (err.message === "Network Error"
          ? `Cannot reach backend at ${API_BASE_URL}. Make sure backend is running.`
          : err.message);
      alert(`Failed to send emails: ${detail}`);
    } finally {
      setSending(false);
    }
  };

  return (
    <div>
      <h2>Upload CSV (auto-send emails)</h2>
      <input
        type="email"
        placeholder="SMTP email (Gmail)"
        value={smtpEmail}
        onChange={(e) => setSmtpEmail(e.target.value)}
      />
      <br />
      <input
        type="password"
        placeholder="SMTP app password"
        value={smtpAppPassword}
        onChange={(e) => setSmtpAppPassword(e.target.value)}
      />
      <br />
      <input
        type="password"
        placeholder="OpenAI API key (optional)"
        value={openaiApiKey}
        onChange={(e) => setOpenaiApiKey(e.target.value)}
      />
      <br />
      <input type="file" accept=".csv" onChange={handleFileUpload} disabled={sending} />

      <h3>Result:</h3>
      <pre>{JSON.stringify(result ?? data, null, 2)}</pre>

      {sending && <p>Sending emails...</p>}
    </div>
  );
}