<template>
  <div class="error-banner" role="alert">
    <span class="error-icon" aria-hidden="true">⚠️</span>
    <span class="error-message">{{ message }}</span>
    <button class="error-dismiss" @click="$emit('dismiss')" aria-label="Dismiss error">×</button>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, required: true },
})
defineEmits(['dismiss'])
</script>

<style scoped>
.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background-color: #fef2f2;
  border: 1px solid #fca5a5;
  border-radius: 8px;
  color: #991b1b;
  animation: fadeIn 0.2s ease-in;
}

.error-icon {
  flex-shrink: 0;
  font-size: 1rem;
  line-height: 1;
}

.error-message {
  flex: 1;
  font-size: 0.875rem;
  line-height: 1.5;
}

.error-dismiss {
  flex-shrink: 0;
  background: none;
  border: none;
  cursor: pointer;
  color: #991b1b;
  font-size: 1.25rem;
  line-height: 1;
  padding: 0 4px;
  border-radius: 4px;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.error-dismiss:hover {
  background-color: #fee2e2;
  color: #7f1d1d;
}

.error-dismiss:focus-visible {
  outline: 2px solid #ef4444;
  outline-offset: 2px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
