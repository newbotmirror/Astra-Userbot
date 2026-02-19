# 🌟 Astra Userbot (dev-beta)

A powerful, modular, and professional-grade WhatsApp Userbot framework built on top of the **Astra Engine**. Designed for efficiency, ease of use, and extensibility.

### 🚀 One-Click Deployments

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/paman7647/Astra-Userbot)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

*For advanced options including **Localhost**, **Docker / VPS**, please see our **[Deployment Guide](DEPLOYMENT.md)**.*

---

## 🚀 Key Features

- **Modular Plugin System**: Easily add or remove features via the `commands/` directory.
- **AI Integration**: Powered by Google's latest **Gemini 3 Flash Preview** models.
- **Media Suite**: Professional-grade media downloading capabilities (YouTube, Instagram, etc.) via a robust JS bridge.
- **State Management**: Persistent storage for AFK, sudo users, permits, and customizable notes.
- **Developer-First**: Clean, well-commented Python code with systemic setup automation.

---

### 🖥️ Local & VPS Setup

Astra Userbot provides a **one-liner auto-installer** that clones the repository and automatically sets up all dependencies (Python, Node.js, FFmpeg, yt-dlp) for your platform.

#### **For Windows (PowerShell)**
Run PowerShell as Administrator and execute:
```powershell
iwr -useb https://raw.githubusercontent.com/paman7647/Astra-Userbot/main/install.ps1 | iex
```

#### **For macOS & Linux (Terminal/VPS)**
Open your terminal and execute:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/paman7647/Astra-Userbot/main/install.sh)
```

For advanced deployments (Docker, custom cloud), see our **[Deployment Guide](DEPLOYMENT.md)**.

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and provide your credentials:
   - `GEMINI_API_KEY`: Your Google AI API key.
   - `OWNER_WHATSAPP_ID`: Your WhatsApp ID (e.g., `910000000000@c.us`).

---

## 🏃 Running the Bot

### Initial Authentication
On your first run, you may need to scan a QR code. Start in non-headless mode:

```bash
export ASTRA_HEADLESS="false"
python3 bot.py
```

### Regular Operation
Once authenticated, simply run:

```bash
python3 bot.py
```

---

## 📚 Common Commands

| Command | Alias | Description |
| :--- | :--- | :--- |
| `.alive` | | Check if the bot is online and view system stats. |
| `.ai` | `.chat` | Interact with Gemini AI. |
| `.yt` | `.youtube` | Download YouTube videos or audio. |
| `.ig` | `.reel` | Download Instagram reels/posts. |
| `.ping` | | Check bot latency. |

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
*Developed with ❤️ by Aman Kumar Pandey*
