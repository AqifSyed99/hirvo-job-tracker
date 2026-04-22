<template>
  <Teleport to="body">
    <div
      class="delete-dialog__overlay"
      @click.self="$emit('cancel')"
      role="dialog"
      aria-modal="true"
      aria-labelledby="delete-dialog-title"
      aria-describedby="delete-dialog-desc"
    >
      <div class="delete-dialog__card">
        <div class="delete-dialog__icon" aria-hidden="true">⚠️</div>
        <h2 id="delete-dialog-title" class="delete-dialog__title">Delete Application</h2>
        <p id="delete-dialog-desc" class="delete-dialog__message">
          Are you sure you want to delete the application for
          <strong>{{ entryName }}</strong>?
          This action cannot be undone.
        </p>
        <div class="delete-dialog__actions">
          <button
            class="delete-dialog__btn delete-dialog__btn--secondary"
            :disabled="loading"
            @click="$emit('cancel')"
          >
            Cancel
          </button>
          <button
            class="delete-dialog__btn delete-dialog__btn--danger"
            :disabled="loading"
            @click="$emit('confirm')"
          >
            <span v-if="loading" class="delete-dialog__spinner" aria-hidden="true"></span>
            <span>{{ loading ? 'Deleting…' : 'Delete' }}</span>
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  entryName: { type: String, required: true },
  loading: { type: Boolean, default: false },
})

defineEmits(['confirm', 'cancel'])
</script>

<style scoped>
.delete-dialog__overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
  animation: fadeIn 0.15s ease;
}

.delete-dialog__card {
  background-color: #fff;
  border-radius: 12px;
  padding: 28px 32px;
  max-width: 420px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  text-align: center;
  animation: slideUp 0.2s ease;
}

.delete-dialog__icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
}

.delete-dialog__title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 12px;
}

.delete-dialog__message {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 24px;
}

.delete-dialog__actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.delete-dialog__btn {
  padding: 9px 24px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: background-color 0.15s ease, border-color 0.15s ease;
  min-width: 100px;
}

.delete-dialog__btn--secondary {
  background-color: #fff;
  color: #374151;
  border-color: #d1d5db;
}

.delete-dialog__btn--secondary:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.delete-dialog__btn--danger {
  background-color: #ef4444;
  color: #fff;
  border-color: #ef4444;
}

.delete-dialog__btn--danger:hover {
  background-color: #dc2626;
  border-color: #dc2626;
}

.delete-dialog__btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.delete-dialog__spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  vertical-align: middle;
  margin-right: 4px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
