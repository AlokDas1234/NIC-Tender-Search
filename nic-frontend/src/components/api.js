import axios from "axios";

const API = axios.create({
  baseURL: "/api/",
});

// Attach token automatically
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auto logout on 401
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default API;



// // Authentication based api.js
// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://127.0.0.1:8000/api/",
// });

// // 🔑 Automatically attach token to every request
// API.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem("token");
//     if (token) {
//       config.headers.Authorization = `Token ${token}`;
//     }
//     return config;
//   },
//   (error) => Promise.reject(error)
// );

// // 🚪 Auto logout on 401 (ADD THIS)
// API.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response?.status === 401) {
//       localStorage.removeItem("token");
//       window.location.href = "/login";
//     }
//     return Promise.reject(error);
//   }
// );

// export default API;




// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://127.0.0.1:8000/api/",
//   headers: {
//     "Content-Type": "multipart/form-data",
//   },
// });

// export default API;
