<script setup lang="ts">
import { onMounted } from 'vue'
import { useDocumentStore } from './stores/document'
const store = useDocumentStore()
onMounted(() => store.fetchDocuments())
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>legal-mask</h1>
      <nav>
        <router-link to="/">工作台</router-link>
        <router-link to="/settings">设置</router-link>
      </nav>
    </header>
    <main><router-view /></main>
  </div>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; color: #333; }
.header { background: #1a1a2e; color: white; padding: 16px 24px; display: flex; align-items: center; gap: 32px; }
.header h1 { font-size: 20px; font-weight: 600; }
.header nav { display: flex; gap: 16px; }
.header nav a { color: #ccc; text-decoration: none; font-size: 14px; }
.header nav a:hover { color: white; }
main { padding: 24px; }
</style>
