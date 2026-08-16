// Small helper used by the React components to call the FastAPI backend.
// It keeps fetch error handling in one place.
const apiRequest = async (url, options = {}) => {
  const token = localStorage.getItem("taskapp_token");
  const headers = new Headers(options.headers || {});

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem("taskapp_token");
      window.dispatchEvent(new Event("taskapp:unauthorized"));
    }

    throw new Error(`Request failed: ${response.status}`);
  }

  // DELETE requests may return a message, and other requests return JSON data.
  return response.json();
};

export default apiRequest;
