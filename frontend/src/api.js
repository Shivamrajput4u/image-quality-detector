const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function readErrorMessage(response) {
  try {
    const body = await response.json();
    return body.detail || `Request failed with status ${response.status}`;
  } catch {
    return `Request failed with status ${response.status}`;
  }
}

export async function analyzeImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return response.json();
}

export async function fetchHistory(limit = 24, offset = 0) {
  const response = await fetch(`${API_BASE_URL}/api/analyses?limit=${limit}&offset=${offset}`);
  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return response.json();
}

export function resolveImageUrl(imageUrl) {
  return `${API_BASE_URL}${imageUrl}`;
}
