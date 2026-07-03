import type { DocumentInfo, Annotation } from '../types'

const BASE = '/api'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function uploadDocument(file: File): Promise<DocumentInfo> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${BASE}/documents/upload`, { method: 'POST', body: form })
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
  return res.json()
}

export async function listDocuments(): Promise<DocumentInfo[]> {
  return request('/documents')
}

export async function getDocument(id: string): Promise<DocumentInfo> {
  return request(`/documents/${id}`)
}

export async function updateAnnotationStatus(annId: string, status: string): Promise<Annotation> {
  return request(`/annotations/${annId}/status`, { method: 'PUT', body: JSON.stringify({ status }) })
}

export async function confirmAll(docId: string): Promise<{ annotations: Annotation[] }> {
  return request(`/annotations/confirm-all/${docId}`, { method: 'PUT' })
}

export async function addManualAnnotation(docId: string, start: number, end: number, text: string, sensitiveType: string): Promise<Annotation> {
  return request('/annotations', { method: 'POST', body: JSON.stringify({ doc_id: docId, start, end, text, sensitive_type: sensitiveType }) })
}

export async function removeAnnotation(annId: string): Promise<void> {
  await request(`/annotations/${annId}`, { method: 'DELETE' })
}

export async function getPendingCount(docId: string): Promise<{ pending_count: number }> {
  return request(`/annotations/pending-count/${docId}`)
}

export async function exportDocument(docId: string): Promise<void> {
  window.open(`${BASE}/export/${docId}`, '_blank')
}

export async function exportComparison(docId: string): Promise<{ comparison: string }> {
  return request(`/export/comparison/${docId}`, { method: 'POST' })
}

export async function getSettings(): Promise<{ enabled_types: string[]; mask_format: string }> {
  return request('/settings')
}

export async function updateSettings(data: { enabled_types: string[]; mask_format: string }): Promise<{ enabled_types: string[]; mask_format: string }> {
  return request('/settings', { method: 'PUT', body: JSON.stringify(data) })
}
