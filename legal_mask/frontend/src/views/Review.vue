<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDocumentStore } from '../stores/document'
import { SENSITIVE_TYPE_COLORS, SENSITIVE_TYPE_LABELS } from '../types'
import { exportComparison, exportDocument } from '../api'
import type { Annotation } from '../types'

const route = useRoute()
const router = useRouter()
const store = useDocumentStore()
const docId = route.params.id as string
const comparing = ref(false)
const comparison = ref('')
const docIdRoute = docId

const pendingCount = computed(() => store.annotations.filter(a => a.status === 'pending').length)

onMounted(async () => { await store.loadDocument(docId) })

function getColor(type: string): string { return SENSITIVE_TYPE_COLORS[type] || '#95A5A6' }
function getLabel(type: string): string { return SENSITIVE_TYPE_LABELS[type] || type }

async function handleStatus(ann: Annotation, status: string) { await store.updateStatus(ann.id, status) }
async function confirmAll() { await store.doConfirmAll(docId) }

async function handleExport() { exportDocument(docId) }

async function handleCompare() {
  comparing.value = !comparing.value
  if (comparing.value) {
    const result = await exportComparison(docId)
    comparison.value = result.comparison
  }
}

function goBack() { router.push('/') }

function renderHighlighted(text: string): string {
  if (!store.annotations.length) return text
  const sorted = [...store.annotations].filter(a => a.status !== 'ignored').sort((a, b) => b.start - a.start)
  let result = text
  for (const ann of sorted) {
    const color = getColor(ann.sensitive_type)
    const label = getLabel(ann.sensitive_type)
    result = result.slice(0, ann.start) + `<mark style="background:${color}22; border-bottom:2px solid ${color};padding:0 2px;" title="${label}">` + result.slice(ann.start, ann.end) + `</mark>` + result.slice(ann.end)
  }
  return result
}
</script>

<template>
  <div v-if="store.currentDoc" class="review">
    <div class="review-header">
      <button class="back-btn" @click="goBack">← 返回</button>
      <h3>{{ store.currentDoc.filename }}</h3>
      <span class="progress">待审核: {{ pendingCount }} / {{ store.annotations.length }}</span>
    </div>

    <div class="review-body">
      <div class="original-pane">
        <h4>原文</h4>
        <div class="text-content" v-html="renderHighlighted(store.currentDoc.content || '')"></div>
      </div>
      <div class="annotations-pane" v-if="comparing">
        <h4>脱敏预览</h4>
        <pre class="comparison-text">{{ comparison }}</pre>
      </div>
    </div>

    <div class="annotations-list" v-if="store.annotations.length">
      <h4>标注列表</h4>
      <div v-for="ann in store.annotations" :key="ann.id" class="annotation-item">
        <span class="type-badge" :style="{ background: getColor(ann.sensitive_type) }">{{ getLabel(ann.sensitive_type) }}</span>
        <span class="ann-text">「{{ ann.text }}」</span>
        <span class="ann-source">({{ ann.source }}, {{ Math.round(ann.confidence * 100) }}%)</span>
        <span class="ann-status" v-if="ann.status !== 'pending'">{{ ann.status }}</span>
        <div class="ann-actions" v-if="ann.status === 'pending'">
          <button class="btn-confirm" @click="handleStatus(ann, 'confirmed')">✓ 确认</button>
          <button class="btn-ignore" @click="handleStatus(ann, 'ignored')">✗ 忽略</button>
        </div>
      </div>
    </div>

    <div class="review-actions">
      <button class="btn-primary" @click="confirmAll" :disabled="pendingCount === 0">全部确认 ({{ pendingCount }})</button>
      <button @click="handleCompare">{{ comparing ? '关闭预览' : '对比预览' }}</button>
      <button class="btn-export" @click="handleExport">导出脱敏文档</button>
    </div>
  </div>
</template>

<style scoped>
.review-header { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
.review-header h3 { flex: 1; }
.progress { font-size: 14px; color: #666; background: #e8f5e9; padding: 4px 12px; border-radius: 12px; }
.review-body { display: flex; gap: 16px; margin-bottom: 16px; }
.original-pane, .annotations-pane { flex: 1; background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; max-height: 500px; overflow-y: auto; }
.original-pane h4, .annotations-pane h4 { margin-bottom: 8px; font-size: 14px; color: #666; }
.text-content { line-height: 1.8; font-size: 14px; white-space: pre-wrap; word-break: break-all; }
.comparison-text { font-size: 13px; line-height: 1.6; white-space: pre-wrap; }
.annotations-list { background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin-bottom: 16px; max-height: 300px; overflow-y: auto; }
.annotations-list h4 { margin-bottom: 8px; font-size: 14px; color: #666; }
.annotation-item { display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
.type-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; color: white; font-size: 12px; }
.ann-text { font-weight: 500; }
.ann-source { color: #999; font-size: 12px; }
.ann-status { font-size: 12px; color: #2e7d32; }
.ann-actions { margin-left: auto; display: flex; gap: 4px; }
.btn-confirm, .btn-ignore { padding: 4px 12px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
.btn-confirm { background: #4ECDC4; color: white; }
.btn-ignore { background: #e0e0e0; color: #666; }
.review-actions { display: flex; gap: 12px; margin-top: 16px; }
.review-actions button { padding: 10px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
.btn-primary { background: #1a1a2e; color: white; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-export { background: #4ECDC4; color: white; }
.back-btn { background: none; border: none; cursor: pointer; font-size: 16px; color: #666; }
</style>
