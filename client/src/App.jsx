import { useState, useEffect, useRef } from "react";
import "./App.css";

const AUTH_API_BASE =
  import.meta.env.VITE_AUTH_API_BASE || "http://127.0.0.1:8000";
const CHAT_API_BASE =
  import.meta.env.VITE_CHAT_API_BASE || "http://127.0.0.1:8001";
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "";

function App() {
  const [messages, setMessages] = useState([]); // { role: 'user'|'assistant', text }
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [authToken, setAuthToken] = useState(
    () => localStorage.getItem("nexus_access_token") || ""
  );
  const [userEmail, setUserEmail] = useState(
    () => localStorage.getItem("nexus_user_email") || ""
  );
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");
  const messagesRef = useRef(null);
  const isAtBottomRef = useRef(true);
  const [showScrollDown, setShowScrollDown] = useState(false);
  const googleButtonRef = useRef(null);

  const setSession = (token, email) => {
    setAuthToken(token);
    setUserEmail(email);
    localStorage.setItem("nexus_access_token", token);
    localStorage.setItem("nexus_user_email", email);
  };

  const clearSession = () => {
    setAuthToken("");
    setUserEmail("");
    localStorage.removeItem("nexus_access_token");
    localStorage.removeItem("nexus_user_email");
  };

  const fetchCurrentUser = async (token) => {
    const response = await fetch(`${AUTH_API_BASE}/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch current user");
    }

    const data = await response.json();
    setUserEmail(data.email || "");
    localStorage.setItem("nexus_user_email", data.email || "");
  };

  const loginWithGoogleCredential = async (credential) => {
    setAuthError("");
    setAuthLoading(true);

    try {
      const response = await fetch(`${AUTH_API_BASE}/google-login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ credential }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Google login failed");
      }

      setSession(data.access_token, "");
      await fetchCurrentUser(data.access_token);
    } catch (err) {
      clearSession();
      setAuthError(err?.message || "Google sign-in failed");
    } finally {
      setAuthLoading(false);
    }
  };

  useEffect(() => {
    if (!authToken || userEmail) return;

    fetchCurrentUser(authToken).catch(() => {
      clearSession();
      setAuthError("Your session expired. Please sign in again.");
    });
  }, [authToken, userEmail]);

  useEffect(() => {
    if (!GOOGLE_CLIENT_ID || authToken) return;

    let isCancelled = false;

    const renderGoogleButton = () => {
      if (isCancelled) return;
      if (!window.google?.accounts?.id || !googleButtonRef.current) return;

      googleButtonRef.current.innerHTML = "";
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: async (response) => {
          if (!response?.credential) {
            setAuthError("Google did not return a valid credential.");
            return;
          }
          await loginWithGoogleCredential(response.credential);
        },
      });

      window.google.accounts.id.renderButton(googleButtonRef.current, {
        type: "standard",
        theme: "filled_blue",
        size: "large",
        text: "signin_with",
        shape: "pill",
        width: 240,
      });
    };

    if (window.google?.accounts?.id) {
      renderGoogleButton();
      return () => {
        isCancelled = true;
      };
    }

    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = renderGoogleButton;
    script.onerror = () => {
      setAuthError("Failed to load Google Identity Services script.");
    };
    document.head.appendChild(script);

    return () => {
      isCancelled = true;
    };
  }, [authToken]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;
    if (!authToken) {
      setAuthError("Please sign in with Google before chatting.");
      return;
    }

    const userMsg = { role: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    setAuthError("");

    try {
      const response = await fetch(`${CHAT_API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Chat request failed");
      }

      const reply = data.reply || "I could not generate a response.";
      const botMsg = { role: "assistant", text: reply };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const botMsg = {
        role: "assistant",
        text: `Error: ${err?.message || "Something went wrong."}`,
      };
      setMessages((prev) => [...prev, botMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    clearSession();
    setAuthError("");
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
          <p>Google-authenticated MVP with temporary Gemini responses.</p>
          <p className="app-subtitle">
            Sign in with Google, then chat using your Gemini API integration.
          </p>

          <div className="auth-panel">
            {authToken ? (
              <div className="auth-row">
                <span className="auth-chip">Signed in: {userEmail || "loading..."}</span>
                <button className="logout-btn" onClick={handleLogout}>
                  Sign out
                </button>
              </div>
            ) : (
              <div className="auth-row">
                <div ref={googleButtonRef} className="google-button-slot" />
                {!GOOGLE_CLIENT_ID && (
                  <div className="auth-hint">
                    Missing VITE_GOOGLE_CLIENT_ID in client/.env.local
                  </div>
                )}
              </div>
            )}

            {authLoading && <div className="status">Signing in...</div>}
            {authError && <div className="auth-error">{authError}</div>}
          </div>
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
            placeholder={
              authToken
                ? "Type your query..."
                : "Sign in with Google to start chatting"
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!authToken || loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading || !authToken}
          >
            Send
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;