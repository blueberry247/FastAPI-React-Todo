// Small helper used by the React components to call the FastAPI backend.
// It keeps fetch error handling in one place.
const apiRequest = async (url, options = {}) => {
  const response = await fetch(url, options);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  // DELETE requests may return a message, and other requests return JSON data.
  return response.json();
};

export default apiRequest;
