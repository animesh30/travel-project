export default function Results({ data }) {
  console.log("Results component received:", data);
  if (!data || data.length === 0) {
    return <p>No results found</p>;
  }

  return (
    <div>
      {data.map((item, index) => (
        <div key={index}>
          <h4>Total Price: ₹{item.total_price}</h4>
          <p>Duration: {item.total_duration_min} mins</p>
        </div>
      ))}
    </div>
  );
}
