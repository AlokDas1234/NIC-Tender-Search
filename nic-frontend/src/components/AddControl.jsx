import React, { useState } from "react";
import API from "./api";

function AddControl({ onSuccess, onClose }) {
  const [form, setForm] = useState({
    site_url: "",
    search_key: "",
    exclude_key: "",
    state_name: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const addReq = async () => {
    try {
      await API.post("add-search-req/", form);
      alert("✅ Requirement added");
      onSuccess(); // refresh table
      onClose();   // close form
    } catch (err) {
      console.error(err);
      alert("❌ Failed to add requirement");
    }
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "15px", margin: "15px 0" }}>
      <h3>Add Tender Search Data</h3>

      <input
        type="text"
        name="site_url"
        placeholder="Site URL"
        value={form.site_url}
        onChange={handleChange}
      /><br />

      <input
        type="text"
        name="search_key"
        placeholder="Search Keys"
        value={form.search_key}
        onChange={handleChange}
      /><br />

      <input
        type="text"
        name="exclude_key"
        placeholder="Exclude Keys"
        value={form.exclude_key}
        onChange={handleChange}
      /><br />

      <input
        type="text"
        name="state_name"
        placeholder="State Name"
        value={form.state_name}
        onChange={handleChange}
      /><br /> <br />

      <button onClick={addReq}>Add</button>
      <button onClick={onClose} style={{ marginLeft: "10px" }}>Cancel</button>
    </div>
  );
}

export default AddControl;
