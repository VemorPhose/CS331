import { useState, useEffect, useRef } from "react";
import "./App.css";
// import { sendChatMessage } from "./api/chatApi";

function App() {
  const [messages, setMessages] = useState([]); // { role: 'user'|'assistant', text }
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesRef = useRef(null);
  const isAtBottomRef = useRef(true);
  const [showScrollDown, setShowScrollDown] = useState(false);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg = { role: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // placeholder for actual API call
      await new Promise((r) => setTimeout(r, 500)); // small delay
      const reply = `Fake bot reply to: "${text}" (backend not connected yet)`;
      const botMsg = { role: "assistant", text: reply };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-scroll 
  useEffect(() => {
    const el = messagesRef.current;
    if (!el) return;

    if (isAtBottomRef.current) {
      el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
    }
  }, [messages]);

  const handleMessagesScroll = () => {
    const el = messagesRef.current;
    if (!el) return;

    const atBottom =
      el.scrollHeight - el.scrollTop - el.clientHeight < 60;

    isAtBottomRef.current = atBottom;
    setShowScrollDown(!atBottom);
  };

  const scrollToBottom = () => {
    const el = messagesRef.current;
    if (!el) return;

    isAtBottomRef.current = true;
    setShowScrollDown(false);
    el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  };

  return (
    <div className="app">
      <main className="chat-container">
        <header className="app-header engine-card">
          <h1>Nexus Chatbot</h1>
          <p>Ask about time, system metrics, or anything else.</p>
          <p className="app-subtitle">
            Powered by a local parsing engine with tools for time and system
            metrics.
          </p>
        </header>

        <div
          className="messages"
          ref={messagesRef}
          onScroll={handleMessagesScroll}
        >
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`message ${m.role === "user" ? "user" : "assistant"}`}
            >
              <div className="bubble">{m.text}</div>
            </div>
          ))}
          {loading && <div className="status">Thinking…</div>}
        </div>

        {showScrollDown && (
          <button className="scroll-down-btn" onClick={scrollToBottom}>
            ↓ Scroll to latest
          </button>
        )}

        <div className="input-row">
          <input
            className="input"
            placeholder="Type your query..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button className="send-btn" onClick={handleSend} disabled={loading}>
            Send
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;