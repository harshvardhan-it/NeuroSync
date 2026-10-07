from collections import defaultdict
from threading import Lock


class ConversationContext:
    """Short-lived, user-scoped chat context.

    This is intentionally bounded runtime memory. Persistent chat history should
    eventually live in PostgreSQL; user_id is included now so contexts cannot
    cross tenant boundaries.
    """

    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.sessions = defaultdict(list)
        self.lock = Lock()

    def add_message(self, user_id: int, dataset_id: int, role: str, content: str):
        key = (user_id, dataset_id)
        with self.lock:
            self.sessions[key].append({"role": role, "content": content})
            self.sessions[key] = self.sessions[key][-self.max_messages :]

    def get_history(self, user_id: int, dataset_id: int):
        with self.lock:
            return list(self.sessions.get((user_id, dataset_id), []))

    def clear_history(self, user_id: int, dataset_id: int):
        with self.lock:
            self.sessions.pop((user_id, dataset_id), None)

    def build_context(self, user_id: int, dataset_id: int) -> str:
        history = self.get_history(user_id, dataset_id)
        if not history:
            return ""

        lines = ["\nPREVIOUS DISCUSSION\n"]
        for msg in history:
            role = "User" if msg["role"] == "user" else "AI"
            lines.append(f"{role}: {msg['content']}\n")
        return "\n".join(lines)


conversation_manager = ConversationContext()
