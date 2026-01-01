
import React, { useState } from "react";

function App() {
	const [source, setSource] = useState("");
	const [destination, setDestination] = useState("");
	const [results, setResults] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");

	const handleSubmit = async (e) => {
		e.preventDefault();
		setLoading(true);
		setError("");
		setResults([]);
		try {
			const res = await fetch("http://localhost:8000/search", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ source, destination }),
			});
			if (!res.ok) throw new Error("API error");
			const data = await res.json();
			setResults(data);
		} catch (err) {
			setError("Failed to fetch routes");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
			<h2>Travel Route Search</h2>
			<form onSubmit={handleSubmit} style={{ marginBottom: 24 }}>
				<input
					placeholder="Source"
					value={source}
					onChange={e => setSource(e.target.value)}
					style={{ marginRight: 8 }}
					required
				/>
				<input
					placeholder="Destination"
					value={destination}
					onChange={e => setDestination(e.target.value)}
					style={{ marginRight: 8 }}
					required
				/>
				<button type="submit" disabled={loading}>
					{loading ? "Searching..." : "Search"}
				</button>
			</form>
			{error && <div style={{ color: "red" }}>{error}</div>}
			{results.length > 0 && (
				<div>
					<h3>Results</h3>
					{results.map((it, idx) => (
						<div key={idx} style={{ border: "1px solid #ccc", padding: 12, marginBottom: 12 }}>
							<div><b>Legs:</b></div>
							<ul>
								{it.legs.map((leg, i) => (
									<li key={i}>
										{leg.source} → {leg.destination} ({leg.mode}, ₹{leg.price}, {leg.duration_min} min, {leg.available ? "Available" : "Unavailable"})
									</li>
								))}
							</ul>
							<div>Total Price: ₹{it.total_price}</div>
							<div>Total Duration: {it.total_duration_min} min</div>
							<div>All Legs Available: {it.all_legs_available ? "Yes" : "No"}</div>
						</div>
					))}
				</div>
			)}
		</div>
	);
}

export default App;
