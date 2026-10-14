let conversations = [];
let activePartnerId = null;
let activePartner = null;
let conversationsTimer = null;
let messagesTimer = null;
let me = {};

async function initChat() {
  const ok = await Dashboard.init({ role: 'user', active: 'chat', title: 'Messages', subtitle: 'Chat with buyers, sellers and owners' });
  if (!ok) return;
  me = Dashboard.currentUser();
  document.getElementById('chatForm').addEventListener('submit', sendMessage);
  await loadConversations();

  const params = new URLSearchParams(window.location.search);
  const withId = params.get('with');
  if (withId) {
    const existing = conversations.find((c) => c.partner && String(c.partner.id) === String(withId));
    const partner = existing ? existing.partner : { id: Number(withId), name: params.get('name') || 'User' };
    openConversation(partner.id, partner);
  }

  conversationsTimer = setInterval(loadConversations, 20000);
}

async function loadConversations() {
  try {
    const list = await ChatAPI.getConversations();
    conversations = Array.isArray(list) ? list : [];
    renderConversations();
  } catch (error) {
    const box = document.getElementById('convoList');
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function renderConversations() {
  const box = document.getElementById('convoList');
  if (!conversations.length) {
    renderInlineEmpty(box, '💬', 'No conversations yet');
    return;
  }
  box.innerHTML = conversations.map((c) => {
    const partner = c.partner || {};
    const active = String(partner.id) === String(activePartnerId) ? ' active' : '';
    const unread = c.unreadCount > 0 ? `<span class="cv-unread">${c.unreadCount}</span>` : '';
    return `<div class="convo-item${active}" onclick="openConversationById(${partner.id})">
      ${dashboardAvatar(partner)}
      <div class="convo-main">
        <div class="cv-name"><span>${escapeHtml(partner.name || 'User')}</span><span class="cv-time">${c.lastMessageAt ? timeAgo(c.lastMessageAt) : ''}</span></div>
        <div class="cv-last">${escapeHtml(c.lastMessage || '')}</div>
      </div>
      ${unread}
    </div>`;
  }).join('');
}

function openConversationById(partnerId) {
  const conv = conversations.find((c) => c.partner && String(c.partner.id) === String(partnerId));
  return openConversation(partnerId, conv ? conv.partner : { id: partnerId, name: 'User' });
}

async function openConversation(partnerId, partner) {
  activePartnerId = partnerId;
  activePartner = partner || { id: partnerId, name: 'User' };
  renderConversations();

  const head = document.getElementById('chatHead');
  head.innerHTML = `
    ${dashboardAvatar(activePartner)}
    <div class="list-main">
      <div class="lr-title">${escapeHtml(activePartner.name || 'User')}</div>
      <div class="lr-sub">${escapeHtml(activePartner.city || '')}</div>
    </div>
    <a href="../../search-properties.html" class="btn btn-secondary btn-sm" style="margin-left:auto">Browse</a>
  `;
  document.getElementById('chatForm').style.display = 'flex';

  await loadMessages();
  try {
    await ChatAPI.markRead(partnerId);
    const conv = conversations.find((c) => c.partner && String(c.partner.id) === String(partnerId));
    if (conv) conv.unreadCount = 0;
    renderConversations();
    Dashboard.unreadCount = Math.max(0, (Dashboard.unreadCount || 0) - 1);
    Dashboard.renderSidebar();
  } catch (error) {
    /* ignore */
  }

  if (messagesTimer) clearInterval(messagesTimer);
  messagesTimer = setInterval(() => {
    if (activePartnerId) loadMessages(true);
  }, 8000);
}

async function loadMessages(silent) {
  const body = document.getElementById('chatBody');
  if (!silent) {
    body.innerHTML = '<div class="loading-block"><div class="row-skeleton"></div><div class="row-skeleton"></div></div>';
  }
  try {
    const res = await ChatAPI.getWith(activePartnerId);
    const messages = (res && res.content) || [];
    renderMessages(messages);
  } catch (error) {
    if (!silent) renderInlineEmpty(body, '⚠️', error.message);
  }
}

function renderMessages(messages) {
  const body = document.getElementById('chatBody');
  if (!messages.length) {
    renderInlineEmpty(body, '💬', 'No messages yet. Say hello!');
    return;
  }
  body.innerHTML = messages.map((m) => {
    const mine = me && m.sender && String(m.sender.id) === String(me.id);
    return `<div class="chat-bubble ${mine ? 'me' : 'them'}">
      ${escapeHtml(m.message)}
      <span class="bubble-time">${timeAgo(m.timestamp)}</span>
    </div>`;
  }).join('');
  body.scrollTop = body.scrollHeight;
}

async function sendMessage(event) {
  event.preventDefault();
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (!message || !activePartnerId) return;
  input.value = '';
  try {
    const last = conversations.find((c) => c.partner && String(c.partner.id) === String(activePartnerId));
    let listingType = null;
    let listingId = null;
    if (last && last.listingType) {
      listingType = last.listingType;
      listingId = last.listingId;
    }
    await ChatAPI.send({ receiverId: activePartnerId, listingType, listingId, message });
    await loadMessages(true);
    loadConversations();
  } catch (error) {
    showToast(error.message, 'error');
    input.value = message;
  }
}

document.addEventListener('DOMContentLoaded', initChat);
