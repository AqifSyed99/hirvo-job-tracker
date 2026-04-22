<template>
  <div class="chart-card">
    <h3 class="chart-title">Applications by Status</h3>
    <div v-if="hasData" class="chart-container">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
    <div v-else class="chart-empty">
      <span>📭</span>
      <p>No applications yet. Add your first job!</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  byStatus: { type: Object, required: true },
})

const STATUS_COLORS = ['#6366f1', '#f59e0b', '#10b981', '#22c55e', '#ef4444', '#94a3b8']

const chartData = computed(() => {
  const labels = Object.keys(props.byStatus)
  const data = Object.values(props.byStatus)
  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: STATUS_COLORS.slice(0, labels.length),
        borderWidth: 2,
        borderColor: '#ffffff',
        hoverBorderColor: '#ffffff',
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 16,
        font: { size: 12 },
        usePointStyle: true,
      },
    },
    tooltip: {
      callbacks: {
        label(context) {
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const pct = total > 0 ? Math.round((context.parsed / total) * 100) : 0
          return ` ${context.label}: ${context.parsed} (${pct}%)`
        },
      },
    },
  },
}

const hasData = computed(() => Object.values(props.byStatus).some((v) => v > 0))
</script>

<style scoped>
.chart-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 20px 0;
}

.chart-container {
  max-width: 320px;
  margin: 0 auto;
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 40px 0;
  color: #9ca3af;
}

.chart-empty span {
  font-size: 2.5rem;
}

.chart-empty p {
  margin: 0;
  font-size: 0.875rem;
}
</style>
