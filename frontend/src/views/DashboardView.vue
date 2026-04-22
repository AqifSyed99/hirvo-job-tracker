<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
      <p>Welcome back, {{ profileStore.profile?.full_name || authStore.user?.full_name || authStore.user?.email }}</p>
    </div>

    <LoadingSpinner v-if="jobsStore.loading" message="Loading stats..." />

    <template v-if="!jobsStore.loading && jobsStore.stats">
      <!-- Stat cards row -->
      <div class="stats-grid">
        <StatCard
          label="Total Applications"
          :value="jobsStore.stats.total"
          icon="📝"
          color="#6366f1"
          :delay="0"
        />
        <StatCard
          label="Interviews"
          :value="jobsStore.stats.interview"
          icon="🎯"
          color="#f59e0b"
          :delay="100"
        />
        <StatCard
          label="Offers"
          :value="jobsStore.stats.offer"
          icon="🎉"
          color="#10b981"
          :delay="200"
        />
        <StatCard
          label="Rejected"
          :value="jobsStore.stats.rejected"
          icon="❌"
          color="#ef4444"
          :delay="300"
        />
      </div>

      <!-- Charts row -->
      <div class="charts-grid">
        <StatusChart :by-status="jobsStore.stats.by_status" />
        <WeeklyChart :monthly-counts="jobsStore.stats.monthly_counts || []" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useAuthStore } from '../store/auth'
import { useJobsStore } from '../store/jobs'
import { useProfileStore } from '../store/profile'
import { useToastStore } from '../store/toast'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import StatCard from '../components/dashboard/StatCard.vue'
import StatusChart from '../components/dashboard/StatusChart.vue'
import WeeklyChart from '../components/dashboard/WeeklyChart.vue'

const authStore = useAuthStore()
const jobsStore = useJobsStore()
const profileStore = useProfileStore()
const toast = useToastStore()

onMounted(async () => {
  // Fetch profile to get full_name if not already loaded
  if (!profileStore.profile) profileStore.fetchProfile()
  try {
    await jobsStore.fetchStats()
  } catch {
    toast.error('Failed to load dashboard stats.')
  }
})

watch(
  () => jobsStore.entries,
  async () => {
    try {
      await jobsStore.fetchStats()
    } catch {
      // silently ignore re-fetch errors
    }
  },
)
</script>

<style scoped>
.dashboard {
  padding: 32px;
}

.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px 0;
}

.dashboard-header p {
  font-size: 0.9375rem;
  color: #6b7280;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 32px;
}

/* Tablet: 2-column stat grid */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile: single column */
@media (max-width: 640px) {
  .dashboard {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
