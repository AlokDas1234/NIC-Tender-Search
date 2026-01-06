// import React from "react";

// const GetFields = () => {

//   const downloadExcel = () => {
//     window.location.href = "http://127.0.0.1:8000/api/client-fields-excel/";
//   };

//   return (
//     <div>
//       <h2>Download Client Fields Excel</h2>
//       <button onClick={downloadExcel}>
//         Download Excel
//       </button>
//     </div>
//   );
// };

// export default GetFields;

import React from "react";
import API from "./api";

const GetFields = () => {
  const downloadExcel = async () => {
    try {
      const res = await API.get("client-fields-excel/", {
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
      <h2>Download Client Fields Excel</h2>
      <button onClick={downloadExcel}>
        Download Excel
      </button>
    </div>
  );
};

export default GetFields;
