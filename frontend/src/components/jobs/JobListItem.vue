<template>
  <div
    class="job-list-item"
    :class="{ 'job-list-item--selected': isSelected }"
    @click="$emit('select', entry)"
    role="button"
    tabindex="0"
    :aria-label="`${entry.company_name} - ${entry.job_title}`"
    @keydown.enter="$emit('select', entry)"
    @keydown.space.prevent="$emit('select', entry)"
  >
    <div class="job-list-item__main">
      <div class="job-list-item__header">
        <span class="job-list-item__company">{{ entry.company_name }}</span>
        <span
          class="job-list-item__badge"
          :style="{ backgroundColor: statusColor(entry.status) }"
        >{{ entry.status }}</span>
      </div>
      <div class="job-list-item__title">{{ entry.job_title }}</div>
      <div class="job-list-item__meta">
        <span v-if="entry.platform" class="job-list-item__platform">
          <template v-if="platformLogoUrl(entry.platform)">
            <img
              :src="platformLogoUrl(entry.platform)"
              :alt="entry.platform"
              class="job-list-item__platform-img"
              @error="(e) => { e.target.style.display='none'; e.target.nextElementSibling.style.display='inline' }"
            />
            <span style="display:none">{{ platformFallbackEmoji(entry.platform) }}</span>
          </template>
          <span v-else>{{ platformFallbackEmoji(entry.platform) }}</span>
          {{ entry.platform }}
        </span>
        <span v-if="entry.application_date" class="job-list-item__date">
          {{ formatDate(entry.application_date) }}
        </span>
        <span v-if="entry.location" class="job-list-item__location">
          📍 {{ entry.location }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  entry: { type: Object, required: true },
  isSelected: { type: Boolean, default: false },
})

defineEmits(['select'])

const STATUS_COLORS = {
  'Applied': '#3b82f6',
  'Phone Screen': '#f59e0b',
  'Interview': '#8b5cf6',
  'Offer': '#10b981',
  'Rejected': '#ef4444',
  'Withdrawn': '#94a3b8',
}

const PLATFORM_LOGOS = {
  'LinkedIn':     'https://www.google.com/s2/favicons?domain=linkedin.com&sz=32',
  'Indeed':       'https://www.google.com/s2/favicons?domain=indeed.com&sz=32',
  'Jobstreet':    'https://www.google.com/s2/favicons?domain=jobstreet.com.my&sz=32',
  'MyFutureJobs': 'https://www.google.com/s2/favicons?domain=myfuturejobs.gov.my&sz=32',
  'Jora':         'https://www.google.com/s2/favicons?domain=jora.com&sz=32',
  'Maukerja':     'https://www.google.com/s2/favicons?domain=maukerja.my&sz=32',
  'SPA':          'https://www.google.com/s2/favicons?domain=malaysia.gov.my&sz=32',
}

const PLATFORM_EMOJI = {
  'MyFutureJobs': '🌐',
  'Maukerja':     '🌐',
  'SPA':          '🌐',
}

function platformLogoUrl(platform) {
  return PLATFORM_LOGOS[platform] || null
}

function platformFallbackEmoji(platform) {
  return PLATFORM_EMOJI[platform] || '🌐'
}

function platformLogo(platform) {
  return PLATFORM_LOGOS[platform] ? '' : '🌐'
}

function statusColor(status) {
  return STATUS_COLORS[status] || '#94a3b8'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr + 'T00:00:00')
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<style scoped>
.job-list-item {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f1f5f9;
  transition: background-color 0.15s ease;
  outline: none;
}

.job-list-item:hover {
  background-color: #f8fafc;
}

.job-list-item:focus-visible {
  outline: 2px solid #6366f1;
  outline-offset: -2px;
}

.job-list-item--selected {
  background-color: #eef2ff;
  border-left: 3px solid #6366f1;
}

.job-list-item--selected:hover {
  background-color: #e0e7ff;
}

.job-list-item__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}

.job-list-item__company {
  font-weight: 600;
  font-size: 0.9375rem;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.job-list-item__badge {
  flex-shrink: 0;
  display: inline-block;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 0.6875rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.job-list-item__title {
  font-size: 0.8125rem;
  color: #64748b;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.job-list-item__meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.job-list-item__date,
.job-list-item__location,
.job-list-item__platform {
  font-size: 0.75rem;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 4px;
}

.job-list-item__platform-img {
  width: 14px;
  height: 14px;
  object-fit: contain;
}
</style>
