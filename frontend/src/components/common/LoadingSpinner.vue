<template>
  <div class="spinner-wrapper">
    <div class="spinner" :class="`spinner--${size}`"></div>
    <p v-if="message" class="spinner-message">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  size: { type: String, default: 'md' },
  message: { type: String, default: '' },
})
</script>

<style scoped>
.spinner-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.spinner {
  border-radius: 50%;
  border: 3px solid #e5e7eb;
  border-top-color: #6366f1;
  animation: spin 0.75s linear infinite;
}

.spinner--sm {
  width: 24px;
  height: 24px;
  border-width: 2px;
}

.spinner--md {
  width: 40px;
  height: 40px;
  border-width: 3px;
}

.spinner--lg {
  width: 64px;
  height: 64px;
  border-width: 4px;
}

.spinner-message {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
