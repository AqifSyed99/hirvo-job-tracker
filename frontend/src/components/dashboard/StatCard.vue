<template>
  <div class="stat-card" :class="{ 'stat-card--visible': visible }">
    <div class="stat-icon" :style="{ backgroundColor: `${color}20`, color: color }">
      {{ icon }}
    </div>
    <div class="stat-value">{{ value }}</div>
    <div class="stat-label">{{ label }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: Number, required: true },
  icon: { type: String, default: '📊' },
  color: { type: String, default: '#6366f1' },
  delay: { type: Number, default: 0 },
})

const visible = ref(false)
onMounted(() => {
  setTimeout(() => {
    visible.value = true
  }, 50 + props.delay)
})
</script>

<style scoped>
.stat-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.4s ease,
    transform 0.4s ease,
    box-shadow 0.2s ease;
  cursor: default;
}

.stat-card--visible {
  opacity: 1;
  transform: translateY(0);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

/* Prevent hover from overriding the entrance animation before it completes */
.stat-card:not(.stat-card--visible):hover {
  transform: translateY(20px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 16px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
}
</style>
