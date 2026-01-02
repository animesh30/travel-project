const BASE_URL = "http://127.0.0.1:8000";

export async function searchRoutes(source, destination) {
  const response = await fetch(
    `${BASE_URL}/search?source=${source}&destination=${destination}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch routes");
  }

  return response.json();
}
