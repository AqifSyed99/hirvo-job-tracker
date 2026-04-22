<template>
  <Teleport to="body">
    <div class="toast-container" aria-live="polite" aria-atomic="false">
      <TransitionGroup name="toast" tag="div" class="toast-list">
        <div
          v-for="toast in toastStore.toasts"
          :key="toast.id"
          class="toast"
          :class="`toast--${toast.type}`"
          role="alert"
        >
          <span class="toast-icon" aria-hidden="true">{{ icons[toast.type] }}</span>
          <span class="toast-message">{{ toast.message }}</span>
          <button
            class="toast-close"
            @click="toastStore.remove(toast.id)"
            aria-label="Dismiss"
          >×</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToastStore } from '../../store/toast'

const toastStore = useToastStore()

const icons = {
  success: '✅',
  error:   '❌',
  warning: '⚠️',
  info:    'ℹ️',
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 10px;
  min-width: 280px;
  max-width: 380px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  pointer-events: all;
  font-size: 0.875rem;
  font-weight: 500;
  border-left: 4px solid transparent;
}

.toast--success {
  background: #f0fdf4;
  color: #166534;
  border-left-color: #22c55e;
}

.toast--error {
  background: #fef2f2;
  color: #991b1b;
  border-left-color: #ef4444;
}

.toast--warning {
  background: #fffbeb;
  color: #92400e;
  border-left-color: #f59e0b;
}

.toast--info {
  background: #eff6ff;
  color: #1e40af;
  border-left-color: #3b82f6;
}

.toast-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  line-height: 1;
  padding: 0 2px;
  border-radius: 4px;
  opacity: 0.5;
  transition: opacity 0.15s ease;
  flex-shrink: 0;
  color: inherit;
}

.toast-close:hover {
  opacity: 1;
}

/* TransitionGroup animations */
.toast-enter-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
.toast-move {
  transition: transform 0.2s ease;
}
</style>
