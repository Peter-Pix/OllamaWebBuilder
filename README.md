# Ollama Web Builder  

A lightweight, browser‑only web application that lets you **chat with an AI model (via Ollama)** to generate, edit, and preview web‑app code in real time.  
Build single‑file or multi‑file projects, export them, and keep a running context so the AI can keep track of your design decisions.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Running](#installation--running)
- [Usage](#usage)
  - [Chat Panel](#chat-panel)
  - [Code Panel](#code-panel)
  - [Preview Panel](#preview-panel)
  - [Context Panel](#context-panel)
  - [Settings Panel](#settings-panel)
- [Configuration](#configuration)
  - [Ollama Server](#ollama-server)
  - [File Mode](#file-mode)
  - [Project Name & System Prompt](#project-name--system-prompt)
- [Exporting Projects](#exporting-projects)
- [How It Works](#how-it-works)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

| Feature | Description |
|---------|-------------|
| **AI‑Powered Chat** | Ask the model to write, refactor, or explain code. |
| **Live Code Editor** | A simple textarea editor that supports single‑file or multi‑file (HTML/CSS/JS) layouts. |
| **Instant Preview** | Render the current code in an `<iframe>` for instant visual feedback. |
| **Context Management** | Persist project goals and optionally include the current code in every AI request. |
| **Settings** | Configure Ollama URL, file mode, project name, and a custom system prompt. |
| **Export** | Download the project as a single HTML file or separate files. |
| **No Build Required** | Pure HTML/JS/CSS – open `index.html` in any modern browser. |

---

## Architecture

```
┌─────────────────────┐
│      Browser UI     │
│  (index.html + js)  │
└───────┬──────────────┘
        │
        ▼
┌─────────────────────┐
│   Ollama Server     │
│  (REST API)         │
└─────────────────────┘
```

* The UI sends POST requests to the Ollama API (`/api/chat/completions`).
* The API returns streamed responses that are appended to the chat window.
* Code changes are automatically rendered in the preview iframe.
* Settings and context are stored in the browser’s `localStorage` for persistence.

---

## Prerequisites

| Requirement | Minimum Version |
|-------------|-----------------|
| **Web Browser** | Chrome / Edge / Firefox (latest) |
| **Ollama** | 0.1.0+ (any model you want to use) |

> **Tip** – Ollama can be installed locally with a single command:  
> ```bash
> curl -fsSL https://ollama.ai/install.sh | sh
> ```

---

## Installation & Running

The project is **static** – no build step is required.

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Peter-Pix/OllamaWebBuilder.git
   cd OllamaWebBuilder
   ```

2. **Start Ollama** (if not already running)  
   ```bash
   ollama serve
   ```

3. **Open the app**  
   *Option 1 – Direct File*  
   Open `index.html` in your browser (double‑click or `open index.html`).

   *Option 2 – Local HTTP Server*  
   ```bash
   npx http-server .
   ```
   Then visit `http://localhost:8080` (or the port shown).

> **Note** – Because the app uses `fetch` to talk to `http://localhost:11434`, you must run it from a web server (or use the file protocol) for the API calls to work.

---

## Usage

### Chat Panel

| Action | Button / Key | Description |
|--------|--------------|-------------|
| **Send Message** | `Send Message` button or `Ctrl+Enter` | Sends the current textarea content to Ollama. |
| **Set Context** | `Set Context` button | Opens the *Context Panel* to add project goals. |
| **Save Chat** | `Save Chat` button | (Future feature – placeholder). |

> The chat starts with a default greeting from the assistant.  
> Every message is appended to the chat history and displayed with the assistant’s response.

### Code Panel

* **Tabs** – Switch between `index.html` (single file) or `index.html / style.css / script.js` (multi‑file).  
* **Settings** – Opens the *Settings Panel* to change file mode, project name, etc.  
* **Export** – Downloads the current project.  

### Preview Panel

* **Live Preview** – The iframe automatically updates when the code changes.    

### Context Panel

* **Project Requirements** – Write a short description of what the project should accomplish.  
* **Include Code Context** – When checked, the current code is sent to the AI with every request.  
* **Clear / Save** – Persist or reset the context.

### Settings Panel

| Setting | Purpose |
|---------|---------|
| **File Mode** | `single` → All code in one file; `multi` → Separate HTML/CSS/JS files. |
| **Project Name** | Used for the `<title>` tag. |
| **Ollama URL** | Endpoint of your Ollama server (default `http://localhost:11434`). |
| **Custom System Prompt** | Override the default system prompt that instructs the AI. |

> Settings are saved to `localStorage` and applied immediately.

---

## Configuration

### Ollama Server

The app talks to the Ollama REST API.  
Default URL: `http://localhost:11434`  
If your server is elsewhere, change the **Ollama URL** in the Settings panel.

```json
{
  "ollamaUrl": "http://your-ollama-host:11434"
}
```

### File Mode

* **Single File Mode** – All HTML, CSS, and JS are embedded in `index.html`.  
* **Multi‑File Mode** – The code is split into `index.html`, `style.css`, and `script.js`.  
  The preview automatically injects the CSS/JS via `<link>` and `<script>` tags.

### Project Name & System Prompt

* **Project Name** – Used for the `<title>` tag.  
* **System Prompt** – The default prompt tells the AI to output a complete, functional web page.  
  Feel free to modify it to suit your workflow.

---

## Exporting Projects

* **Single File** – Downloads `index.html`.  
* **Multi‑File** – Downloads `index.html`, `style.css`, and `script.js` (each as separate files).  
  The export logic can be extended to a ZIP archive if needed.

---

## How It Works

1. **Model Selection** – On load, the app fetches available models from Ollama (`/api/tags`) and populates the dropdown.  
2. **Chat Flow**  
   * User types a prompt → `Send Message` → POST to `/api/chat/completions`.  
   * The request includes:  
     * `model`: selected model  
     * `messages`: conversation history + optional context  
     * `stream`: true (to receive partial responses).  
   * The response is streamed and appended to the chat in real time.  
3. **Code Generation** – The assistant’s response is parsed for code blocks (` ```html `, ` ```css `, etc.) and inserted into the appropriate editor tab.  
4. **Preview Update** – Whenever the editor changes, the iframe’s `srcdoc` is updated to render the current code.  
5. **Context & Settings** – Stored in `localStorage`; changes immediately affect subsequent requests.

---

## Contribution Guidelines

1. **Fork** the repository.  
2. Create a new branch.
3. Commit your changes with clear messages.  
4. Open a Pull Request and describe the changes.  

**Code Style** – Vanilla JS, CSS, and HTML.  
**Testing** – Manual testing is sufficient for now; add unit tests if you wish.  

---

## License

MIT © 2025 [Petr Piskáček]  
See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* **Ollama** – for the open‑source LLM hosting platform.  
* **Vanilla JS** – keeping the app lightweight and easy to run.  
* **Open Source Community** – for inspiring this project.

---

Happy coding!

---
