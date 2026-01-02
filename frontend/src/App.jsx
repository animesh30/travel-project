import React, { useState } from "react";
import SearchForm from "./components/SearchForm";
import Results from "./components/Results";

export default function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  return (
    <div className="container">
      <h1>🚆 Travel Route Mixer</h1>
      <SearchForm setResults={setResults} setLoading={setLoading} />
      {loading && <p>Loading routes...</p>}
      <Results results={results} />
    </div>
  );
}
