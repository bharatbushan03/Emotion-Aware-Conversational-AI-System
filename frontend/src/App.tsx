import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState<{ role: string, content: string }[]>([])
  const [input, setInput] = useState('')
  const [emotion, setEmotion] = useState<string>('Waiting...')
  const [confidence, setConfidence] = useState<number | null>(null)

  const sendMessage = async () => {
    if (!input.trim()) return

    // Add user message
    const newMessages = [...messages, { role: 'user', content: input }]
    setMessages(newMessages)
    setInput('')

    // API call
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          user_id: "test_user" // Fixed user for now
        })
      })
      const data = await response.json()

      setMessages(prev => [...prev, { role: 'ai', content: data.response }])
      setEmotion(data.emotion)
      setConfidence(data.confidence)
    } catch (error) {
      console.error("Error:", error)
      setMessages(prev => [...prev, { role: 'ai', content: "Error connecting to server." }])
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Emotion-Aware AI</h1>
      </header>

      <main className="main-content">
        <div className="chat-container">
          <div className="messages">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                {m.content}
              </div>
            ))}
          </div>
          <div className="input-area">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Type a message..."
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>

        <aside className="dashboard-panel">
          <h2>Real-time Analysis</h2>
          <div className="metric">
            <label>Detected Emotion:</label>
            <span>{emotion}</span>
          </div>
          <div className="metric">
            <label>Confidence:</label>
            <span>{confidence !== null ? (confidence * 100).toFixed(1) + '%' : '-'}</span>
          </div>
        </aside>
      </main>
    </div>
  )
}

export default App
