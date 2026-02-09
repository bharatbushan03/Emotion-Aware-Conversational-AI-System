import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState<{ role: string, content: string }[]>([])
  const [input, setInput] = useState('')
  const [emotion, setEmotion] = useState<string>('Waiting...')
  const [confidence, setConfidence] = useState<number | null>(null)
  const [explanation, setExplanation] = useState<any>(null)

  const sendMessage = async () => {
    if (!input.trim()) return

    // Add user message
    const newMessages = [...messages, { role: 'user', content: input }]
    setMessages(newMessages)
    setInput('')

    // API call
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      const response = await fetch(`${apiUrl}/api/chat`, {
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
      setExplanation(data.explanation)
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
            <span className={confidence && confidence > 0.8 ? 'high-conf' : 'low-conf'}>
              {confidence !== null ? (confidence * 100).toFixed(1) + '%' : '-'}
            </span>
          </div>

          {explanation && (
            <div className="explanation-section">
              <h3>🧠 Explainability</h3>

              <div className="exp-item">
                <label>Reasoning Trace:</label>
                <p>{explanation.reasoning || "Analyzing..."}</p>
              </div>

              {explanation.is_sarcastic && (
                <div className="exp-item sarcasm-alert">
                  ⚠️ Sarcasm Detected
                </div>
              )}

              <div className="exp-item">
                <label>Key Tokens:</label>
                <div className="tags">
                  {explanation.key_tokens && explanation.key_tokens.map((token: string, i: number) => (
                    <span key={i} className="token-tag">{token}</span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </aside>
      </main>
    </div>
  )
}

export default App
