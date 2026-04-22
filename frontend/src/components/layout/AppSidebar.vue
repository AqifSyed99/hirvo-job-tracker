<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { useProfileStore } from '../../store/profile'
import logo from '../../assets/logo.jpg'

const authStore = useAuthStore()
const profileStore = useProfileStore()

onMounted(() => {
  if (!profileStore.profile) profileStore.fetchProfile()
})

const initials = computed(() => {
  const name = profileStore.profile?.full_name || authStore.user?.email || '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})
</script>

<template>
  <aside class="sidebar">
    <!-- Brand -->
    <div class="sidebar-brand">
      <img :src="logo" alt="Hirvo" class="brand-logo" />
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <RouterLink to="/dashboard" class="nav-link">
        <span class="nav-icon">📊</span>
        <span>Dashboard</span>
      </RouterLink>
      <RouterLink to="/jobs" class="nav-link">
        <span class="nav-icon">📋</span>
        <span>Job List</span>
      </RouterLink>
      <RouterLink to="/profile" class="nav-link">
        <span class="nav-icon">👤</span>
        <span>Profile</span>
      </RouterLink>
    </nav>

    <!-- User info + logout -->
    <div class="sidebar-footer">
      <RouterLink to="/profile" class="user-profile-link">
        <div class="user-avatar">
          <img v-if="profileStore.profile?.avatar_url" :src="profileStore.profile.avatar_url" alt="avatar" class="user-avatar-img" />
          <span v-else class="user-avatar-initials">{{ initials }}</span>
        </div>
        <div class="user-info">
          <div class="user-name">{{ profileStore.profile?.full_name || 'My Profile' }}</div>
          <div class="user-email-text">{{ authStore.user?.email }}</div>
        </div>
      </RouterLink>
      <button class="logout-btn" @click="authStore.logout()">
        <span class="nav-icon">🚪</span>
        <span>Logout</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 240px;
  min-width: 240px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background-color: #0f172a;
  color: #e2e8f0;
  display: flex;
  flex-direction: column;
  z-index: 100;
}

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-logo {
  width: 100%;
  max-width: 160px;
  height: auto;
  object-fit: contain;
}

.brand-icon {
  font-size: 22px;
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #f1f5f9;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.15s ease, color 0.15s ease;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.08);
  color: #f1f5f9;
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: #f1f5f9;
  font-weight: 600;
  border-left-color: #818cf8;
}

.nav-icon {
  font-size: 16px;
  flex-shrink: 0;
}

/* Footer */
.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-profile-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.user-profile-link:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex-shrink: 0;
  overflow: hidden;
}

.user-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar-initials {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-email-text {
  font-size: 0.7rem;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.logout-btn:hover {
  background-color: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
}
</style>
