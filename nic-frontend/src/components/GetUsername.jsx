import React, { useState, useEffect } from "react";

function GetUserInfo() {
  const [username, setUsername] = useState("");

  useEffect(() => {
    const storedUsername = localStorage.getItem("username");
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []); // runs once when component mounts

  return (
    <>
      <h1>{username}</h1>
    </>
  );
}

export default GetUserInfo;
