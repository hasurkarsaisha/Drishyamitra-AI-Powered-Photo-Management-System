import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import api from '../api/axios'

function Chat() {
  const navigate = useNavigate()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [photoUrls, setPhotoUrls] = useState({})
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetchHistory()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const fetchHistory = async () => {
    try {
      const response = await api.get('/chat/history')
      const history = response.data.history || []
      const formattedMessages = history.flatMap(h => {
        const parsedResponse = parseResponse(h.response)
        return [
          { role: 'user', content: h.message },
          { role: 'assistant', content: h.response, parsed: parsedResponse }
        ]
      })
      setMessages(formattedMessages)
    } catch (err) {
      console.error('Failed to fetch chat history:', err)
    }
  }

  const parseResponse = (response) => {
    try {
      // Check if response is already an object
      if (typeof response === 'object' && response.success && response.photos) {
        return response
      }
      
      // Try to parse as JSON string
      if (typeof response === 'string') {
        const parsed = JSON.parse(response)
        if (parsed.success && parsed.photos) {
          return parsed
        }
      }
    } catch (e) {
      // Not JSON, return as text
      console.log('Failed to parse response:', e)
    }
    return null
  }

  const fetchPhotoBlob = async (photoId) => {
    if (photoUrls[photoId]) return
    
    try {
      const response = await api.get(`/photos/${photoId}`, {
        responseType: 'blob'
      })
      const url = URL.createObjectURL(response.data)
      setPhotoUrls(prev => {
        const updated = { ...prev, [photoId]: url }
        return updated
      })
    } catch (err) {
      console.error(`Failed to fetch photo ${photoId}:`, err)
    }
  }

  // Watch for new messages with photos and fetch them
  useEffect(() => {
    const photoIds = new Set()
    
    messages.forEach(msg => {
      if (msg.parsed?.photos) {
        msg.parsed.photos.forEach(photo => {
          if (!photoUrls[photo.id] && !photoIds.has(photo.id)) {
            photoIds.add(photo.id)
            fetchPhotoBlob(photo.id)
          }
        })
      }
    })
  }, [messages.length]) // Only trigger when messages array length changes

  const handleClearChat = async () => {
    if (!confirm('Are you sure you want to clear all chat history?')) return
    
    try {
      await api.delete('/chat/history')
      setMessages([])
      setPhotoUrls({})
    } catch (err) {
      console.error('Failed to clear chat history:', err)
      alert('Failed to clear chat history. Please try again.')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await api.post('/chat/query', { message: userMessage })
      
      // The response.data IS the result object from backend
      const result = response.data
      const parsedResponse = parseResponse(result)
      
      const newMessage = { 
        role: 'assistant', 
        content: result.message || JSON.stringify(result),
        parsed: parsedResponse
      }
      
      setMessages(prev => [...prev, newMessage])
    } catch (err) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="h-[calc(100vh-4rem)] flex flex-col">
        {/* Header */}
        <div className="indian-card p-6 mb-4 bg-gradient-to-r from-orange-50 to-yellow-50">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <svg className="w-10 h-10 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <h1 className="text-4xl font-bold text-maroon">AI Assistant</h1>
              </div>
              <p className="text-gray-600 font-medium">
                Ask me anything about your photos
              </p>
            </div>
            {messages.length > 0 && (
              <button
                onClick={handleClearChat}
                className="px-4 py-2 rounded-xl border-2 border-red-300 bg-white text-red-600 font-semibold hover:bg-red-50 transition-all flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>Clear Chat</span>
              </button>
            )}
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 indian-card p-6 overflow-y-auto mb-4 scroll-smooth" style={{ maxHeight: 'calc(100vh - 20rem)', scrollBehavior: 'smooth' }}>
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <svg className="w-24 h-24 mx-auto mb-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <h2 className="text-3xl font-bold text-maroon mb-3">Start a Conversation</h2>
                <p className="text-gray-600 font-medium mb-4">
                  Try asking:
                </p>
                <div className="space-y-2 text-left max-w-md mx-auto">
                  <div className="p-3 rounded-xl bg-orange-50 border-2 border-orange-200">
                    <span className="text-gray-700 font-medium">"Show me photos of [person name]"</span>
                  </div>
                  <div className="p-3 rounded-xl bg-yellow-50 border-2 border-yellow-200">
                    <span className="text-gray-700 font-medium">"Find photos from last month"</span>
                  </div>
                  <div className="p-3 rounded-xl bg-green-50 border-2 border-green-200">
                    <span className="text-gray-700 font-medium">"How many people are in my gallery?"</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[70%] p-4 rounded-2xl ${
                      msg.role === 'user'
                        ? 'bg-gradient-to-r from-orange-400 to-yellow-400 text-white'
                        : 'bg-white border-2 border-orange-200 text-gray-800'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      {msg.role === 'user' ? (
                        <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="w-5 h-5 flex-shrink-0 mt-0.5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      )}
                      <div className="flex-1">
                        {msg.parsed?.photos ? (
                          <div>
                            <p className="font-semibold mb-2 text-maroon">
                              {msg.parsed.message || `Found ${msg.parsed.count} photo${msg.parsed.count !== 1 ? 's' : ''}`}
                            </p>
                            <div className="grid grid-cols-3 gap-2 max-w-sm">
                              {msg.parsed.photos.slice(0, 6).map((photo) => (
                                <div
                                  key={photo.id}
                                  onClick={() => navigate(`/photo/${photo.id}`)}
                                  className="relative aspect-square rounded-lg overflow-hidden border-2 border-orange-300 cursor-pointer hover:border-orange-500 transition-all hover:scale-105 group"
                                >
                                  {photoUrls[photo.id] ? (
                                    <img
                                      src={photoUrls[photo.id]}
                                      alt={photo.filename}
                                      className="w-full h-full object-cover"
                                    />
                                  ) : (
                                    <div className="w-full h-full flex items-center justify-center bg-gray-100">
                                      <div className="w-4 h-4 border-2 border-orange-400 border-t-transparent rounded-full animate-spin"></div>
                                    </div>
                                  )}
                                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                                    <div className="absolute bottom-1 left-1 right-1">
                                      <p className="text-white text-[10px] font-semibold truncate">{photo.filename}</p>
                                    </div>
                                  </div>
                                </div>
                              ))}
                            </div>
                            {msg.parsed.photos.length > 6 && (
                              <p className="text-xs text-gray-600 mt-2">
                                +{msg.parsed.photos.length - 6} more photos
                              </p>
                            )}
                          </div>
                        ) : (
                          <p className="font-medium whitespace-pre-wrap">{msg.content}</p>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white border-2 border-orange-200 p-4 rounded-2xl">
                    <div className="flex items-center gap-2">
                      <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="indian-card p-4">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me about your photos..."
              className="indian-input flex-1"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="indian-button px-8 flex items-center gap-2"
            >
              <span>Send</span>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}

export default Chat
