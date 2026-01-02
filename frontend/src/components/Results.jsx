import React from "react";

export default function Results({ results }) {
  if (!results.length) return null;

  return (
    <div className="results">
      <h2>Available Itineraries</h2>

      {results.map((route, index) => (
        <div key={index} className="card">
          <p><strong>Total Price:</strong> ₹{route.total_price}</p>
          <p><strong>Total Duration:</strong> {route.total_duration_min} mins</p>
          <p><strong>Transfers:</strong> {route.transfers}</p>

          <ul>
            {route.legs.map((leg, i) => (
              <li key={i}>
                {leg.src} → {leg.dst} ({leg.mode}) | ₹{leg.price}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
