<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const selMenu = ref(false)
const selTop = ref(0)
const selLeft = ref(0)
const selText = ref('')
const selStart = ref(0)
const selEnd = ref(0)

const pendingCount = computed(() => store.annotations.filter(a => a.status === 'pending').length)

onMounted(async () => { await store.loadDocument(docId) })
onUnmounted(() => { document.removeEventListener('mousedown', handleOutsideClick) })

function handleTextMouseup(e: MouseEvent) {
  const sel = window.getSelection()
  if (!sel || sel.isCollapsed || !sel.toString().trim()) {
    selMenu.value = false
    return
  }
  const text = sel.toString().trim()
  const content = store.currentDoc?.content || ''
  let idx = content.indexOf(text)
  if (idx === -1) {
    idx = content.indexOf(text.replace(/\s+/g, ''))
    if (idx === -1) { selMenu.value = false; return }
  }
  selText.value = text
  selStart.value = idx
  selEnd.value = idx + text.length
  selTop.value = e.clientY + 6
  selLeft.value = e.clientX
  selMenu.value = true
  setTimeout(() => document.addEventListener('mousedown', handleOutsideClick), 0)
}

function handleOutsideClick(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.sel-popup') && !target.closest('.text-content')) {
    selMenu.value = false
    document.removeEventListener('mousedown', handleOutsideClick)
  }
}

async function markSelection(type: string) {
  await store.addAnnotation(docId, selStart.value, selEnd.value, selText.value, type)
  selMenu.value = false
  document.removeEventListener('mousedown', handleOutsideClick)
}

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

function escapeHtml(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;')
}

function renderHighlighted(text: string): string {
  const safe = escapeHtml(text)
  if (!store.annotations.length) return safe
  const sorted = [...store.annotations].filter(a => a.status !== 'ignored').sort((a, b) => b.start - a.start)
  let result = safe
  for (const ann of sorted) {
    const color = getColor(ann.sensitive_type)
    const label = getLabel(ann.sensitive_type)
    const annText = escapeHtml(result.slice(ann.start, ann.end))
    result = result.slice(0, ann.start) + `<mark style="background:${color}22;border-bottom:2px solid ${color};padding:0 2px;" title="${escapeHtml(label)}">` + annText + `</mark>` + result.slice(ann.end)
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
        <h4>原文 <span class="hint">（选中文字可手动标记为敏感内容）</span></h4>
        <div class="text-content" v-html="renderHighlighted(store.currentDoc.content || '')" @mouseup="handleTextMouseup"></div>
      </div>
      <div class="right-pane">
        <div class="annotations-list" v-if="store.annotations.length">
          <h4>标注列表</h4>
          <div class="ann-scroll">
            <div v-for="ann in store.annotations" :key="ann.id" class="annotation-item">
              <span class="type-badge" :style="{ background: getColor(ann.sensitive_type) }">{{ getLabel(ann.sensitive_type) }}</span>
              <span class="ann-text">「{{ ann.text }}」</span>
              <span class="ann-source">({{ ann.source }}, {{ Math.round(ann.confidence * 100) }}%)</span>
              <span class="ann-status" v-if="ann.status !== 'pending'">{{ ann.status === 'confirmed' ? '已确认' : '已忽略' }}</span>
              <div class="ann-actions" v-if="ann.status === 'pending'">
                <button class="btn-confirm" @click="handleStatus(ann, 'confirmed')">✓</button>
                <button class="btn-ignore" @click="handleStatus(ann, 'ignored')">✗</button>
              </div>
            </div>
          </div>
        </div>
        <div class="annotations-pane" v-if="comparing">
          <h4>脱敏预览</h4>
          <pre class="comparison-text">{{ comparison }}</pre>
        </div>
        <div class="review-actions">
          <button class="btn-primary" @click="confirmAll" :disabled="pendingCount === 0">全部确认</button>
          <button @click="handleCompare">{{ comparing ? '关闭预览' : '对比预览' }}</button>
          <button class="btn-export" @click="handleExport">导出</button>
        </div>
      </div>
    </div>

    <div v-if="selMenu" class="sel-popup" :style="{ top: selTop + 'px', left: selLeft + 'px' }">
      <div class="sel-label">标记为：</div>
      <div class="sel-types">
        <button v-for="(label, key) in SENSITIVE_TYPE_LABELS" :key="key"
                class="sel-btn" :style="{ borderColor: getColor(key) }"
                @click="markSelection(key)">{{ label }}</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.review-header { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; flex-shrink: 0; }
.review-header h3 { flex: 1; font-size: 16px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.progress { font-size: 13px; color: #666; background: #e8f5e9; padding: 4px 12px; border-radius: 12px; white-space: nowrap; }
.review-body { display: flex; gap: 16px; height: calc(100vh - 160px); }
.original-pane { flex: 1; background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; display: flex; flex-direction: column; overflow: hidden; }
.original-pane h4 { margin-bottom: 8px; font-size: 14px; color: #666; flex-shrink: 0; }
.text-content { flex: 1; overflow-y: auto; line-height: 1.8; font-size: 14px; white-space: pre-wrap; word-break: break-all; }
.right-pane { width: 360px; display: flex; flex-direction: column; gap: 12px; }
.annotations-list { background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.annotations-list h4 { margin-bottom: 8px; font-size: 14px; color: #666; flex-shrink: 0; }
.ann-scroll { flex: 1; overflow-y: auto; }
.annotation-item { display: flex; align-items: center; gap: 6px; padding: 6px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
.type-badge { display: inline-block; padding: 1px 6px; border-radius: 4px; color: white; font-size: 11px; white-space: nowrap; flex-shrink: 0; }
.ann-text { font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0; }
.ann-source { color: #999; font-size: 11px; white-space: nowrap; }
.ann-status { font-size: 11px; color: #2e7d32; white-space: nowrap; }
.ann-actions { margin-left: auto; display: flex; gap: 2px; flex-shrink: 0; }
.btn-confirm, .btn-ignore { padding: 2px 8px; border: none; border-radius: 3px; cursor: pointer; font-size: 12px; }
.btn-confirm { background: #4ECDC4; color: white; }
.btn-ignore { background: #e0e0e0; color: #666; }
.review-actions { display: flex; gap: 8px; flex-wrap: wrap; flex-shrink: 0; }
.review-actions button { padding: 8px 14px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; flex: 1; min-width: 0; }
.btn-primary { background: #1a1a2e; color: white; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-export { background: #4ECDC4; color: white; }
.back-btn { background: none; border: none; cursor: pointer; font-size: 16px; color: #666; flex-shrink: 0; }
.comparison-text { font-size: 13px; line-height: 1.6; white-space: pre-wrap; }
.annotations-pane { background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.annotations-pane h4 { margin-bottom: 8px; font-size: 14px; color: #666; flex-shrink: 0; }
.hint { font-size: 12px; color: #999; font-weight: normal; }
.text-content { flex: 1; overflow-y: auto; line-height: 1.8; font-size: 14px; white-space: pre-wrap; word-break: break-all; cursor: text; }
.text-content::selection { background: #b3d4fc; }
.sel-popup { position: fixed; z-index: 1000; background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 8px 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); max-width: 320px; }
.sel-label { font-size: 11px; color: #999; margin-bottom: 6px; }
.sel-types { display: flex; flex-wrap: wrap; gap: 4px; }
.sel-btn { padding: 3px 8px; border: 1px solid; border-radius: 4px; background: white; cursor: pointer; font-size: 11px; white-space: nowrap; }
.sel-btn:hover { background: #f5f5f5; }
</style>
