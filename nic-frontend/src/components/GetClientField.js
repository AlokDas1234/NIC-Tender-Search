import React from "react";

const GetFields = () => {

  const downloadExcel = () => {
    window.location.href = "http://127.0.0.1:8000/api/client-fields-excel/";
  };

  return (
    <div>
      <h2>Download Client Fields Excel</h2>
      <button onClick={downloadExcel}>
        Download Excel
      </button>
    </div>
  );
};

export default GetFields;
