<template>
  <div class="chart-card">
    <h3 class="chart-title">Applications per Month</h3>
    <div v-if="hasData" class="chart-container">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <div v-else class="chart-empty">
      <span>📅</span>
      <p>No applications in the last 12 months.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
  // Accepts either monthly_counts (new) or weekly_counts (legacy fallback)
  monthlyCounts: { type: Array, default: () => [] },
  weeklyCounts:  { type: Array, default: () => [] },
})

const data = computed(() =>
  props.monthlyCounts.length ? props.monthlyCounts : props.weeklyCounts
)

const chartData = computed(() => ({
  labels: data.value.map((d) => d.month || d.week),
  datasets: [
    {
      label: 'Applications',
      data: data.value.map((d) => d.count),
      backgroundColor: 'rgba(99, 102, 241, 0.8)',
      borderColor: '#6366f1',
      borderWidth: 1,
      borderRadius: 4,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label(context) {
          return ` ${context.parsed.y} application${context.parsed.y !== 1 ? 's' : ''}`
        },
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { font: { size: 11 }, maxRotation: 45 },
    },
    y: {
      beginAtZero: true,
      ticks: { stepSize: 1, precision: 0 },
      grid: { color: 'rgba(0,0,0,0.05)' },
    },
  },
}

const hasData = computed(() => data.value.some((d) => d.count > 0))
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
  position: relative;
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

.chart-empty span { font-size: 2.5rem; }
.chart-empty p { margin: 0; font-size: 0.875rem; }
</style>
