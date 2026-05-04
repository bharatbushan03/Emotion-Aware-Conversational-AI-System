import { useState } from 'react'
import type { KeyboardEvent } from 'react'
import './App.css'

type ChatMessage = {
  role: 'user' | 'ai'
  content: string
}

type ChatApiResponse = {
  response: string
  emotion: string
  confidence: number
  explanation: {
    tone: string
    reasoning: string
    key_tokens: string[]
    all_scores: Record<string, number>
    is_sarcastic: boolean
  }
}

const SAMPLE_PROMPTS = [
  'I am feeling overwhelmed by work today.',
  'I just got some great news and I cannot stop smiling.',
  'I am nervous about an important presentation tomorrow.',
]

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'ai',
      content: 'Hello. Share how you are feeling, and I will adapt my response to your emotional state.',
    },
  ])
  const [input, setInput] = useState('')
  const [emotion, setEmotion] = useState<string>('Waiting...')
  const [confidence, setConfidence] = useState<number | null>(null)
  const [explanation, setExplanation] = useState<ChatApiResponse['explanation'] | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const submitMessage = async (messageText: string) => {
    const trimmed = messageText.trim()
    if (!trimmed || loading) return

    setMessages((prev) => [...prev, { role: 'user', content: trimmed }])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: trimmed,
          user_id: 'test_user',
        }),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data: ChatApiResponse = await response.json()

      setMessages((prev) => [...prev, { role: 'ai', content: data.response }])
      setEmotion(data.emotion)
      setConfidence(data.confidence)
      setExplanation(data.explanation)
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : 'Unknown network error'
      setError(message)
      setMessages((prev) => [
        ...prev,
        { role: 'ai', content: 'Error connecting to the backend. Please check that the API is running.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async () => {
    await submitMessage(input)
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      void sendMessage()
    }
  }

  const handleClearChat = () => {
    setMessages([
      {
        role: 'ai',
        content: 'Conversation cleared. Send another message to continue the emotional analysis.',
      },
    ])
    setEmotion('Waiting...')
    setConfidence(null)
    setExplanation(null)
    setError(null)
    setLoading(false)
  }

  const confidenceLabel = confidence !== null ? `${(confidence * 100).toFixed(1)}%` : '—'

  return (
    <div className="app-shell">
      <div className="background-orb background-orb-left" />
      <div className="background-orb background-orb-right" />

      <header className="app-header">
        <div>
          <p className="eyebrow">Emotion-Aware Conversational AI</p>
          <h1>Adaptive replies with emotional context</h1>
        </div>
        <div className="header-actions">
          <button className="ghost-button" onClick={handleClearChat} type="button">
            Clear chat
          </button>
        </div>
      </header>

      <main className="main-grid">
        <section className="chat-card">
          <div className="chat-card-header">
            <div>
              <p className="section-label">Conversation</p>
              <h2>Talk naturally and see how the system responds</h2>
            </div>
            <div className="status-pill">API {apiUrl}</div>
          </div>

          <div className="quick-prompts">
            {SAMPLE_PROMPTS.map((prompt) => (
              <button
                key={prompt}
                className="prompt-chip"
                onClick={() => setInput(prompt)}
                type="button"
              >
                {prompt}
              </button>
            ))}
          </div>

          <div className="messages">
            {messages.map((message, index) => (
              <article key={`${message.role}-${index}`} className={`message-bubble ${message.role}`}>
                <span className="message-role">{message.role === 'user' ? 'You' : 'AI'}</span>
                <p>{message.content}</p>
              </article>
            ))}
            {loading && <div className="typing-indicator">Analyzing emotion and preparing a response...</div>}
          </div>

          <div className="composer">
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Share how you are feeling, or press a sample prompt above..."
              rows={3}
            />
            <div className="composer-footer">
              <p className="hint-text">Press Enter to send, Shift+Enter for a new line.</p>
              <button onClick={sendMessage} disabled={loading || !input.trim()} type="button">
                {loading ? 'Sending...' : 'Send message'}
              </button>
            </div>
            {error && <p className="error-banner">{error}</p>}
          </div>
        </section>

        <aside className="dashboard-card">
          <div className="panel-heading">
            <div>
              <p className="section-label">Analysis</p>
              <h2>Real-time emotional snapshot</h2>
            </div>
          </div>

          <div className="metric-grid">
            <div className="metric">
              <label>Detected emotion</label>
              <span>{emotion}</span>
            </div>
            <div className="metric">
              <label>Confidence</label>
              <span className={confidence !== null && confidence > 0.8 ? 'high-conf' : 'low-conf'}>
                {confidenceLabel}
              </span>
            </div>
          </div>

          {explanation ? (
            <div className="explanation-section">
              <div className="exp-item">
                <label>Tone strategy</label>
                <p>{explanation.tone}</p>
              </div>

              <div className="exp-item">
                <label>Reasoning trace</label>
                <p>{explanation.reasoning || 'Analyzing...'}</p>
              </div>

              {explanation.is_sarcastic && <div className="sarcasm-alert">Sarcasm detected</div>}

              <div className="exp-item">
                <label>Key tokens</label>
                <div className="tags">
                  {explanation.key_tokens.length > 0 ? (
                    explanation.key_tokens.map((token) => (
                      <span key={token} className="token-tag">
                        {token}
                      </span>
                    ))
                  ) : (
                    <span className="empty-state">No highlighted tokens yet.</span>
                  )}
                </div>
              </div>

              <div className="exp-item">
                <label>Model scores</label>
                <div className="score-list">
                  {Object.entries(explanation.all_scores)
                    .sort((left, right) => right[1] - left[1])
                    .slice(0, 5)
                    .map(([label, score]) => (
                      <div key={label} className="score-row">
                        <span>{label}</span>
                        <strong>{(score * 100).toFixed(1)}%</strong>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-card">
              <p>Send a message to populate the emotion dashboard, explanation trace, and response strategy.</p>
            </div>
          )}
        </aside>
      </main>
    </div>
  )
}

export default App
