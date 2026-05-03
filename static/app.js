// ─── State ───────────────────────────────────────────────────────────────────
const state = {
    chatHistory: [],
    isLoading: false,
    lastRequest: null,
};

// ─── DOM refs ─────────────────────────────────────────────────────────────────
const chatWindow = document.getElementById('chatWindow');
const generateBtn = document.getElementById('generateBtn');
const newChatBtn = document.getElementById('newChatBtn');
const subjectSel = document.getElementById('subject');
const examTypeSel = document.getElementById('examType');
const numQRange = document.getElementById('numQuestions');
const numQDisplay = document.getElementById('numQDisplay');
const activeBadge = document.getElementById('activeBadge');

// ─── Range display ─────────────────────────────────────────────────────────────
numQRange.addEventListener('input', () => {
    numQDisplay.textContent = numQRange.value;
});

// ─── Generate ─────────────────────────────────────────────────────────────────
generateBtn.addEventListener('click', handleGenerate);
newChatBtn.addEventListener('click', resetChat);

async function handleGenerate() {
    if (state.isLoading) return;

    const subject = subjectSel.value;
    const examType = examTypeSel.value;
    const numQ = parseInt(numQRange.value);

    if (!subject || !examType) {
        showError('Please select both a Subject and an Exam Type.');
        return;
    }

    // Remove empty state if present
    const emptyState = chatWindow.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    // Update header badge
    activeBadge.textContent = `${subject} · ${examType}`;
    activeBadge.classList.add('active');

    // User bubble
    const userText = `Generate ${numQ} practice questions for ${subject} (${examType})`;
    appendUserBubble(userText);

    // Add to history
    state.chatHistory.push({ role: 'user', content: userText });

    // Thinking indicator
    const thinkingId = appendThinking();
    setLoading(true);

    state.lastRequest = { subject, examType, numQuestions: numQ };

    try {
        const res = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                subject,
                exam_type: examType,
                num_questions: numQ,
                chat_history: state.chatHistory.slice(-10), // last 10 turns
            }),
        });

        removeThinking(thinkingId);

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Server error');
        }

        const data = await res.json();
        appendAIBubble(data, subject, examType);

        // Add AI response to history
        state.chatHistory.push({
            role: 'assistant',
            content: data.formatted_text,
        });

    } catch (err) {
        removeThinking(thinkingId);
        showError(err.message);
    } finally {
        setLoading(false);
    }
}

// ─── Bubble builders ──────────────────────────────────────────────────────────
function appendUserBubble(text) {
    const msg = document.createElement('div');
    msg.className = 'message user';
    msg.innerHTML = `
    <div class="avatar">👤</div>
    <div class="bubble">
      <div class="meta">You</div>
      ${escapeHtml(text)}
    </div>`;
    chatWindow.appendChild(msg);
    scrollToBottom();
}

function appendAIBubble(data, subject, examType) {
    const msg = document.createElement('div');
    msg.className = 'message assistant';

    const questionsHtml = data.questions.length > 0
        ? renderQuestions(data.questions)
        : `<p>${escapeHtml(data.formatted_text)}</p>`;

    const msgId = 'msg-' + Date.now();
    msg.id = msgId;
    msg.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="bubble">
      <div class="meta">AI • ${subject} ${examType} • ${data.questions.length} questions</div>
      <div class="questions-list">${questionsHtml}</div>
      <div class="bubble-actions">
        <button class="action-btn copy-btn" onclick="copyQuestions('${msgId}')">📋 Copy</button>
        <button class="action-btn" onclick="regenerate()">🔄 Regenerate</button>
      </div>
    </div>`;
    chatWindow.appendChild(msg);
    scrollToBottom();
}

function renderQuestions(questions) {
    return questions.map((q, i) => {
        // Strip leading number if already present
        const clean = q.replace(/^\d+\.\s*/, '').trim();
        return `
      <div class="question-item">
        <span class="q-num">${i + 1}.</span>
        <span class="q-text">${escapeHtml(clean)}</span>
      </div>`;
    }).join('');
}

// ─── Thinking indicator ───────────────────────────────────────────────────────
function appendThinking() {
    const id = 'thinking-' + Date.now();
    const msg = document.createElement('div');
    msg.className = 'message assistant thinking-msg';
    msg.id = id;
    msg.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="bubble">
      <div class="dots">
        <span></span><span></span><span></span>
      </div>
      Generating questions…
    </div>`;
    chatWindow.appendChild(msg);
    scrollToBottom();
    return id;
}

function removeThinking(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ─── Error ────────────────────────────────────────────────────────────────────
function showError(message) {
    const msg = document.createElement('div');
    msg.className = 'message assistant error-bubble';
    msg.innerHTML = `
    <div class="avatar">⚠️</div>
    <div class="bubble">
      <div class="meta">Error</div>
      ${escapeHtml(message)}
    </div>`;
    chatWindow.appendChild(msg);
    scrollToBottom();
}

// ─── Actions ──────────────────────────────────────────────────────────────────
function copyQuestions(msgId) {
    const msgEl = document.getElementById(msgId);
    if (!msgEl) return;
    const items = msgEl.querySelectorAll('.question-item');
    const text = Array.from(items).map((el, i) => {
        const q = el.querySelector('.q-text').textContent.trim();
        return `${i + 1}. ${q}`;
    }).join('\n');

    navigator.clipboard.writeText(text).then(() => {
        const btn = msgEl.querySelector('.copy-btn');
        btn.textContent = '✅ Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.textContent = '📋 Copy';
            btn.classList.remove('copied');
        }, 2000);
    });
}

function regenerate() {
    if (!state.lastRequest || state.isLoading) return;
    // Re-trigger with last known params
    subjectSel.value = state.lastRequest.subject;
    examTypeSel.value = state.lastRequest.examType;
    numQRange.value = state.lastRequest.numQuestions;
    numQDisplay.textContent = state.lastRequest.numQuestions;
    handleGenerate();
}

function resetChat() {
    state.chatHistory = [];
    state.lastRequest = null;
    activeBadge.textContent = 'Ready';
    activeBadge.classList.remove('active');
    chatWindow.innerHTML = emptyStateHTML();
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function setLoading(val) {
    state.isLoading = val;
    generateBtn.disabled = val;
    generateBtn.innerHTML = val
        ? `<span class="dots"><span></span><span></span><span></span></span> Thinking…`
        : `✨ Generate Questions`;
}

function scrollToBottom() {
    chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
}

function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function emptyStateHTML() {
    return `
    <div class="empty-state">
      <div class="empty-icon">🎓</div>
      <h2>AI Question Generator</h2>
      <p>Select a subject and exam type, then click <strong>Generate Questions</strong> to get started.</p>
      <div class="quick-tips">
        <span class="tip">JEE · Mathematics</span>
        <span class="tip">NEET · Biology</span>
        <span class="tip">GATE · CS</span>
        <span class="tip">SAT · Physics</span>
      </div>
    </div>`;
}
