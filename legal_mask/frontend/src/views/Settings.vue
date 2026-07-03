<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { SENSITIVE_TYPE_LABELS } from '../types'
import { getSettings, updateSettings } from '../api'

const enabledTypes = ref<Record<string, boolean>>({})
const saved = ref(false)
const loading = ref(true)

onMounted(async () => {
  try {
    const settings = await getSettings()
    const et: Record<string, boolean> = {}
    for (const key of Object.keys(SENSITIVE_TYPE_LABELS)) {
      et[key] = settings.enabled_types.includes(key)
    }
    enabledTypes.value = et
  } catch {
    for (const key of Object.keys(SENSITIVE_TYPE_LABELS)) {
      enabledTypes.value[key] = true
    }
  } finally {
    loading.value = false
  }
})

async function save() {
  const enabled = Object.entries(enabledTypes.value).filter(([, v]) => v).map(([k]) => k)
  try {
    await updateSettings({ enabled_types: enabled, mask_format: 'default' })
    saved.value = true
    setTimeout(() => saved.value = false, 2000)
  } catch {
    alert('保存失败')
  }
}
</script>

<template>
  <div class="settings">
    <h2>设置</h2>
    <section>
      <h3>敏感类型开关</h3>
      <p class="hint">取消勾选则不检测该类型</p>
      <div v-if="!loading" class="type-grid">
        <div v-for="(label, key) in SENSITIVE_TYPE_LABELS" :key="key" class="type-item">
          <input type="checkbox" :id="key" v-model="enabledTypes[key]" />
          <label :for="key">{{ label }}</label>
        </div>
      </div>
    </section>
    <section>
      <h3>数据安全</h3>
      <p>所有数据在本地处理，不会离开本机。程序退出时自动清理临时文件。</p>
    </section>
    <button class="save-btn" @click="save">{{ saved ? '已保存 ✓' : '保存设置' }}</button>
  </div>
</template>

<style scoped>
.settings { background: white; border-radius: 8px; padding: 24px; }
.settings h2 { margin-bottom: 20px; }
section { margin-bottom: 24px; }
section h3 { font-size: 15px; margin-bottom: 8px; color: #333; }
.hint { font-size: 13px; color: #999; margin-bottom: 8px; }
.type-grid { display: flex; flex-wrap: wrap; gap: 12px; }
.type-item { display: flex; align-items: center; gap: 6px; font-size: 14px; }
.save-btn { padding: 10px 24px; background: #1a1a2e; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
</style>
