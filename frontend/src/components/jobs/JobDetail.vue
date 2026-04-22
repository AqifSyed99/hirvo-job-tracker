<template>
  <div class="job-detail">
    <div class="job-detail__header">
      <div class="job-detail__header-info">
        <h2 class="job-detail__company">{{ entry.company_name }}</h2>
        <p class="job-detail__title">{{ entry.job_title }}</p>
        <span
          class="job-detail__badge"
          :style="{ backgroundColor: statusColor(entry.status) }"
        >{{ entry.status }}</span>
      </div>
      <div class="job-detail__actions">
        <button class="job-detail__btn job-detail__btn--secondary" @click="$emit('edit')">
          ✏️ Edit
        </button>
        <button class="job-detail__btn job-detail__btn--danger" @click="$emit('delete')">
          🗑️ Delete
        </button>
      </div>
    </div>

    <div class="job-detail__body">
      <div class="job-detail__fields">

        <div v-if="entry.application_date" class="job-detail__field">
          <span class="job-detail__field-label">Application Date</span>
          <span class="job-detail__field-value">{{ formatDate(entry.application_date) }}</span>
        </div>

        <div v-if="entry.platform" class="job-detail__field">
          <span class="job-detail__field-label">Platform</span>
          <div class="job-detail__platform">
            <template v-if="platformLogo(entry.platform)">
              <img
                :src="platformLogo(entry.platform)"
                :alt="entry.platform"
                class="job-detail__platform-logo"
                @error="onLogoError($event)"
              />
              <span class="job-detail__platform-emoji" style="display:none">{{ platformEmoji(entry.platform) }}</span>
            </template>
            <span v-else class="job-detail__platform-emoji">{{ platformEmoji(entry.platform) }}</span>
            <span class="job-detail__platform-name">{{ entry.platform }}</span>
          </div>
        </div>

        <div v-if="entry.location" class="job-detail__field">
          <span class="job-detail__field-label">Location</span>
          <span class="job-detail__field-value">📍 {{ entry.location }}</span>
          <div class="job-detail__map">
            <iframe
              :src="`https://maps.google.com/maps?q=${encodeURIComponent(entry.location)}&output=embed&z=13`"
              class="job-detail__map-iframe"
              allowfullscreen
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
              title="Location map"
            ></iframe>
          </div>
        </div>

        <div v-if="salaryDisplay" class="job-detail__field">
          <span class="job-detail__field-label">Salary Range</span>
          <span class="job-detail__field-value">{{ salaryDisplay }}</span>
        </div>

        <div v-if="entry.job_url" class="job-detail__field">
          <span class="job-detail__field-label">Job URL</span>
          <a
            :href="entry.job_url"
            target="_blank"
            rel="noopener noreferrer"
            class="job-detail__link"
          >{{ entry.job_url }}</a>
        </div>

        <div v-if="entry.work_type || entry.employment_type" class="job-detail__field">
          <span class="job-detail__field-label">Job Type</span>
          <div class="job-detail__tags">
            <span v-if="entry.work_type" class="job-detail__tag job-detail__tag--work">{{ entry.work_type }}</span>
            <span v-if="entry.employment_type" class="job-detail__tag job-detail__tag--employment">{{ entry.employment_type }}</span>
          </div>
        </div>

        <div v-if="entry.contact_person" class="job-detail__field">
          <span class="job-detail__field-label">Contact Person</span>
          <span class="job-detail__field-value">👤 {{ entry.contact_person }}</span>
        </div>

        <div v-if="entry.notes" class="job-detail__field job-detail__field--full">
          <span class="job-detail__field-label">Notes</span>
          <p class="job-detail__notes">{{ entry.notes }}</p>
        </div>

        <!-- Multiple attachments -->
        <div v-if="allAttachments.length" class="job-detail__field">
          <span class="job-detail__field-label">Attachments ({{ allAttachments.length }})</span>
          <div class="job-detail__attachments">
            <button
              v-for="att in allAttachments"
              :key="att.id || att.file_url"
              class="job-detail__file-btn"
              @click="openAttachment(att)"
            >
              📎 {{ att.file_original_name || 'Attachment' }}
              <span class="job-detail__file-btn-hint">Click to view</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- File preview modal -->
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="showFileModal"
        class="file-modal__overlay"
        @click.self="showFileModal = false"
        role="dialog"
        aria-modal="true"
        aria-label="File preview"
      >
        <div class="file-modal__card">
          <div class="file-modal__header">
            <span class="file-modal__title">📎 {{ attachmentName }}</span>
            <div class="file-modal__header-actions">
              <a
                :href="selectedAttachment?.file_url"
                target="_blank"
                rel="noopener noreferrer"
                class="file-modal__open-btn"
                title="Open in new tab"
              >↗ Open</a>
              <button class="file-modal__close" @click="showFileModal = false" aria-label="Close">×</button>
            </div>
          </div>
          <div class="file-modal__body">
            <!-- Image preview -->
            <img
              v-if="currentIsImage"
              :src="selectedAttachment?.file_url"
              :alt="attachmentName"
              class="file-modal__image"
            />
            <!-- PDF preview via blob URL -->
            <div v-else-if="currentIsPdf" class="file-modal__pdf-wrapper">
              <iframe
                v-if="pdfBlobUrl"
                :src="pdfBlobUrl"
                class="file-modal__iframe"
                title="PDF preview"
              ></iframe>
              <div v-else-if="pdfError" class="file-modal__fallback">
                <p>{{ pdfError }}</p>
                <a :href="selectedAttachment?.file_url" target="_blank" rel="noopener noreferrer" class="file-modal__download">
                  ↗ Open file in new tab
                </a>
              </div>
              <div v-else class="file-modal__loading">
                <div class="file-modal__spinner"></div>
                <p>Loading PDF…</p>
              </div>
            </div>
            <!-- Fallback -->
            <div v-else class="file-modal__fallback">
              <p>Preview not available for this file type.</p>
              <a :href="selectedAttachment?.file_url" target="_blank" rel="noopener noreferrer" class="file-modal__download">
                ↗ Open file in new tab
              </a>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  entry: { type: Object, required: true },
})

defineEmits(['edit', 'delete'])

const showFileModal = ref(false)
const selectedAttachment = ref(null)
const pdfBlobUrl = ref(null)
const pdfError = ref(null)

// All attachments: new multi-attachments + legacy single file
const allAttachments = computed(() => {
  const atts = props.entry.attachments ? [...props.entry.attachments] : []
  // Include legacy single file if present and not already in attachments
  if (props.entry.file_url && !atts.some(a => a.file_url === props.entry.file_url)) {
    atts.push({
      id: 'legacy',
      file_url: props.entry.file_url,
      file_public_id: props.entry.file_public_id,
      file_original_name: props.entry.file_original_name,
    })
  }
  return atts
})

function openAttachment(att) {
  selectedAttachment.value = att
  pdfBlobUrl.value = null
  pdfError.value = null
  showFileModal.value = true
}

// Fetch PDF as blob when modal opens
watch(showFileModal, async (open) => {
  if (!open) {
    if (pdfBlobUrl.value) {
      URL.revokeObjectURL(pdfBlobUrl.value)
      pdfBlobUrl.value = null
    }
    pdfError.value = null
    selectedAttachment.value = null
    return
  }
  if (currentIsPdf.value && !pdfBlobUrl.value && selectedAttachment.value) {
    try {
      const response = await fetch(selectedAttachment.value.file_url)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const blob = await response.blob()
      const pdfBlob = new Blob([blob], { type: 'application/pdf' })
      pdfBlobUrl.value = URL.createObjectURL(pdfBlob)
    } catch (err) {
      pdfError.value = 'Could not load PDF preview. Use the Open button to view it.'
    }
  }
})

const PLATFORM_LOGOS = {
  'LinkedIn':     'https://www.google.com/s2/favicons?domain=linkedin.com&sz=64',
  'Indeed':       'https://www.google.com/s2/favicons?domain=indeed.com&sz=64',
  'Jobstreet':    'https://www.google.com/s2/favicons?domain=jobstreet.com.my&sz=64',
  'MyFutureJobs': 'https://www.google.com/s2/favicons?domain=myfuturejobs.gov.my&sz=64',
  'Jora':         'https://www.google.com/s2/favicons?domain=jora.com&sz=64',
  'Maukerja':     'https://www.google.com/s2/favicons?domain=maukerja.my&sz=64',
  'SPA':          'https://www.google.com/s2/favicons?domain=malaysia.gov.my&sz=64',
  'Other':        null,
}

// Emoji fallbacks for platforms whose favicons may not load
const PLATFORM_EMOJI = {
  'LinkedIn':     null,
  'Indeed':       null,
  'Jobstreet':    null,
  'MyFutureJobs': '🌐',
  'Jora':         null,
  'Maukerja':     '🌐',
  'SPA':          '🌐',
  'Other':        '🌐',
}

function platformLogo(platform) {
  return PLATFORM_LOGOS[platform] || null
}

function platformEmoji(platform) {
  return PLATFORM_EMOJI[platform] || '🌐'
}

function onLogoError(event) {
  // Hide the broken image and show the emoji fallback sibling
  event.target.style.display = 'none'
  const fallback = event.target.nextElementSibling
  if (fallback) fallback.style.display = 'inline'
}

const STATUS_COLORS = {
  'Applied': '#3b82f6',
  'Phone Screen': '#f59e0b',
  'Interview': '#8b5cf6',
  'Offer': '#10b981',
  'Rejected': '#ef4444',
  'Withdrawn': '#94a3b8',
}

function statusColor(status) {
  return STATUS_COLORS[status] || '#94a3b8'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr + 'T00:00:00')
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function formatSalary(value) {
  if (value === null || value === undefined) return null
  return 'RM ' + Number(value).toLocaleString('en-MY', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

const salaryDisplay = computed(() => {
  const min = props.entry.salary_min
  const max = props.entry.salary_max
  if (min != null && max != null) return `${formatSalary(min)} - ${formatSalary(max)}`
  if (min != null) return formatSalary(min)
  if (max != null) return formatSalary(max)
  return null
})

const attachmentName = computed(() => {
  const att = selectedAttachment.value
  if (!att) return ''
  if (att.file_original_name) return att.file_original_name
  const parts = att.file_url.split('/')
  return decodeURIComponent(parts[parts.length - 1].split('?')[0])
})

const fileExt = computed(() => {
  const name = attachmentName.value.toLowerCase()
  const dot = name.lastIndexOf('.')
  return dot !== -1 ? name.slice(dot + 1) : ''
})

const currentIsPdf = computed(() => {
  const att = selectedAttachment.value
  if (!att) return false
  const url = att.file_url || ''
  const origName = (att.file_original_name || '').toLowerCase()
  if (url.includes('/raw/upload/')) return true
  if (origName.endsWith('.pdf')) return true
  return fileExt.value === 'pdf'
})

const currentIsImage = computed(() => {
  if (currentIsPdf.value) return false
  const att = selectedAttachment.value
  if (!att) return false
  const url = att.file_url || ''
  if (url.includes('/image/upload/')) return true
  return ['png', 'jpg', 'jpeg', 'gif', 'webp'].includes(fileExt.value)
})
</script>

<style scoped>
.job-detail {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.job-detail__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 24px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.job-detail__header-info {
  flex: 1;
  min-width: 0;
}

.job-detail__company {
  font-size: 1.375rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px;
  line-height: 1.3;
}

.job-detail__title {
  font-size: 1rem;
  color: #64748b;
  margin: 0 0 10px;
}

.job-detail__badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.job-detail__actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.job-detail__btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 7px 14px;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

.job-detail__btn--secondary {
  background-color: #fff;
  color: #374151;
  border-color: #d1d5db;
}

.job-detail__btn--secondary:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.job-detail__btn--danger {
  background-color: #fff;
  color: #ef4444;
  border-color: #fca5a5;
}

.job-detail__btn--danger:hover {
  background-color: #fef2f2;
  border-color: #ef4444;
}

.job-detail__body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

.job-detail__fields {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-detail__field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.job-detail__field-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
}

.job-detail__field-value {
  font-size: 0.9375rem;
  color: #1e293b;
}

.job-detail__link {
  font-size: 0.9375rem;
  color: #6366f1;
  text-decoration: none;
  word-break: break-all;
}

.job-detail__link:hover {
  text-decoration: underline;
}

.job-detail__notes {
  font-size: 0.9375rem;
  color: #374151;
  white-space: pre-wrap;
  margin: 0;
  line-height: 1.6;
}

/* Job type tags */
.job-detail__tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.job-detail__tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 9999px;
  font-size: 0.8125rem;
  font-weight: 500;
}

.job-detail__tag--work {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
}

.job-detail__tag--employment {
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

/* Platform display */
.job-detail__platform {
  display: flex;
  align-items: center;
  gap: 8px;
}

.job-detail__platform-logo {
  width: 24px;
  height: 24px;
  object-fit: contain;
  border-radius: 4px;
}

.job-detail__platform-emoji {
  font-size: 1.25rem;
  line-height: 1;
}

.job-detail__platform-name {
  font-size: 0.9375rem;
  color: #1e293b;
  font-weight: 500;
}

/* Google Maps embed */
.job-detail__map {
  margin-top: 8px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.job-detail__map-iframe {
  width: 100%;
  height: 200px;
  border: none;
  display: block;
}

/* File preview button */
.job-detail__attachments {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.job-detail__file-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: #f5f3ff;
  border: 1px solid #c4b5fd;
  border-radius: 8px;
  color: #6366f1;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease;
  text-align: left;
}

.job-detail__file-btn:hover {
  background: #ede9fe;
  border-color: #a78bfa;
}

.job-detail__file-btn-hint {
  font-size: 0.75rem;
  color: #a78bfa;
  font-weight: 400;
}

/* File preview modal */
.file-modal__overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 24px;
}

.file-modal__card {
  background: #fff;
  border-radius: 12px;
  width: 100%;
  max-width: 860px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.file-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
  gap: 12px;
}

.file-modal__title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-modal__header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.file-modal__open-btn {
  font-size: 0.8125rem;
  color: #6366f1;
  text-decoration: none;
  padding: 4px 10px;
  border: 1px solid #c4b5fd;
  border-radius: 6px;
  transition: background-color 0.15s ease;
}

.file-modal__open-btn:hover {
  background: #f5f3ff;
}

.file-modal__close {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  color: #94a3b8;
  padding: 0 4px;
  border-radius: 4px;
  transition: color 0.15s ease;
}

.file-modal__close:hover {
  color: #1e293b;
}

.file-modal__body {
  flex: 1;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  min-height: 300px;
}

.file-modal__image {
  max-width: 100%;
  max-height: 75vh;
  object-fit: contain;
  display: block;
}

.file-modal__iframe {
  width: 100%;
  height: 75vh;
  border: none;
  display: block;
}

.file-modal__fallback {
  text-align: center;
  color: #64748b;
  padding: 48px;
}

.file-modal__fallback p {
  margin: 0 0 16px;
}

.file-modal__download {
  color: #6366f1;
  font-weight: 500;
  text-decoration: none;
}

.file-modal__pdf-wrapper {
  width: 100%;
  height: 75vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-modal__loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #64748b;
  font-size: 0.875rem;
}

.file-modal__spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e2e8f0;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Modal transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-active .file-modal__card,
.modal-leave-active .file-modal__card {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .file-modal__card {
  transform: scale(0.95) translateY(10px);
}
.modal-leave-to .file-modal__card {
  transform: scale(0.95) translateY(10px);
  opacity: 0;
}
</style>