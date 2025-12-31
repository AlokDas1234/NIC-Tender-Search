
//Authentication based api.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// 🔑 Automatically attach token
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // or access_token
    if (token) {
      config.headers.Authorization = `Token ${token}`;
      // If JWT → `Bearer ${token}`
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default API;




// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://127.0.0.1:8000/api/",
//   headers: {
//     "Content-Type": "multipart/form-data",
//   },
// });

// export default API;
