
import React from "react";
import API from "./api";

const GetAllField = () => {
  const downloadExcel = async () => {
    try {
      const res = await API.get("client-fields/", {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "client_fields.xlsx");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
      alert("❌ Download failed");
    }
  };

  return (
    <div>
      <h2>Download Demo Client Fields </h2>
      <button onClick={downloadExcel}>
        Download Excel
      </button>
    </div>
  );
};

export default GetAllField;
