<script setup lang="ts">
import { ref } from 'vue'
import { SENSITIVE_TYPE_LABELS } from '../types'

const saved = ref(false)
function save() {
  saved.value = true
  setTimeout(() => saved.value = false, 2000)
}
</script>

<template>
  <div class="settings">
    <h2>设置</h2>
    <section>
      <h3>敏感类型开关</h3>
      <div class="type-grid">
        <div v-for="(label, key) in SENSITIVE_TYPE_LABELS" :key="key" class="type-item">
          <input type="checkbox" :id="key" checked />
          <label :for="key">{{ label }}</label>
        </div>
      </div>
    </section>
    <section>
      <h3>数据安全</h3>
      <p>所有数据在本地处理，不会离开本机。</p>
    </section>
    <button class="save-btn" @click="save">{{ saved ? '已保存 ✓' : '保存设置' }}</button>
  </div>
</template>

<style scoped>
.settings { background: white; border-radius: 8px; padding: 24px; }
.settings h2 { margin-bottom: 20px; }
section { margin-bottom: 24px; }
section h3 { font-size: 15px; margin-bottom: 8px; color: #333; }
.type-grid { display: flex; flex-wrap: wrap; gap: 12px; }
.type-item { display: flex; align-items: center; gap: 6px; font-size: 14px; }
.save-btn { padding: 10px 24px; background: #1a1a2e; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
</style>
