"use client"

import { useState, useEffect, useRef } from "react"
import "./globals.css"

export default function ChatBot() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const [isOnline, setIsOnline] = useState(true)
  const [showSettings, setShowSettings] = useState(false)
  const [darkMode, setDarkMode] = useState(false)
  const [fontSize, setFontSize] = useState("medium")
  const [stats, setStats] = useState(null)
  const [showStats, setShowStats] = useState(false)
  const messagesEndRef = useRef(null)
  const sessionId = useRef(Math.random().toString(36).substring(7))
  const inputRef = useRef(null)

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessage = {
      id: "welcome-" + Date.now(),
      text: "👋 Hello! I'm your AI assistant. I'm here to help you with any questions or tasks you might have. How can I assist you today?",
      sender: "bot",
      timestamp: new Date(),
    }
    setMessages([welcomeMessage])

    // Check online status
    const handleOnline = () => setIsOnline(true)
    const handleOffline = () => setIsOnline(false)

    window.addEventListener("online", handleOnline)
    window.addEventListener("offline", handleOffline)

    return () => {
      window.removeEventListener("online", handleOnline)
      window.removeEventListener("offline", handleOffline)
    }
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading || !isOnline) return

    const userMessage = {
      id: "user-" + Date.now(),
      text: inputMessage,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputMessage("")
    setIsLoading(true)
    setIsTyping(true)

    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId.current,
        }),
      })

      const data = await response.json()

      if (data.status === "success") {
        setTimeout(
          () => {
            const botMessage = {
              id: "bot-" + Date.now(),
              text: data.response,
              sender: "bot",
              timestamp: new Date(),
            }
            setMessages((prev) => [...prev, botMessage])
            setIsTyping(false)
          },
          Math.random() * 1000 + 500,
        ) // Random delay for more natural feel
      } else {
        throw new Error(data.error || "Failed to get response")
      }
    } catch (error) {
      console.error("Error:", error)
      const errorMessage = {
        id: "error-" + Date.now(),
        text: "I apologize, but I'm experiencing some technical difficulties. Please check your connection and try again. 🔧",
        sender: "bot",
        timestamp: new Date(),
        isError: true,
      }
      setMessages((prev) => [...prev, errorMessage])
      setIsTyping(false)
    } finally {
      setIsLoading(false)
    }
  }

  const clearChat = async () => {
    try {
      await fetch(`http://localhost:5000/api/clear/${sessionId.current}`, {
        method: "DELETE",
      })
      setMessages([
        {
          id: "welcome-" + Date.now(),
          text: "Chat cleared! How can I help you today? 😊",
          sender: "bot",
          timestamp: new Date(),
        },
      ])
    } catch (error) {
      console.error("Error clearing chat:", error)
    }
  }

  const exportChat = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/export/${sessionId.current}`)
      const data = await response.json()

      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `chat-export-${new Date().toISOString().split("T")[0]}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error("Error exporting chat:", error)
    }
  }

  const getStats = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/stats/${sessionId.current}`)
      const data = await response.json()
      setStats(data)
      setShowStats(true)
    } catch (error) {
      console.error("Error getting stats:", error)
    }
  }

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage(e)
    }
  }

  return (
    <div className={`chat-app ${darkMode ? "dark-mode" : ""} font-${fontSize}`}>
      {/* Header */}
      <header className="chat-header">
        <div className="header-left">
          <div className="bot-avatar">
            <div className="avatar-circle">
              <span className="bot-icon">🤖</span>
            </div>
            <div className={`status-dot ${isOnline ? "online" : "offline"}`}></div>
          </div>
          <div className="header-info">
            <h1>AI Assistant</h1>
            <p className="status-text">{isOnline ? (isTyping ? "Typing..." : "Online") : "Offline"}</p>
          </div>
        </div>

        <div className="header-actions">
          <button className="action-btn" onClick={getStats} title="View Statistics">
            📊
          </button>
          <button className="action-btn" onClick={exportChat} title="Export Chat">
            📥
          </button>
          <button className="action-btn" onClick={clearChat} title="Clear Chat">
            🗑️
          </button>
          <button className="action-btn" onClick={() => setShowSettings(!showSettings)} title="Settings">
            ⚙️
          </button>
        </div>
      </header>

      {/* Settings Panel */}
      {showSettings && (
        <div className="settings-panel">
          <div className="settings-content">
            <h3>Settings</h3>
            <div className="setting-item">
              <label>
                <input type="checkbox" checked={darkMode} onChange={(e) => setDarkMode(e.target.checked)} />
                Dark Mode
              </label>
            </div>
            <div className="setting-item">
              <label>Font Size:</label>
              <select value={fontSize} onChange={(e) => setFontSize(e.target.value)}>
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Stats Modal */}
      {showStats && stats && (
        <div className="modal-overlay" onClick={() => setShowStats(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Chat Statistics</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Total Messages:</span>
                <span className="stat-value">{stats.total_messages}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Your Messages:</span>
                <span className="stat-value">{stats.user_messages}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">AI Responses:</span>
                <span className="stat-value">{stats.bot_messages}</span>
              </div>
            </div>
            <button className="close-btn" onClick={() => setShowStats(false)}>
              Close
            </button>
          </div>
        </div>
      )}

      {/* Messages Container */}
      <main className="messages-container">
        <div className="messages-wrapper">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === "user" ? "user-message" : "bot-message"} ${message.isError ? "error-message" : ""}`}
            >
              <div className="message-content">
                <div className="message-bubble">
                  <div className="message-text">{message.text}</div>
                </div>
                <div className="message-meta">
                  <span className="message-time">{formatTime(message.timestamp)}</span>
                  {message.sender === "user" && <span className="message-status">✓</span>}
                </div>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="message bot-message">
              <div className="message-content">
                <div className="message-bubble typing-bubble">
                  <div className="typing-indicator">
                    <div className="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="input-area">
        <form onSubmit={sendMessage} className="input-form">
          <div className="input-container">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isOnline ? "Type your message..." : "You're offline. Check your connection."}
              disabled={isLoading || !isOnline}
              className="message-input"
              rows="1"
            />
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim() || !isOnline}
              className="send-button"
              title="Send message"
            >
              {isLoading ? <div className="loading-spinner"></div> : <span className="send-icon">➤</span>}
            </button>
          </div>
        </form>

        {!isOnline && (
          <div className="offline-indicator">
            <span>🔴 You're offline. Please check your internet connection.</span>
          </div>
        )}
      </footer>
    </div>
  )
}
