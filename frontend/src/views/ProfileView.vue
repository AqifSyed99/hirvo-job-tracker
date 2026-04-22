<template>
  <div class="profile-page">
    <div class="profile-header">
      <div>
        <h1>My Profile</h1>
        <p>Manage your personal information</p>
      </div>
      <button v-if="!editing" class="btn btn--outline" @click="startEdit">
        ✏️ Edit Profile
      </button>
    </div>

    <LoadingSpinner v-if="profileStore.loading && !profileStore.profile" message="Loading profile..." />

    <div v-else class="profile-content">
      <!-- Avatar + name card -->
      <div class="profile-card avatar-card">
        <div class="avatar-wrapper">
          <!-- Show preview if new avatar selected, else show current -->
          <img
            v-if="avatarPreview || profileStore.profile?.avatar_url"
            :src="avatarPreview || profileStore.profile.avatar_url"
            alt="Avatar"
            class="avatar-img"
          />
          <div v-else class="avatar-placeholder">
            {{ avatarInitials }}
          </div>

          <!-- Pencil overlay — only shown in edit mode -->
          <label v-if="editing" class="avatar-edit-overlay" title="Change photo">
            <span class="avatar-pencil">✏️</span>
            <input
              type="file"
              accept=".png,.jpg,.jpeg"
              class="avatar-input"
              ref="avatarInput"
              @change="handleAvatarSelect"
            />
          </label>
        </div>

        <div class="avatar-info">
          <div class="avatar-name">
            {{ profileStore.profile?.full_name || profileStore.profile?.email || '—' }}
          </div>
          <div class="avatar-email">{{ profileStore.profile?.email }}</div>
          <div v-if="avatarPreview && editing" class="avatar-pending-hint">
            📎 New photo selected — click Save Changes to apply
          </div>
        </div>
      </div>

      <!-- Info card — view mode -->
      <div v-if="!editing" class="profile-card info-card">
        <h2 class="card-title">Personal Information</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Full Name</span>
            <span class="info-value">{{ profileStore.profile?.full_name || '—' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Email</span>
            <span class="info-value">{{ profileStore.profile?.email }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Phone Number</span>
            <span class="info-value">{{ profileStore.profile?.phone || '—' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">IC Number</span>
            <span class="info-value">{{ profileStore.profile?.ic_number || '—' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Date of Birth</span>
            <span class="info-value">{{ formatDate(profileStore.profile?.date_of_birth) || '—' }}</span>
          </div>
          <div class="info-item info-item--full">
            <span class="info-label">Address</span>
            <span class="info-value">{{ profileStore.profile?.address || '—' }}</span>
          </div>
        </div>
      </div>

      <!-- Edit form card -->
      <div v-else class="profile-card form-card">
        <h2 class="card-title">Edit Personal Information</h2>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input v-model="form.full_name" type="text" class="form-input" placeholder="e.g. Ahmad bin Ali" />
          </div>

          <div class="form-group">
            <label class="form-label">Email</label>
            <input :value="profileStore.profile?.email" type="email" class="form-input form-input--readonly" readonly />
          </div>

          <div class="form-group">
            <label class="form-label">Phone Number</label>
            <input v-model="form.phone" type="tel" class="form-input" placeholder="e.g. 012-3456789" />
          </div>

          <div class="form-group">
            <label class="form-label">IC Number</label>
            <input v-model="form.ic_number" type="text" class="form-input" placeholder="e.g. 990101-14-1234" />
          </div>

          <div class="form-group">
            <label class="form-label">Date of Birth</label>
            <input v-model="form.date_of_birth" type="date" class="form-input" />
          </div>

          <div class="form-group form-group--full">
            <label class="form-label">Address</label>
            <textarea v-model="form.address" class="form-textarea" rows="3" placeholder="e.g. No. 1, Jalan Bukit Bintang, 55100 Kuala Lumpur"></textarea>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn btn--secondary" @click="cancelEdit" :disabled="saving">
            Cancel
          </button>
          <button class="btn btn--primary" @click="handleSave" :disabled="saving">
            <span v-if="saving" class="btn-spinner"></span>
            <span>{{ saving ? 'Saving…' : 'Save Changes' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useProfileStore } from '../store/profile'
import { useToastStore } from '../store/toast'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

const profileStore = useProfileStore()
const toast = useToastStore()

const editing = ref(false)
const saving = ref(false)
const avatarPreview = ref(null)
const pendingAvatarFile = ref(null)
const avatarInput = ref(null)

const form = reactive({
  full_name: '',
  phone: '',
  ic_number: '',
  date_of_birth: '',
  address: '',
})

function populateForm(profile) {
  if (!profile) return
  form.full_name = profile.full_name || ''
  form.phone = profile.phone || ''
  form.ic_number = profile.ic_number || ''
  form.date_of_birth = profile.date_of_birth || ''
  form.address = profile.address || ''
}

onMounted(async () => {
  await profileStore.fetchProfile()
  populateForm(profileStore.profile)
})

watch(() => profileStore.profile, (p) => {
  if (!editing.value) populateForm(p)
})

const avatarInitials = computed(() => {
  const name = profileStore.profile?.full_name || profileStore.profile?.email || '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

function formatDate(dateStr) {
  if (!dateStr) return null
  const d = new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('en-MY', { day: 'numeric', month: 'long', year: 'numeric' })
}

function startEdit() {
  populateForm(profileStore.profile)
  editing.value = true
}

function cancelEdit() {
  editing.value = false
  avatarPreview.value = null
  pendingAvatarFile.value = null
  populateForm(profileStore.profile)
}

function handleAvatarSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  pendingAvatarFile.value = file
  // Show local preview immediately without uploading
  const reader = new FileReader()
  reader.onload = (e) => { avatarPreview.value = e.target.result }
  reader.readAsDataURL(file)
}

async function handleSave() {
  saving.value = true
  try {
    const payload = { ...form }
    if (pendingAvatarFile.value) {
      payload.avatar = pendingAvatarFile.value
    }
    await profileStore.updateProfile(payload)
    toast.success('Profile updated successfully!')
    editing.value = false
    avatarPreview.value = null
    pendingAvatarFile.value = null
  } catch {
    toast.error(profileStore.error || 'Failed to update profile.')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.profile-page {
  padding: 32px;
}

.profile-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
  gap: 16px;
}

.profile-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px;
}

.profile-header p {
  font-size: 0.9375rem;
  color: #6b7280;
  margin: 0;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Cards */
.profile-card {
  background: #fff;
  border-radius: 12px;
  padding: 28px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
}

/* Avatar card */
.avatar-card {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
  width: 88px;
  height: 88px;
}

.avatar-img,
.avatar-placeholder {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Pencil overlay on hover */
.avatar-edit-overlay {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.avatar-wrapper:hover .avatar-edit-overlay {
  opacity: 1;
}

.avatar-pencil {
  font-size: 1.25rem;
}

.avatar-input {
  display: none;
}

.avatar-info {
  flex: 1;
  min-width: 0;
}

.avatar-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.avatar-email {
  font-size: 0.875rem;
  color: #6b7280;
}

.avatar-pending-hint {
  font-size: 0.8rem;
  color: #f59e0b;
  margin-top: 6px;
}

/* View mode info grid */
.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item--full {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
}

.info-value {
  font-size: 0.9375rem;
  color: #1e293b;
}

/* Edit form */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group--full {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #374151;
}

.form-input,
.form-textarea {
  padding: 9px 12px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9375rem;
  color: #111827;
  background: #fff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  outline: none;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

.form-input--readonly {
  background: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 22px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: background-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.btn--primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn--primary:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 6px 18px rgba(99, 102, 241, 0.4);
}

.btn--primary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn--secondary {
  background: #fff;
  color: #374151;
  border-color: #d1d5db;
}

.btn--secondary:hover:not(:disabled) {
  background: #f9fafb;
}

.btn--secondary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn--outline {
  background: transparent;
  color: #6366f1;
  border-color: #6366f1;
}

.btn--outline:hover {
  background: #f5f3ff;
}

.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 640px) {
  .profile-page { padding: 16px; }
  .profile-header { flex-direction: column; }
  .form-grid, .info-grid { grid-template-columns: 1fr; }
  .avatar-card { flex-direction: column; text-align: center; }
}
</style>
