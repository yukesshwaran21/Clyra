# Green Themed AI Chatbot

A beautiful chatbot application with a green theme, smooth animations, and AI-powered responses.

## Features

- 🤖 AI-powered responses using OpenAI GPT
- 🎨 Beautiful green-themed UI with smooth animations
- 💬 Real-time chat interface
- 📱 Responsive design for mobile and desktop
- ⚡ Fast and lightweight
- 🔄 Typing indicators and loading states

## Setup Instructions

### Backend (Python Flask)

1. Install Python dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Set up environment variables:
\`\`\`bash
cp .env.example .env
# Edit .env and add your OpenAI API key
\`\`\`

3. Run the Flask server:
\`\`\`bash
python scripts/app.py
\`\`\`

The backend will run on `http://localhost:5000`

### Frontend (React/Next.js)

1. Install Node.js dependencies:
\`\`\`bash
npm install
\`\`\`

2. Run the development server:
\`\`\`bash
npm run dev
\`\`\`

The frontend will run on `http://localhost:3000`

## Usage

1. Start both the Python backend and React frontend
2. Open your browser to `http://localhost:3000`
3. Start chatting with the AI assistant!

## Customization

- Modify the green theme colors in `app/globals.css`
- Adjust AI behavior in `scripts/app.py`
- Add new animations or UI components as needed

## Technologies Used

- **Backend**: Python, Flask, OpenAI API
- **Frontend**: React, Next.js, JavaScript
- **Styling**: CSS3 with animations and gradients
- **AI**: OpenAI GPT-3.5-turbo
