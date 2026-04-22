<template>
  <div class="job-list-view">
    <!-- Left Panel -->
    <aside class="job-list-view__sidebar">
      <div class="job-list-view__sidebar-header">
        <h1 class="job-list-view__heading">Applications</h1>
        <button class="job-list-view__add-btn" @click="handleAddJob" aria-label="Add new job application">
          + Add Job
        </button>
      </div>

      <div v-if="jobsStore.loading && jobsStore.entries.length === 0" class="job-list-view__loading">
        <LoadingSpinner message="Loading applications..." />
      </div>
      <JobList
        v-else
        :entries="jobsStore.entries"
        :selected-id="selectedEntry?.id ?? null"
        @select="handleSelectEntry"
      />
    </aside>

    <!-- Right Panel -->
    <main class="job-list-view__main">
      <!-- Loading overlay for mutations -->
      <div v-if="jobsStore.loading && jobsStore.entries.length > 0" class="job-list-view__main-loading">
        <LoadingSpinner size="sm" />
      </div>

      <!-- Empty state -->
      <div v-if="mode === 'list' && !selectedEntry" class="job-list-view__empty-state">
        <div class="job-list-view__empty-icon">💼</div>
        <p class="job-list-view__empty-text">Select a job or add a new one</p>
        <button class="job-list-view__empty-btn" @click="handleAddJob">+ Add Job</button>
      </div>

      <!-- Create form -->
      <div v-else-if="mode === 'create'" class="job-list-view__panel">
        <div class="job-list-view__panel-header">
          <h2 class="job-list-view__panel-title">New Application</h2>
        </div>
        <div class="job-list-view__panel-body">
          <JobForm
            :entry="null"
            :submitting="submitting"
            @submitted="handleFormSubmitted"
            @cancel="handleFormCancel"
          />
        </div>
      </div>

      <!-- Edit form -->
      <div v-else-if="mode === 'edit'" class="job-list-view__panel">
        <div class="job-list-view__panel-header">
          <h2 class="job-list-view__panel-title">Edit Application</h2>
        </div>
        <div class="job-list-view__panel-body">
          <JobForm
            :entry="selectedEntry"
            :submitting="submitting"
            @submitted="handleFormSubmitted"
            @cancel="handleFormCancel"
          />
        </div>
      </div>

      <!-- Detail view -->
      <div v-else-if="mode === 'detail' && selectedEntry" class="job-list-view__panel">
        <JobDetail
          :entry="selectedEntry"
          @edit="handleEdit"
          @delete="handleDeleteRequest"
        />
      </div>
    </main>

    <!-- Delete confirmation dialog -->
    <DeleteDialog
      v-if="showDeleteDialog && selectedEntry"
      :entry-name="selectedEntry.company_name"
      :loading="deleting"
      @confirm="handleDeleteConfirm"
      @cancel="showDeleteDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useJobsStore } from '../store/jobs.js'
import { useToastStore } from '../store/toast.js'
import JobList from '../components/jobs/JobList.vue'
import JobForm from '../components/jobs/JobForm.vue'
import JobDetail from '../components/jobs/JobDetail.vue'
import DeleteDialog from '../components/jobs/DeleteDialog.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

const jobsStore = useJobsStore()
const toast = useToastStore()

// mode: 'list' | 'create' | 'edit' | 'detail'
const mode = ref('list')
const showDeleteDialog = ref(false)
const selectedEntry = ref(null)
const submitting = ref(false)
const deleting = ref(false)

onMounted(async () => {
  try {
    await jobsStore.fetchAll()
  } catch {
    toast.error('Failed to load job applications.')
  }
})

function handleAddJob() {
  selectedEntry.value = null
  mode.value = 'create'
}

function handleSelectEntry(entry) {
  selectedEntry.value = entry
  mode.value = 'detail'
}

function handleEdit() {
  mode.value = 'edit'
}

function handleDeleteRequest() {
  showDeleteDialog.value = true
}

async function handleFormSubmitted(data) {
  submitting.value = true
  try {
    if (mode.value === 'create') {
      const newEntry = await jobsStore.create(data)
      selectedEntry.value = newEntry
      mode.value = 'detail'
      toast.success('Job application added!')
    } else if (mode.value === 'edit') {
      const updated = await jobsStore.update(selectedEntry.value.id, data)
      selectedEntry.value = updated
      mode.value = 'detail'
      toast.success('Application updated.')
    }
  } catch (err) {
    toast.error(err.response?.data?.error || err.message || 'Something went wrong.')
  } finally {
    submitting.value = false
  }
}

function handleFormCancel() {
  if (mode.value === 'create') {
    mode.value = selectedEntry.value ? 'detail' : 'list'
  } else {
    mode.value = 'detail'
  }
}

async function handleDeleteConfirm() {
  const id = selectedEntry.value?.id
  if (!id) return
  deleting.value = true
  try {
    await jobsStore.remove(id)
    selectedEntry.value = null
    mode.value = 'list'
    toast.success('Application deleted.')
    showDeleteDialog.value = false
  } catch (err) {
    toast.error(err.response?.data?.error || err.message || 'Failed to delete.')
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
.job-list-view {
  display: flex;
  height: 100%;
  overflow: hidden;
}

/* Left sidebar panel */
.job-list-view__sidebar {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e2e8f0;
  background-color: #fff;
  overflow: hidden;
}

.job-list-view__sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 16px 12px;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.job-list-view__heading {
  font-size: 1.0625rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.job-list-view__add-btn {
  padding: 6px 14px;
  background-color: #6366f1;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.job-list-view__add-btn:hover {
  background-color: #4f46e5;
}

.job-list-view__error {
  margin: 8px 12px 0;
  flex-shrink: 0;
}

.job-list-view__loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Right main panel */
.job-list-view__main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #fff;
  position: relative;
}

.job-list-view__main-loading {
  position: absolute;
  top: 12px;
  right: 16px;
  z-index: 10;
}

.job-list-view__empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  gap: 12px;
  padding: 48px;
}

.job-list-view__empty-icon {
  font-size: 3rem;
}

.job-list-view__empty-text {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
}

.job-list-view__empty-btn {
  padding: 8px 20px;
  background-color: #6366f1;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.job-list-view__empty-btn:hover {
  background-color: #4f46e5;
}

.job-list-view__panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.job-list-view__panel-header {
  padding: 20px 24px 16px;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.job-list-view__panel-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.job-list-view__panel-body {
  flex: 1;
  overflow-y: auto;
}
</style>
