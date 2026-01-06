
import React, { useState,useEffect } from "react";
import API from "./api";
const GetReq = () => {
  const [req, setReq] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchClientReq = async () => {
    setLoading(true);
    try {
      const res = await API.get("clients/");
      setReq(res.data);
    } catch (error) {
      console.error(error);
      alert("❌ Unauthorized or failed");
    }
    setLoading(false);
  };

   useEffect(()=>{
    fetchClientReq()

  },[]);


       
const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("upload-clients/", formData);
      alert("✅ Uploaded successfully");
         fetchClientReq();
      console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Upload failed");
    }
  };


   const delReq = async () => {
    const confirm = window.confirm(
      "⚠️ This will delete ALL Requirements data. Are you sure?"
    );
    if (!confirm) return;

    try {
      const req = await API.post("del-req/");
      alert("✅ All Uploaded Requirements deleted");
      console.log(req.data);
         fetchClientReq();
    } catch (err) {
      console.error(err);
      alert("❌ Failed to delete requirements");
    }
  };

function   delPrticularReq(id){
  console.log(" Del particular req called: ",id)

}
  
  return (
    <div>
      <h2>Client Requirements</h2>
      {/* <button onClick={fetchClientReq}>Load Requirement</button> */}
    <h3>Upload Client Excel / CSV</h3>
       <input type="file" onChange={handleUpload} />
       <h3>Delete All Requirement</h3>
       <button onClick={delReq}>Delete All Requirement</button>

      {loading && <p>Loading...</p>}

      {req.length > 0 && (
        <table border="1" cellPadding="5" style={{ marginTop: "20px" }}>
          <thead>
            <tr>
              <th>SL No</th>
              <th>Site Link</th>
              <th>Search Key</th>
              <th>Exclude Key</th>
              <th>State Name</th>
              <th>Delete Operation</th>
            </tr>
          </thead>
          <tbody>
            {req.map((r, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>
                  <a href={r.site_url} target="_blank" rel="noreferrer">
                    {r.site_url}
                  </a>
                </td>
                <td>{r.search_key}</td>
                <td>{r.exclude_key}</td>
                <td>{r.state_name}</td>
                <td>{<button onClick={()=>delPrticularReq(r.index)}>Delete</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {req.length === 0 && !loading && <p>No Requirements available.</p>}
    </div>
  );
};

export default GetReq;




// import React, { useState } from "react";

// const GetReq = () => {
//   const [req, setReq] = useState([]);
//   const [loading, setLoading] = useState(false);

//   const fetchClientReq = async () => {
//     setLoading(true);
//     try {
//       const response = await fetch("http://127.0.0.1:8000/api/clients/");
//       const data = await response.json();
//       setReq(data);
//     } catch (error) {
//       console.error("Error fetching client data:", error);
//     }
//     setLoading(false);
//   };

//   return (
//     <div>
//       <h2>Client Requirements</h2>
//       <button onClick={fetchClientReq}>Load Requirement</button>

//       {loading && <p>Loading...</p>}

//       {req.length > 0 && (
//         <table border="1" cellPadding="5" style={{ marginTop: "20px" }}>
//           <thead>
//             <tr>
//               <th>SL No</th>
//               <th>Site Link</th>
//               <th>Search Key</th>
//               <th>Exclude Key</th>
//               <th>State Name</th>    
           
//             </tr>
//           </thead>
//           <tbody>
//             {req.map((req, index) => (
//               <tr key={index}>
//                 <td>{index + 1}</td>
//                 <td><a href={req.site_url} target="_blank" rel="noreferrer">
//                     {req.site_url}
//                   </a></td>
//                 <td>{req.search_key}</td>
//                 <td>{req.exclude_key}</td>
//                 <td>{req.state_name}</td>
               
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       )}

//       {req.length === 0 && !loading && <p>No Requiremenrs available.</p>}
//     </div>
//   );
// };

// export default GetReq;
