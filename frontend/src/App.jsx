import { useState } from "react";
import SearchForm from "./components/SearchForm";
import Results from "./components/Results";

function App() {
  const [results, setResults] = useState([]);

  return (
    <div>
      <h1>Travel Route Finder</h1>

      <SearchForm onResults={setResults} />

      <Results data={results} />
    </div>
  );
}

export default App;
