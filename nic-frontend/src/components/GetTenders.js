import React, { useState, useEffect } from "react";
import API from "./api";


const GetTenders = () => {
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [next, setNext] = useState(null);
  const [previous, setPrevious] = useState(null);
  const [totalPages, setTotalPages] = useState(1);

  const fetchTenders = async (pageNumber = 1) => {
    setLoading(true);
    try {
      const res = await API.get(`tenders/?page=${pageNumber}`);
      setTenders(res.data.results);
      setNext(res.data.next);
      setPrevious(res.data.previous);
      setPage(pageNumber);
      setTotalPages(res.data.total_pages); // ✅ NEW
    } catch (error) {
      console.error(error);
      alert("❌ Failed to fetch tenders");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchTenders(1);
  }, []);

  // ✅ DOWNLOAD VISIBLE TENDERS (CURRENT PAGE)
  const downloadVisibleTenders = () => {
    if (tenders.length === 0) {
      alert("No tenders to download");
      return;
    }

    const headers = Object.keys(tenders[0]).join(",");
    const rows = tenders.map(t =>
      Object.values(t)
        .map(val => `"${val ?? ""}"`)
        .join(",")
    );

    const csvContent = [headers, ...rows].join("\n");
    const blob = new Blob([csvContent], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `visible_tenders_page_${page}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // ✅ DOWNLOAD ALL TENDERS (BACKEND)
  const downloadAllTenders = () => {
    window.location.href =
      "http://127.0.0.1:8000/api/download-all-tenders/";
  };


  // const delTenders = async () => {
  //   const confirm = window.confirm(
  //     "⚠️ This will delete ALL tender data. Are you sure?"
  //   );
  //   if (!confirm) return;

  //   try {
  //     const res = await API.post("del-tenders/");
  //     alert("✅ All Uploaded Tenders deleted");
  //      fetchTenders(1);
  //     // console.log(res.data);
  //   } catch (err) {
  //     console.error(err);
  //     alert("❌ Failed to delete tender");
  //   }
  // };

  return (
    <div>
      <h2>Available Tenders</h2>

      {loading && <p>Loading...</p>}

      {tenders.length > 0 && (
        <>
          {/* DOWNLOAD BUTTONS */}
          <div style={{ marginBottom: "10px" }}>
            <button onClick={downloadVisibleTenders}>
              ⬇ Download Visible Tenders
            </button>

            <button
              onClick={downloadAllTenders}
              style={{ marginLeft: "10px" }}
            >
              ⬇ Download All Tenders
            </button>
            {/* <button
              onClick={delTenders}
              style={{ marginLeft: "10px" }}
            >
             Delete All Tender
            </button> */}

          </div>

          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>#</th>
                <th>Search Time</th>
                <th>Tender ID</th>
                <th>State</th>
                <th>Search Key</th>
                <th>Site Link</th>
                <th>Description</th>
                <th>Organization</th>
                <th>Bid End Date</th>
                <th>Bid End Time</th>
                <th>Value</th>
                <th>EMD</th>
                <th>Fee</th>
              </tr>
            </thead>
            <tbody>
              {tenders.map((t, index) => (
                <tr key={index}>
                  <td>{(page - 1) * 10 + index + 1}</td>
                  <td>{t.search_time}</td>
                  <td>{t.tender_id}</td>
                  <td>{t.state_name}</td>
                  <td>{t.search_key}</td>
                  <td>
                    <a href={t.site_link} target="_blank" rel="noreferrer">
                      Link
                    </a>
                  </td>
                  <td>{t.work_description}</td>
                  <td>{t.organization_chain}</td>
                  <td>{t.bid_submission_end_date}</td>
                  <td>{t.bid_submission_end_time}</td>
                  <td>{t.tender_value}</td>
                  <td>{t.emd_amt}</td>
                  <td>{t.tender_fee}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* PAGINATION */}
          <div style={{ marginTop: "15px" }}>
          <button
              onClick={() => fetchTenders( 1)}
              disabled={!previous}
            >
              ◀◀ First Page
            </button>
            <button
              onClick={() => fetchTenders(page - 1)}
              disabled={!previous}
            >
              ◀ Previous
            </button>
            
               <button
              onClick={() => fetchTenders(page - 1)}
              disabled={page - 2 < 1}
            >
              {page - 2}
            </button>
              <button
              onClick={() => fetchTenders(page - 1)}
             disabled={page - 1 < 1}
            >
              {page - 1}
            </button>

            <span style={{ margin: "0 10px" }}>
              Page {page}
            </span>

              <button
              onClick={() => fetchTenders(page + 1)}
              disabled={!next}
            >
              {page + 1}
            </button>
               <button
              onClick={() => fetchTenders(page + 1)}
              disabled={!next}
            >
              {page + 2}
            </button>

            <button
              onClick={() => fetchTenders(page + 1)}
              disabled={!next}
            >
              Next ▶
            </button>
             <button
            onClick={() => fetchTenders(totalPages)}
            disabled={page === totalPages}
          >
            Last Page ▶▶
          </button>

          </div>
        </>
      )}

      {!loading && tenders.length === 0 && <p>No tenders available.</p>}
    </div>
  );
};
export default GetTenders;
