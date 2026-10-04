// Function to upload Knowledge Base PDF to Python RAG service
export async function uploadKnowledgeBase(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/api/rag/upload', {
    method: 'POST',
    body: formData,
  });
  return response.json();
}

// Function to save Voice Agent configuration to Java Backend
export async function saveAgentConfig(config) {
  const response = await fetch('/api/agents/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  });
  return response.json();
}