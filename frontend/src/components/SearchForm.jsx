import React, { useState } from "react";

export default function SearchForm({ onResults }) {
  const [src, setSrc] = useState("");
  const [dst, setDst] = useState("");

  async function handleSubmit(e) {
  e.preventDefault();

  const url = new URL("http://127.0.0.1:8000/search");
  url.searchParams.append("source", src);
  url.searchParams.append("destination", dst);

  try {
    const response = await fetch(url.toString(), {
      method: "GET",
    });

    if (!response.ok) {
      console.error("Backend error:", await response.text());
      return;
    }

    const data = await response.json();
    console.log("Results:", data);
    onResults(data);
  } catch (err) {
    console.error("Network error:", err);
  }
}


  return (
    <form onSubmit={handleSubmit}>
      <input value={src} onChange={e => setSrc(e.target.value)} />
      <input value={dst} onChange={e => setDst(e.target.value)} />
      <button type="submit">Search</button>
    </form>
  );
}
