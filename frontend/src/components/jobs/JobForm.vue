<template>
  <form class="job-form" @submit.prevent="handleSubmit" novalidate>
    <div class="job-form__section">
      <h3 class="job-form__section-title">Basic Information</h3>

      <!-- Company Name -->
      <div class="job-form__field">
        <label class="job-form__label" for="company_name">
          Company Name <span class="job-form__required" aria-hidden="true">*</span>
        </label>
        <input
          id="company_name"
          v-model="form.company_name"
          type="text"
          class="job-form__input"
          :class="{ 'job-form__input--error': errors.company_name }"
          placeholder="e.g. Intel Inc."
          autocomplete="organization"
        />
        <span v-if="errors.company_name" class="job-form__error" role="alert">
          {{ errors.company_name }}
        </span>
      </div>

      <!-- Job Title -->
      <div class="job-form__field">
        <label class="job-form__label" for="job_title">
          Job Title <span class="job-form__required" aria-hidden="true">*</span>
        </label>
        <input
          id="job_title"
          v-model="form.job_title"
          type="text"
          class="job-form__input"
          :class="{ 'job-form__input--error': errors.job_title }"
          placeholder="e.g. Software Engineer"
          autocomplete="off"
        />
        <span v-if="errors.job_title" class="job-form__error" role="alert">
          {{ errors.job_title }}
        </span>
      </div>

      <!-- Status -->
      <div class="job-form__field">
        <label class="job-form__label" for="status">
          Status <span class="job-form__required" aria-hidden="true">*</span>
        </label>
        <select
          id="status"
          v-model="form.status"
          class="job-form__select"
          :class="{ 'job-form__input--error': errors.status }"
        >
          <option value="" disabled>Select a status</option>
          <option v-for="s in STATUS_OPTIONS" :key="s" :value="s">{{ s }}</option>
        </select>
        <span v-if="errors.status" class="job-form__error" role="alert">
          {{ errors.status }}
        </span>
      </div>

      <!-- Platform -->
      <div class="job-form__field">
        <label class="job-form__label" for="platform">
          Platform <span class="job-form__required" aria-hidden="true">*</span>
        </label>
        <div class="job-form__platform-grid">
          <button
            v-for="p in PLATFORM_OPTIONS"
            :key="p.value"
            type="button"
            class="job-form__platform-btn"
            :class="{ 'job-form__platform-btn--selected': platformSelection === p.value }"
            @click="platformSelection = p.value"
          >
            <img v-if="p.logo" :src="p.logo" :alt="p.label" class="job-form__platform-img" />
            <span v-else class="job-form__platform-fallback">🌐</span>
            <span class="job-form__platform-name">{{ p.label }}</span>
          </button>
        </div>
        <!-- Custom platform text field shown when Other is selected -->
        <div v-if="platformSelection === 'Other'" class="job-form__other-platform">
          <input
            v-model="form.platform"
            type="text"
            class="job-form__input"
            :class="{ 'job-form__input--error': errors.platform }"
            placeholder="Enter platform name e.g. Glassdoor, Telegram"
            autofocus
          />
        </div>
        <span v-if="errors.platform" class="job-form__error" role="alert">
          {{ errors.platform }}
        </span>
      </div>

      <!-- Application Date -->
      <div class="job-form__field">
        <label class="job-form__label" for="application_date">
          Application Date <span class="job-form__required" aria-hidden="true">*</span>
        </label>
        <input
          id="application_date"
          v-model="form.application_date"
          type="date"
          class="job-form__input"
          :class="{ 'job-form__input--error': errors.application_date }"
        />
        <span v-if="errors.application_date" class="job-form__error" role="alert">
          {{ errors.application_date }}
        </span>
      </div>
    </div>

    <div class="job-form__section">
      <h3 class="job-form__section-title">Details</h3>

      <!-- Work Type -->
      <div class="job-form__field">
        <label class="job-form__label" for="work_type">Work Type</label>
        <select id="work_type" v-model="form.work_type" class="job-form__select">
          <option value="">Select work type</option>
          <option v-for="w in WORK_TYPE_OPTIONS" :key="w" :value="w">{{ w }}</option>
        </select>
      </div>

      <!-- Employment Type -->
      <div class="job-form__field">
        <label class="job-form__label" for="employment_type">Employment Type</label>
        <select id="employment_type" v-model="form.employment_type" class="job-form__select">
          <option value="">Select employment type</option>
          <option v-for="e in EMPLOYMENT_TYPE_OPTIONS" :key="e" :value="e">{{ e }}</option>
        </select>
      </div>

      <!-- Location -->
      <div class="job-form__field">
        <label class="job-form__label" for="location">Location</label>
        <input
          id="location"
          v-model="form.location"
          type="text"
          class="job-form__input"
          placeholder="Company address"
        />
      </div>

      <!-- Salary Range (two-column) -->
      <div class="job-form__field">
        <label class="job-form__label">Salary Range</label>
        <div class="job-form__salary-row">
          <div class="job-form__salary-field">
            <label class="job-form__sublabel" for="salary_min">Minimum</label>
            <input
              id="salary_min"
              v-model.number="form.salary_min"
              type="number"
              class="job-form__input"
              :class="{ 'job-form__input--error': errors.salary }"
              placeholder="e.g. 80000"
              min="0"
            />
          </div>
          <div class="job-form__salary-field">
            <label class="job-form__sublabel" for="salary_max">Maximum</label>
            <input
              id="salary_max"
              v-model.number="form.salary_max"
              type="number"
              class="job-form__input"
              :class="{ 'job-form__input--error': errors.salary }"
              placeholder="e.g. 120000"
              min="0"
            />
          </div>
        </div>
        <span v-if="errors.salary" class="job-form__error" role="alert">
          {{ errors.salary }}
        </span>
      </div>

      <!-- Job URL -->
      <div class="job-form__field">
        <label class="job-form__label" for="job_url">Job URL</label>
        <input
          id="job_url"
          v-model="form.job_url"
          type="url"
          class="job-form__input"
          placeholder="https://example.com/job"
        />
      </div>
    </div>

    <div class="job-form__section">
      <h3 class="job-form__section-title">Additional Info</h3>

      <!-- Contact Person -->
      <div class="job-form__field">
        <label class="job-form__label" for="contact_person">Contact Person</label>
        <input
          id="contact_person"
          v-model="form.contact_person"
          type="text"
          class="job-form__input"
          placeholder="e.g. Abu from HR, +60 12-345 6789"
        />
      </div>

      <!-- Notes -->
      <div class="job-form__field">
        <label class="job-form__label" for="notes">Notes</label>
        <textarea
          id="notes"
          v-model="form.notes"
          class="job-form__textarea"
          rows="4"
          placeholder="Any notes about this application..."
        ></textarea>
      </div>

      <!-- File Attachments (multiple) -->
      <div class="job-form__field">
        <label class="job-form__label">Attachments</label>
        <div class="job-form__file-wrapper">
          <label class="job-form__file-label" for="files">
            <span class="job-form__file-icon">📎</span>
            <span class="job-form__file-text">Choose files (PDF, PNG, JPG, JPEG) — multiple allowed</span>
          </label>
          <input
            id="files"
            ref="fileInput"
            type="file"
            class="job-form__file-input"
            accept=".pdf,.png,.jpg,.jpeg"
            multiple
            @change="handleFileChange"
          />
        </div>
        <!-- Selected new files -->
        <div v-if="selectedFiles.length" class="job-form__file-list">
          <div v-for="(f, i) in selectedFiles" :key="i" class="job-form__file-item">
            <span>📎 {{ f.name }}</span>
            <button type="button" class="job-form__file-clear" @click="removeFile(i)">×</button>
          </div>
        </div>
        <!-- Existing attachments (edit mode) -->
        <div v-if="existingAttachments.length" class="job-form__file-list">
          <div v-for="att in existingAttachments" :key="att.id" class="job-form__file-item job-form__file-item--existing">
            <span>📎 {{ att.file_original_name || 'Attachment' }}</span>
            <button type="button" class="job-form__file-clear" @click="removeExisting(att.id)">×</button>
          </div>
        </div>
      </div>
    </div>

    <div class="job-form__actions">
      <button
        type="button"
        class="job-form__btn job-form__btn--secondary"
        :disabled="submitting"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
      <button
        type="submit"
        class="job-form__btn job-form__btn--primary"
        :disabled="submitting"
      >
        <span v-if="submitting" class="job-form__spinner" aria-hidden="true"></span>
        <span>{{ submitting ? 'Saving…' : (entry ? 'Save Changes' : 'Add Job') }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'

const props = defineProps({
  entry: { type: Object, default: null },
  submitting: { type: Boolean, default: false },
})

const emit = defineEmits(['submitted', 'cancel'])

const STATUS_OPTIONS = ['Applied', 'Phone Screen', 'Interview', 'Offer', 'Rejected', 'Withdrawn']

const WORK_TYPE_OPTIONS = ['On-site', 'Remote', 'Hybrid']

const EMPLOYMENT_TYPE_OPTIONS = [
  'Full-time',
  'Part-time',
  'Contract',
  'Freelance',
  'Internship',
  'Apprenticeship',
  'Temporary',
  'Volunteer',
]

const PLATFORM_OPTIONS = [
  { value: 'LinkedIn',     label: 'LinkedIn',     logo: 'https://www.google.com/s2/favicons?domain=linkedin.com&sz=64' },
  { value: 'Indeed',       label: 'Indeed',       logo: 'https://www.google.com/s2/favicons?domain=indeed.com&sz=64' },
  { value: 'Jobstreet',    label: 'Jobstreet',    logo: 'https://www.google.com/s2/favicons?domain=jobstreet.com.my&sz=64' },
  { value: 'MyFutureJobs', label: 'MyFutureJobs', logo: 'https://www.google.com/s2/favicons?domain=myfuturejobs.gov.my&sz=64' },
  { value: 'Jora',         label: 'Jora',         logo: 'https://www.google.com/s2/favicons?domain=jora.com&sz=64' },
  { value: 'Maukerja',     label: 'Maukerja',     logo: 'https://www.google.com/s2/favicons?domain=maukerja.my&sz=64' },
  { value: 'SPA',          label: 'SPA',          logo: 'https://www.google.com/s2/favicons?domain=malaysia.gov.my&sz=64' },
  { value: 'Other',        label: 'Other',        logo: null },
]

const fileInput = ref(null)
const selectedFiles = ref([])
const removedAttachmentIds = ref([])
const existingAttachments = ref([])

// Tracks which button is highlighted — 'Other' means user types a custom value
const platformSelection = ref('')

// Watch platformSelection: when a known platform is picked, set form.platform directly.
// When 'Other' is picked, clear form.platform so user types it.
watch(platformSelection, (val) => {
  if (val !== 'Other') {
    form.platform = val
  } else {
    form.platform = ''
  }
})

const form = reactive({
  company_name: '',
  job_title: '',
  status: '',
  platform: '',
  contact_person: '',
  work_type: '',
  employment_type: '',
  application_date: '',
  location: '',
  salary_min: null,
  salary_max: null,
  job_url: '',
  notes: '',
})

const errors = reactive({
  company_name: '',
  job_title: '',
  status: '',
  platform: '',
  application_date: '',
  salary: '',
})

// Remove computed fileDisplayName — no longer needed

// Pre-populate when entry prop is provided
function populateForm(entry) {
  if (!entry) return
  form.company_name = entry.company_name || ''
  form.job_title = entry.job_title || ''
  form.status = entry.status || ''
  form.contact_person = entry.contact_person || ''
  form.work_type = entry.work_type || ''
  form.employment_type = entry.employment_type || ''
  form.application_date = entry.application_date || ''
  form.location = entry.location || ''
  form.salary_min = entry.salary_min ?? null
  form.salary_max = entry.salary_max ?? null
  form.job_url = entry.job_url || ''
  form.notes = entry.notes || ''
  selectedFiles.value = []
  removedAttachmentIds.value = []
  existingAttachments.value = entry.attachments ? [...entry.attachments] : []

  // Restore platform selection
  const knownPlatforms = PLATFORM_OPTIONS.map(p => p.value).filter(v => v !== 'Other')
  if (knownPlatforms.includes(entry.platform)) {
    platformSelection.value = entry.platform
    form.platform = entry.platform
  } else if (entry.platform) {
    platformSelection.value = 'Other'
    form.platform = entry.platform
  } else {
    platformSelection.value = ''
    form.platform = ''
  }
}

// Initialize on mount
populateForm(props.entry)

// Re-populate when entry changes (e.g., switching between edit targets)
watch(() => props.entry, (newEntry) => {
  populateForm(newEntry)
  clearErrors()
  if (!newEntry) {
    platformSelection.value = ''
  }
})

function clearErrors() {
  errors.company_name = ''
  errors.job_title = ''
  errors.status = ''
  errors.platform = ''
  errors.application_date = ''
  errors.salary = ''
}

function handleFileChange(event) {
  const files = Array.from(event.target.files)
  selectedFiles.value.push(...files)
  event.target.value = ''
}

function removeFile(index) {
  selectedFiles.value.splice(index, 1)
}

function removeExisting(id) {
  removedAttachmentIds.value.push(id)
  existingAttachments.value = existingAttachments.value.filter(a => a.id !== id)
}

function validate() {
  clearErrors()
  let valid = true

  if (!form.company_name.trim()) {
    errors.company_name = 'Company name is required.'
    valid = false
  }
  if (!form.job_title.trim()) {
    errors.job_title = 'Job title is required.'
    valid = false
  }
  if (!form.status) {
    errors.status = 'Status is required.'
    valid = false
  }
  if (!form.platform) {
    errors.platform = 'Platform is required.'
    valid = false
  }
  if (!form.application_date) {
    errors.application_date = 'Application date is required.'
    valid = false
  }
  if (
    form.salary_min !== null && form.salary_min !== '' &&
    form.salary_max !== null && form.salary_max !== '' &&
    Number(form.salary_min) > Number(form.salary_max)
  ) {
    errors.salary = 'Minimum salary cannot be greater than maximum salary.'
    valid = false
  }

  return valid
}

function handleSubmit() {
  if (!validate()) return

  const data = {
    company_name: form.company_name.trim(),
    job_title: form.job_title.trim(),
    status: form.status,
    platform: form.platform,
    contact_person: form.contact_person.trim() || null,
    work_type: form.work_type || null,
    employment_type: form.employment_type || null,
    application_date: form.application_date || null,
    location: form.location.trim() || null,
    salary_min: form.salary_min !== '' && form.salary_min !== null ? Number(form.salary_min) : null,
    salary_max: form.salary_max !== '' && form.salary_max !== null ? Number(form.salary_max) : null,
    job_url: form.job_url.trim() || null,
    notes: form.notes.trim() || null,
    files: selectedFiles.value,
    removedAttachmentIds: removedAttachmentIds.value,
  }

  emit('submitted', data)
}
</script>

<style scoped>
.job-form {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.job-form__section {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.job-form__section:last-of-type {
  border-bottom: none;
}

.job-form__section-title {
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
  margin: 0 0 16px;
}

.job-form__field {
  margin-bottom: 16px;
}

.job-form__field:last-child {
  margin-bottom: 0;
}

.job-form__label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
}

.job-form__sublabel {
  display: block;
  font-size: 0.8125rem;
  color: #6b7280;
  margin-bottom: 4px;
}

.job-form__required {
  color: #ef4444;
  margin-left: 2px;
}

.job-form__input,
.job-form__select,
.job-form__textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #1e293b;
  background-color: #fff;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  box-sizing: border-box;
}

.job-form__input:focus,
.job-form__select:focus,
.job-form__textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.job-form__input--error {
  border-color: #ef4444;
}

.job-form__input--error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.job-form__select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%236b7280' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
  cursor: pointer;
}

.job-form__textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.job-form__error {
  display: block;
  font-size: 0.75rem;
  color: #ef4444;
  margin-top: 4px;
}

.job-form__salary-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

/* Platform selector */
.job-form__platform-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.job-form__platform-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 6px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  transition: border-color 0.15s ease, background-color 0.15s ease, transform 0.1s ease;
  font-size: 0.75rem;
  color: #374151;
  font-weight: 500;
}

.job-form__platform-btn:hover {
  border-color: #6366f1;
  background: #f5f3ff;
}

.job-form__platform-btn--selected {
  border-color: #6366f1;
  background: #eef2ff;
  color: #4f46e5;
  transform: scale(1.03);
}

.job-form__platform-logo {
  font-size: 1.25rem;
}

.job-form__platform-img {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.job-form__platform-fallback {
  font-size: 1.25rem;
}

.job-form__platform-name {
  font-size: 0.6875rem;
  text-align: center;
  line-height: 1.2;
}

.job-form__other-platform {
  margin-top: 10px;
  animation: fadeIn 0.15s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}

.job-form__file-wrapper {
  position: relative;
}

.job-form__file-input {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
}

.job-form__file-label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 1px dashed #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  color: #6b7280;
  transition: border-color 0.15s ease, background-color 0.15s ease;
}

.job-form__file-label:hover {
  border-color: #6366f1;
  background-color: #f5f3ff;
  color: #6366f1;
}

.job-form__file-icon {
  font-size: 1rem;
}

.job-form__file-selected {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: #6366f1;
  margin-top: 6px;
}

.job-form__file-clear {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  font-size: 1rem;
  line-height: 1;
  padding: 0 2px;
  border-radius: 3px;
  transition: color 0.15s ease;
}

.job-form__file-clear:hover {
  color: #ef4444;
}

.job-form__file-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 8px;
}

.job-form__file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 10px;
  background: #f5f3ff;
  border: 1px solid #c4b5fd;
  border-radius: 6px;
  font-size: 0.8125rem;
  color: #4f46e5;
}

.job-form__file-item--existing {
  background: #f0fdf4;
  border-color: #86efac;
  color: #166534;
}

.job-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 24px;
  border-top: 1px solid #f1f5f9;
  background-color: #fafafa;
}

.job-form__btn {
  padding: 8px 20px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
  border: 1px solid transparent;
}

.job-form__btn--primary {
  background-color: #6366f1;
  color: #fff;
  border-color: #6366f1;
}

.job-form__btn--primary:hover {
  background-color: #4f46e5;
  border-color: #4f46e5;
}

.job-form__btn--secondary {
  background-color: #fff;
  color: #374151;
  border-color: #d1d5db;
}

.job-form__btn--secondary:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.job-form__btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.job-form__spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
  vertical-align: middle;
  margin-right: 4px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
