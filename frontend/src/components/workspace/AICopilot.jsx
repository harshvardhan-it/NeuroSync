import {
  useState,
  useRef,
  useEffect,
} from "react";

import ReactMarkdown from "react-markdown";

import {
  chatWithAI,
} from "../../api/client";

export default function AICopilot({
  datasetMeta,
}) {
  const meta =
    datasetMeta || {};

  const datasetId = Number(
    localStorage.getItem(
      "dataset_id"
    )
  );

  const [messages, setMessages] =
    useState([]);

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const messagesEndRef =
    useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  useEffect(() => {
    if (!datasetId) return;

    localStorage.setItem(
      `chat_${datasetId}`,
      JSON.stringify(messages)
    );
  }, [messages, datasetId]);

  useEffect(() => {
    if (!datasetId) return;

    const savedChat =
      localStorage.getItem(
        `chat_${datasetId}`
      );

    if (savedChat) {
      try {
        setMessages(
          JSON.parse(savedChat)
        );
      } catch (error) {
        console.error(
          "Failed to restore chat",
          error
        );
      }
    } else {
      setMessages([]);
    }
  }, [datasetId]);

  async function sendMessage(
    predefinedQuestion = null
  ) {
    const question =
      predefinedQuestion || input;

    if (!question.trim()) {
      return;
    }

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const res =
        await chatWithAI(
          question,
          datasetId
        );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            res.data.data,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠️ AI service unavailable.",
        },
      ]);
    }

    setLoading(false);
  }

  function clearConversation() {
    setMessages([]);

    localStorage.removeItem(
      `chat_${datasetId}`
    );
  }

  const prompts = [
    "Why is risk high?",
    "Summarize my dataset",
    "Suggest cost optimizations",
    "What are anomalies?",
  ];

  return (
    <div
      className="
        rounded-[28px]
        p-6
        min-h-[650px]
        max-h-[85vh]
        flex
        flex-col
      "
      style={{
        background:
          "rgba(255,255,255,0.03)",

        border:
          "1px solid rgba(255,255,255,0.08)",

        backdropFilter:
          "blur(24px)",
      }}
    >
      {/* Header */}

      <div
        className="
          mb-4
          flex
          items-center
          justify-between
        "
      >
        <h2
          className="
            text-2xl
            font-display
            font-bold
          "
        >
          🤖 NeuroSync AI Copilot
        </h2>

        {messages.length > 0 && (
          <button
            onClick={
              clearConversation
            }
            className="
              px-3
              py-2
              rounded-xl
              text-sm
              hover:scale-105
              transition-all
            "
            style={{
              background:
                "rgba(255,255,255,0.05)",

              border:
                "1px solid rgba(255,255,255,0.08)",

              color:
                "var(--text-secondary)",
            }}
          >
            🗑 Clear Chat
          </button>
        )}
      </div>

      {/* Dataset Context */}

      <div
        className="
          mb-4
          px-4
          py-3
          rounded-2xl
          flex
          flex-wrap
          items-center
          gap-4
        "
        style={{
          background:
            "rgba(255,255,255,0.03)",

          border:
            "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <div
          className="
            font-medium
            truncate
          "
        >
          📁 {meta.name}
        </div>

        <div
          className="text-sm"
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          📊 {meta.rows} Rows
        </div>

        <div
          className="text-sm"
          style={{
            color:
              "var(--text-secondary)",
          }}
        >
          📈 {meta.columns} Columns
        </div>
      </div>

      {/* Suggested Prompts */}

      {messages.length === 0 && (
        <div
          className="
            flex
            flex-wrap
            gap-2
            mb-5
          "
        >
          {prompts.map(
            (prompt) => (
              <button
                key={prompt}
                onClick={() =>
                  sendMessage(
                    prompt
                  )
                }
                className="
                  px-3
                  py-2
                  rounded-full
                  text-sm
                  hover:scale-105
                  transition-all
                "
                style={{
                  background:
                    "rgba(255,255,255,0.05)",

                  border:
                    "1px solid rgba(255,255,255,0.08)",
                }}
              >
                {prompt}
              </button>
            )
          )}
        </div>
      )}

      {/* Messages */}

      <div
        className="
          flex-1
          overflow-y-auto
          space-y-5
          pr-2
        "
      >
        {messages.length === 0 && (
          <div
            className="
              flex
              items-center
              justify-center
              h-full
              text-center
            "
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            <div>
              <div className="text-5xl mb-4">
                🤖
              </div>

              <h3 className="text-xl font-semibold mb-2">
                NeuroSync Executive Copilot
              </h3>

              <p>
                Ask questions about
                risks, profitability,
                forecasts, anomalies,
                and strategic
                decisions.
              </p>
            </div>
          </div>
        )}

        {messages.map(
          (
            msg,
            idx
          ) => (
            <div
              key={idx}
              className={
                msg.role ===
                "user"
                  ? "max-w-[60%] ml-auto"
                  : "max-w-[65%]"
              }
            >
              <div
                className="
                  mb-2
                  text-xs
                  opacity-60
                "
              >
                {msg.role ===
                "user"
                  ? "🧑 You"
                  : "🤖 NeuroSync AI"}
              </div>

              <div
                className={`
                  p-4
                  shadow-lg
                  ${
                    msg.role ===
                    "user"
                      ? "rounded-3xl rounded-br-lg"
                      : "rounded-3xl rounded-bl-lg"
                  }
                `}
                style={{
                  background:
                    msg.role ===
                    "user"
                      ? "linear-gradient(135deg,#E7B75F,#B3264A)"
                      : "rgba(255,255,255,0.05)",

                  color:
                    msg.role ===
                    "user"
                      ? "#000"
                      : "#fff",

                  border:
                    "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <ReactMarkdown>
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
          )
        )}

        {loading && (
          <div
            className="
              animate-pulse
              text-sm
            "
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            🤖 NeuroSync AI is analyzing your business...
          </div>
        )}

        <div
          ref={
            messagesEndRef
          }
        />
      </div>

      {/* Input */}

      <div
        className="
          mt-4
          flex
          gap-3
        "
      >
        <input
          value={input}
          onChange={(e) =>
            setInput(
              e.target.value
            )
          }
          onKeyDown={(e) => {
            if (
              e.key ===
              "Enter"
            ) {
              sendMessage();
            }
          }}
          placeholder="Ask about your dataset..."
          className="
            flex-1
            px-4
            py-4
            rounded-2xl
            outline-none
          "
          style={{
            background:
              "rgba(255,255,255,0.03)",

            border:
              "1px solid rgba(255,255,255,0.08)",

            color:
              "#fff",
          }}
        />

        <button
          onClick={() =>
            sendMessage()
          }
          className="
            px-6
            rounded-2xl
            font-semibold
            hover:scale-105
            transition-all
          "
          style={{
            background:
              "linear-gradient(135deg,#E7B75F,#B3264A)",

            color:
              "#000",
          }}
        >
          Ask AI →
        </button>
      </div>
    </div>
  );
}