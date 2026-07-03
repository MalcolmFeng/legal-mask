<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDocumentStore } from '../stores/document'

const store = useDocumentStore()
const router = useRouter()
const dragOver = ref(false)

onMounted(() => store.fetchDocuments())

async function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files?.length) {
    const result = await store.uploadFile(input.files[0])
    router.push(`/review/${result.id}`)
  }
}

async function handleDrop(event: DragEvent) {
  dragOver.value = false
  const file = event.dataTransfer?.files[0]
  if (file) {
    const result = await store.uploadFile(file)
    router.push(`/review/${result.id}`)
  }
}

function openReview(id: string) { router.push(`/review/${id}`) }
</script>

<template>
  <div>
    <div class="upload-zone" :class="{ 'drag-over': dragOver }"
         @dragover.prevent="dragOver = true" @dragleave="dragOver = false"
         @drop.prevent="handleDrop">
      <p>拖拽文件到此处上传</p>
      <p class="sub">支持 .docx .pdf .xlsx .txt</p>
      <label class="upload-btn">
        选择文件
        <input type="file" hidden accept=".docx,.pdf,.xlsx,.txt,.md,.csv" @change="handleFileUpload" />
      </label>
    </div>

    <div v-if="store.documents.length" class="file-list">
      <h3>已上传文件</h3>
      <table>
        <thead><tr><th>文件名</th><th>类型</th><th>大小</th><th>状态</th><th>操作</th></tr></thead>
        <tbody>
          <tr v-for="doc in store.documents" :key="doc.id">
            <td>{{ doc.filename }}</td>
            <td>{{ doc.file_type }}</td>
            <td>{{ doc.content_length }}B</td>
            <td><span class="status-badge">{{ doc.annotation_count }} 处标注</span></td>
            <td><button @click="openReview(doc.id)">审核</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.upload-zone { border: 2px dashed #ccc; border-radius: 12px; padding: 48px; text-align: center; background: white; transition: all 0.2s; cursor: pointer; }
.upload-zone.drag-over { border-color: #4ECDC4; background: #f0fdfa; }
.sub { font-size: 13px; color: #999; margin-top: 4px; }
.upload-btn { display: inline-block; margin-top: 16px; padding: 10px 24px; background: #1a1a2e; color: white; border-radius: 6px; cursor: pointer; font-size: 14px; }
.file-list { margin-top: 24px; background: white; border-radius: 8px; padding: 16px; }
.file-list h3 { margin-bottom: 12px; font-size: 16px; }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #eee; font-size: 14px; }
th { font-weight: 600; color: #666; }
button { padding: 6px 16px; background: #4ECDC4; color: white; border: none; border-radius: 4px; cursor: pointer; }
.status-badge { padding: 2px 8px; background: #e8f5e9; color: #2e7d32; border-radius: 4px; font-size: 12px; }
</style>
