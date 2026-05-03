Create a full-stack AI-powered web application using an Agentic framework with the following requirements:

### 🎯 Goal

Build an intelligent Question Generator Agent that:

* Accepts input: **Subject** and **Exam Type**
* Uses predefined knowledge/context
* Generates **similar practice questions** dynamically
* Provides a chatbot-like interactive experience

---

### 🧠 AI Integration

* Use **Gemini API (latest version)**
* Implement LLM interaction with:

  * **System Prompt**
  * **User Prompt**

---

### ⚙️ Agent Behavior

#### System Prompt (fixed)

"You are an expert exam question generator. Based on the given subject, exam type, and existing context, generate high-quality, realistic, and practice-oriented questions. Maintain the difficulty level and pattern relevant to the exam. Ensure variety and clarity. Avoid repeating questions."

#### User Prompt (dynamic)

"Generate practice questions for:
Subject: {subject}
Exam Type: {examType}

Use this context:
{context}

Generate {n} similar questions."

---

### 🧩 Context Handling

* Store predefined context (JSON or DB)
* Context should include:

  * Sample questions
  * Patterns
  * Difficulty level
* Agent should retrieve relevant context before calling LLM

---

### 🖥️ UI Requirements (Chatbot Interface)

Create a modern interactive UI with:

* Chat window (like ChatGPT)
* Input fields:

  * Subject (dropdown or text)
  * Exam Type (dropdown)
* "Generate Questions" button
* Chat-style response rendering:

  * User query bubble
  * AI response bubble
* Loading indicator (thinking state)

Optional:

* Regenerate button
* Copy questions button

---

### 🏗️ Tech Stack

* Frontend: React (with hooks)
* Backend: Node.js / Express (or serverless)
* API layer for Gemini integration
* Clean modular architecture

---

### 🔄 Agent Flow

1. User inputs subject + exam type
2. Fetch relevant context
3. Construct prompt (system + user)
4. Call Gemini API
5. Return formatted questions
6. Display in chat UI

---

### 📦 Output Format

* Numbered list of questions
* Clean formatting
* Optional: difficulty tag

---

### 🚀 Additional Features

* Maintain chat history
* Allow multiple queries
* Basic error handling for API failures

---

### 🎨 UI Design

* Minimal, modern (like ChatGPT)
* Smooth scrolling
* Responsive layout

---

Generate complete working code with:

* Frontend
* Backend
* API integration
* Sample context data
* Environment configuration for Gemini API key

Ensure code is clean, modular, and production-ready.
