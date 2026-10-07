import { useState, useRef, useEffect } from "react";
import { chatWithAI } from "../../api/client";

export default function AICopilot({ datasetMeta }) {
  const meta = datasetMeta || {};
  const datasetId = Number(localStorage.getItem("dataset_id"));

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (!datasetId) return;
    const saved = localStorage.getItem(`chat_${datasetId}`);
    setMessages(saved ? JSON.parse(saved) : []);
  }, [datasetId]);

  useEffect(() => {
    if (!datasetId) return;
    localStorage.setItem(`chat_${datasetId}`, JSON.stringify(messages.slice(-10)));
  }, [messages, datasetId]);

  async function sendMessage(predefinedQuestion = null) {
    const question = (predefinedQuestion || input).trim();
    if (!question || !datasetId || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const res = await chatWithAI(question, datasetId);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.data.data },
      ]);
    } catch (error) {
      const status = error?.response?.status;
      const message =
        status === 401
          ? "Your session has expired. Please log in again."
          : status === 403
            ? "You are not authorized to access this dataset."
            : status === 404
              ? "Dataset not found."
              : "Executive AI is temporarily unavailable. Please try again.";
      setMessages((prev) => [...prev, { role: "assistant", content: message }]);
    } finally {
      setLoading(false);
    }
  }

  function clearConversation() {
    setMessages([]);
    if (datasetId) localStorage.removeItem(`chat_${datasetId}`);
  }

  const executiveActions = [
    ["Business Diagnosis", "🩺", "Provide a complete business diagnosis. Identify key problems, risks, strengths, and business health."],
    ["Risk Review", "⚠️", "Review business risks, explain severity, impact, and mitigation strategies."],
    ["Growth Opportunities", "📈", "Identify growth opportunities supported by the analyzed dataset."],
    ["Cost Optimization", "💰", "Analyze expenses and recommend evidence-based cost optimization opportunities."],
    ["Executive Summary", "📋", "Generate a CFO-style executive summary using the analyzed dataset."],
  ];

  return (
    <div
      className="rounded-[28px] p-6 min-h-[650px] max-h-[85vh] flex flex-col"
      style={{
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.08)",
        backdropFilter: "blur(24px)",
      }}
    >
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-display font-bold">🧠 Executive AI Consultant</h2>
          <p className="text-sm mt-1" style={{ color: "var(--text-secondary)" }}>
            CFO-style business intelligence powered by Groq
          </p>
        </div>
        {messages.length > 0 && (
          <button
            onClick={clearConversation}
            className="px-3 py-2 rounded-xl text-sm"
            style={{
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.08)",
              color: "var(--text-secondary)",
            }}
          >
            Clear Chat
          </button>
        )}
      </div>

      <div
        className="mb-4 px-4 py-3 rounded-2xl flex flex-wrap items-center gap-4"
        style={{
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <div className="font-medium truncate">📁 {meta.name || "No dataset selected"}</div>
        <div className="text-sm" style={{ color: "var(--text-secondary)" }}>📊 {meta.rows || 0} Rows</div>
        <div className="text-sm" style={{ color: "var(--text-secondary)" }}>📈 {meta.columns || 0} Columns</div>
      </div>

      {messages.length === 0 && (
        <div className="mb-6">
          <div className="text-sm uppercase tracking-wider mb-3 opacity-70">Executive Quick Actions</div>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            {executiveActions.map(([title, icon, prompt]) => (
              <button
                key={title}
                onClick={() => sendMessage(prompt)}
                className="p-4 rounded-2xl text-left hover:scale-[1.02] transition-all"
                style={{
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <div className="text-3xl mb-3">{icon}</div>
                <div className="font-semibold text-base">{title}</div>
                <div className="text-sm mt-2" style={{ color: "var(--text-secondary)" }}>
                  Launch executive analysis
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-5 pr-2">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-center" style={{ color: "var(--text-secondary)" }}>
            <div>
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-2xl font-semibold mb-2">NeuroSync Executive Consultant</h3>
              <p className="max-w-xl">
                Analyze business performance, diagnose operational risks, discover growth opportunities,
                optimize costs, and generate CFO-style strategic recommendations.
              </p>
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={msg.role === "user" ? "max-w-[60%] ml-auto" : "max-w-[65%]"}>
            <div className="mb-2 text-xs opacity-60">
              {msg.role === "user" ? "🧑 You" : "🤖 NeuroSync AI"}
            </div>
            <div
              className={`p-4 shadow-lg ${msg.role === "user" ? "rounded-3xl rounded-br-lg" : "rounded-3xl rounded-bl-lg"}`}
              style={{
                background:
                  msg.role === "user"
                    ? "linear-gradient(135deg,#E7B75F,#B3264A)"
                    : "rgba(255,255,255,0.05)",
                color: msg.role === "user" ? "#000" : "#fff",
                border: "1px solid rgba(255,255,255,0.08)",
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="animate-pulse text-sm" style={{ color: "var(--text-secondary)" }}>
            🤖 NeuroSync AI is analyzing your business...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="mt-4 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder={datasetId ? "Ask a strategic business question..." : "Upload a dataset first"}
          disabled={!datasetId || loading}
          className="flex-1 px-4 py-4 rounded-2xl outline-none"
          style={{
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.08)",
            color: "#fff",
          }}
        />
        <button
          onClick={() => sendMessage()}
          disabled={!datasetId || loading}
          className="px-6 rounded-2xl font-semibold hover:scale-105 transition-all disabled:opacity-50"
          style={{
            background: "linear-gradient(135deg,#E7B75F,#B3264A)",
            color: "#000",
          }}
        >
          Ask AI →
        </button>
      </div>
    </div>
  );
}
