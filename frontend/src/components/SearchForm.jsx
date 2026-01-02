import React, { useState } from "react";
import { searchRoutes } from "../api";

export default function SearchForm({ setResults, setLoading }) {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await searchRoutes(source, destination);
      setResults(data.itineraries || []);
    } catch (err) {
      alert("Error fetching routes");
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <input
        placeholder="Source (e.g. A)"
        value={source}
        onChange={(e) => setSource(e.target.value)}
        required
      />
      <input
        placeholder="Destination (e.g. C)"
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
        required
      />
      <button type="submit">Search</button>
    </form>
  );
}
