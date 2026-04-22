<script setup>
import AppSidebar from '../components/layout/AppSidebar.vue'
import ChatBot from '../components/common/ChatBot.vue'
</script>

<template>
  <div class="app-layout">
    <AppSidebar />
    <main class="main-content">
      <Transition name="page" mode="out-in">
        <RouterView />
      </Transition>
    </main>
    <ChatBot />
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
}

.main-content {
  margin-left: 240px;
  flex: 1;
  overflow-y: auto;
  background-color: #f8fafc;
}

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>
