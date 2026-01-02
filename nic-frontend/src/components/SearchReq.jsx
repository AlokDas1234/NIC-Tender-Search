
import React, { useState,useEffect } from "react";
import API from "./api";
import Dashboard from "./Dashboard";
import AddControl from "./AddControl";
import GetFields from "./GetClientField";
import GetAllField from "./GetClientAllField";

const GetSearcReq = () => {
  const [req, setReq] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchClientSearchReq = async () => {
    setLoading(true);
    try {
      const res = await API.get("search/");
      console.log("search data",res.data)
      setReq(res.data);

    } catch (error) {
      console.error(error);
      alert("❌ Unauthorized or failed");
    }
    setLoading(false);
  };

   useEffect(()=>{
    fetchClientSearchReq()

  },[]);

  const delsearch = async () => {
    const confirm = window.confirm(
      "⚠️ This will delete ALL search req. Are you sure?"
    );
    if (!confirm) return;

    try {
      const res = await API.post("del-search/");
      alert("✅ All data deleted");
       fetchClientSearchReq()
       
      // console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Failed to delete");
    }
  };

  

const runScraperForSearch = async (searchId) => {
  try {
    const res = await API.post(`run-scraper/${searchId}/`);
    alert("✅ Scraper started");
    console.log(res.data);
  } catch (err) {
    console.error(err);
    alert("❌ Failed to start scraper");
  }
};

const delScraperForSearch = async (searchId,state_name) => {
  try {
    const res = await API.post(`del-scraper/${searchId}/`);
   const confirm = window.confirm(
      `⚠️ This will delete  req for ${state_name} Are you sure?`
    );
    if (!confirm) return;
       fetchClientSearchReq()
  } catch (err) {
    console.error(err);
    alert("❌ Failed to delete req");
  }
};


const [showAdd, setShowAdd] = useState(false);


const startScraper = async () => {
    try {
      const res = await API.post("run-scraper/"); // Calls your Django start endpoint
      alert("✅ Scraper started");
      console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Failed to start scraper");
    }};

 const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("upload-search-req/", formData);
      alert("✅ Uploaded successfully");
       fetchClientSearchReq()
      console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("❌ Upload failed");
    }
  };

  return (
    <div>
      <Dashboard/>
      <h2>Search  Requirements</h2>      
      <button onClick={startScraper}>Run All Scrape</button>

   
      <GetFields/>
      <GetAllField/>

      <h2>Add Requirements</h2>
      <button onClick={() => setShowAdd(true)}>Add Requirement</button>

{showAdd && (
  <AddControl
    onSuccess={fetchClientSearchReq}
    onClose={() => setShowAdd(false)}
  />
)}


    <h2>Upload Requirement</h2>
<input type="file" onChange={handleUpload} />

    <h2>Delete Requirement</h2>
<button onClick={delsearch}>Delete Req</button>


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
              <th>Run Each Tender</th>
              <th>Delete Each Tender</th>
            
              {/* <th>Searching State Name</th>
              <th>Searching Keyword</th> */}
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
                <td>{<button onClick={()=>runScraperForSearch(r.id)}>Run</button>}</td>
          
                <td>{<button onClick={()=>delScraperForSearch(r.id,r.state_name)}>Delete</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {req.length === 0 && !loading && <p>No Search  Requirements available.</p>}
    </div>
  );
};
export default GetSearcReq;