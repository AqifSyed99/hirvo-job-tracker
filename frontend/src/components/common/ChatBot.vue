<template>
  <!-- Floating button -->
  <button
    class="chat-fab"
    @click="isOpen = !isOpen"
    :aria-label="isOpen ? 'Close chat' : 'Open Hirvo Assistant'"
    :title="isOpen ? 'Close' : 'Ask Hirvo Assistant'"
  >
    <svg v-if="!isOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    <svg v-else xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  </button>

  <!-- Chat window -->
  <Transition name="chat-window">
    <div v-if="isOpen" class="chat-window" role="dialog" aria-label="Hirvo Assistant">
      <!-- Header -->
      <div class="chat-header">
        <div class="chat-header-info">
          <div class="chat-avatar">🤖</div>
          <div>
            <div class="chat-title">Hirvo Assistant</div>
            <div class="chat-subtitle">Ask me anything about the system</div>
          </div>
        </div>
        <button class="chat-close" @click="isOpen = false" aria-label="Close">×</button>
      </div>

      <!-- Messages -->
      <div class="chat-messages" ref="messagesEl">
        <!-- Welcome message -->
        <div class="chat-msg chat-msg--bot">
          <div class="chat-bubble">
            👋 Hi! I'm Hirvo Assistant. Ask me anything about how to use the system — adding jobs, tracking applications, using the dashboard, and more!
          </div>
        </div>

        <div v-for="(msg, i) in messages" :key="i" class="chat-msg" :class="msg.role === 'user' ? 'chat-msg--user' : 'chat-msg--bot'">
          <div class="chat-bubble" v-html="formatMessage(msg.content)"></div>
        </div>

        <!-- Typing indicator -->
        <div v-if="loading" class="chat-msg chat-msg--bot">
          <div class="chat-bubble chat-bubble--typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-area">
        <input
          v-model="inputText"
          type="text"
          class="chat-input"
          placeholder="Ask a question…"
          @keydown.enter.prevent="sendMessage"
          :disabled="loading"
          ref="inputEl"
        />
        <button
          class="chat-send"
          @click="sendMessage"
          :disabled="loading || !inputText.trim()"
          aria-label="Send"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const inputText = ref('')
const loading = ref(false)
const messages = ref([])
const messagesEl = ref(null)
const inputEl = ref(null)

watch(isOpen, (open) => {
  if (open) {
    nextTick(() => inputEl.value?.focus())
  }
})

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

function formatMessage(text) {
  // Convert markdown-like formatting to HTML
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br/>')
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  loading.value = true
  await scrollToBottom()

  try {
    const response = await axios.post('/api/chat/', {
      messages: messages.value,
    })
    messages.value.push({ role: 'assistant', content: response.data.reply })
  } catch (err) {
    messages.value.push({
      role: 'assistant',
      content: 'Sorry, I encountered an error. Please try again.',
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}
</script>

<style scoped>
/* Floating action button */
.chat-fab {
  position: fixed;
  bottom: 28px;
  right: 28px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.5);
  z-index: 1500;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chat-fab:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 28px rgba(99, 102, 241, 0.6);
}

/* Chat window */
.chat-window {
  position: fixed;
  bottom: 96px;
  right: 28px;
  width: 360px;
  max-width: calc(100vw - 40px);
  height: 500px;
  max-height: calc(100vh - 120px);
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1499;
}

/* Header */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  flex-shrink: 0;
}

.chat-header-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-avatar {
  font-size: 1.5rem;
  width: 36px;
  height: 36px;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-title {
  font-size: 0.9375rem;
  font-weight: 600;
}

.chat-subtitle {
  font-size: 0.75rem;
  opacity: 0.8;
}

.chat-close {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
  padding: 0 4px;
  opacity: 0.8;
  transition: opacity 0.15s ease;
}

.chat-close:hover { opacity: 1; }

/* Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f8fafc;
}

.chat-msg {
  display: flex;
}

.chat-msg--user {
  justify-content: flex-end;
}

.chat-msg--bot {
  justify-content: flex-start;
}

.chat-bubble {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 0.875rem;
  line-height: 1.5;
  word-break: break-word;
}

.chat-msg--user .chat-bubble {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.chat-msg--bot .chat-bubble {
  background: #fff;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* Typing indicator */
.chat-bubble--typing {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 16px;
}

.chat-bubble--typing span {
  width: 7px;
  height: 7px;
  background: #94a3b8;
  border-radius: 50%;
  animation: bounce 1.2s infinite;
}

.chat-bubble--typing span:nth-child(2) { animation-delay: 0.2s; }
.chat-bubble--typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

/* Input area */
.chat-input-area {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border-top: 1px solid #f1f5f9;
  background: #fff;
  flex-shrink: 0;
}

.chat-input {
  flex: 1;
  padding: 9px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 20px;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.15s ease;
  background: #f8fafc;
}

.chat-input:focus {
  border-color: #6366f1;
  background: #fff;
}

.chat-send {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.chat-send:hover:not(:disabled) { transform: scale(1.08); }
.chat-send:disabled { opacity: 0.4; cursor: not-allowed; }

/* Window transition */
.chat-window-enter-active,
.chat-window-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.chat-window-enter-from,
.chat-window-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.97);
}
</style>
