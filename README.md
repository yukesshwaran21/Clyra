# Professional AI Chatbot

A modern, professional AI chatbot application with a clean light theme, smooth animations, and advanced features.

## ✨ Features

### Core Features
- 🤖 **AI-Powered Responses** - OpenAI GPT integration
- 💬 **Real-time Chat** - Instant message delivery
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Professional UI** - Clean, modern interface

### Advanced Features
- 🌙 **Dark/Light Mode** - Toggle between themes
- 📊 **Chat Statistics** - View conversation analytics
- 📥 **Export Chat** - Download conversation history
- 🗑️ **Clear Chat** - Reset conversation
- ⚙️ **Settings Panel** - Customize experience
- 🔌 **Offline Detection** - Network status awareness
- 📝 **Multi-line Input** - Support for longer messages
- ⌨️ **Keyboard Shortcuts** - Enter to send, Shift+Enter for new line

### UI Enhancements
- ✨ **Smooth Animations** - Fluid transitions and micro-interactions
- 🎯 **Professional Design** - Clean, structured layout
- 🔤 **Font Size Options** - Adjustable text size
- 📊 **Typing Indicators** - Real-time feedback
- ✅ **Message Status** - Delivery confirmation
- 🎨 **Light Color Scheme** - Easy on the eyes

## 🚀 Setup Instructions

### Backend Setup
1. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Run the Flask server:
   \`\`\`bash
   python scripts/app.py
   \`\`\`

### Frontend Setup
1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Start development server:
   \`\`\`bash
   npm run dev
   \`\`\`

## 🎯 Usage

1. Open http://localhost:3000
2. Start chatting with the AI assistant
3. Use the header buttons for additional features:
   - 📊 View statistics
   - 📥 Export chat
   - 🗑️ Clear conversation
   - ⚙️ Open settings

## 🛠️ API Endpoints

- `POST /api/chat` - Send message to AI
- `GET /api/conversation/<session_id>` - Get chat history
- `DELETE /api/clear/<session_id>` - Clear conversation
- `GET /api/export/<session_id>` - Export chat data
- `GET /api/stats/<session_id>` - Get conversation statistics
- `GET /api/health` - Health check

## 🎨 Customization

The application uses CSS custom properties for easy theming. Modify the variables in `globals.css` to customize colors, spacing, and animations.

## 📱 Responsive Breakpoints

- Desktop: 1024px+
- Tablet: 768px - 1023px
- Mobile: 320px - 767px

## ♿ Accessibility

- Keyboard navigation support
- Screen reader friendly
- High contrast mode support
- Reduced motion support
- Focus indicators

## 🔧 Technologies

- **Frontend**: React, Next.js, CSS3
- **Backend**: Python, Flask
- **AI**: OpenAI GPT-3.5-turbo
- **Features**: Real-time updates, responsive design
