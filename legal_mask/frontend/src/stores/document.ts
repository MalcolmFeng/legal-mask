import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DocumentInfo, Annotation } from '../types'
import * as api from '../api'

export const useDocumentStore = defineStore('document', () => {
  const documents = ref<DocumentInfo[]>([])
  const currentDoc = ref<DocumentInfo | null>(null)
  const annotations = ref<Annotation[]>([])
  const loading = ref(false)

  async function fetchDocuments() { documents.value = await api.listDocuments() }

  async function uploadFile(file: File) {
    loading.value = true
    try {
      const result = await api.uploadDocument(file)
      await fetchDocuments()
      return result
    } finally { loading.value = false }
  }

  async function loadDocument(id: string) {
    loading.value = true
    try {
      const doc = await api.getDocument(id)
      currentDoc.value = doc
      annotations.value = doc.annotations || []
    } finally { loading.value = false }
  }

  async function updateStatus(annId: string, status: string) {
    const updated = await api.updateAnnotationStatus(annId, status)
    const idx = annotations.value.findIndex(a => a.id === annId)
    if (idx !== -1) annotations.value[idx] = updated
  }

  async function doConfirmAll(docId: string) {
    const result = await api.confirmAll(docId)
    annotations.value = result.annotations
  }

  async function addAnnotation(docId: string, start: number, end: number, text: string, type: string) {
    const ann = await api.addManualAnnotation(docId, start, end, text, type)
    annotations.value.push(ann)
  }

  async function removeAnnotation(annId: string) {
    await api.removeAnnotation(annId)
    annotations.value = annotations.value.filter(a => a.id !== annId)
  }

  return { documents, currentDoc, annotations, loading, fetchDocuments, uploadFile, loadDocument, updateStatus, doConfirmAll, addAnnotation, removeAnnotation }
})
