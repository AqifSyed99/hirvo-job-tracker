<template>
  <div class="job-list">
    <div v-if="entries.length === 0" class="job-list__empty">
      <div class="job-list__empty-icon">📋</div>
      <p class="job-list__empty-text">No job applications yet</p>
      <p class="job-list__empty-hint">Click the <strong>+ Add Job</strong> button to get started</p>
    </div>
    <div v-else class="job-list__items">
      <JobListItem
        v-for="entry in entries"
        :key="entry.id"
        :entry="entry"
        :is-selected="entry.id === selectedId"
        @select="$emit('select', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import JobListItem from './JobListItem.vue'

defineProps({
  entries: { type: Array, required: true },
  selectedId: { type: Number, default: null },
})

defineEmits(['select'])
</script>

<style scoped>
.job-list {
  height: 100%;
  overflow-y: auto;
}

.job-list__items {
  display: flex;
  flex-direction: column;
}

.job-list__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
  color: #94a3b8;
  height: 100%;
  min-height: 200px;
}

.job-list__empty-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
}

.job-list__empty-text {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #64748b;
  margin: 0 0 6px;
}

.job-list__empty-hint {
  font-size: 0.8125rem;
  color: #94a3b8;
  margin: 0;
}
</style>
