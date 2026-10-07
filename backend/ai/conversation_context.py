from collections import defaultdict
from threading import Lock


class ConversationContext:
    """Bounded prototype conversation memory scoped by user and dataset."""

    MAX_MESSAGES = 10
    MAX_MESSAGE_CHARS = 4000
    MAX_SESSIONS = 1000

    def __init__(self):
        self.sessions = defaultdict(list)
        self._lock = Lock()

    def _key(self, user_id: int, dataset_id: int):
        return user_id, dataset_id

    def add_message(self, user_id: int, dataset_id: int, role: str, content: str):
        key = self._key(user_id, dataset_id)
        safe_content = str(content)[: self.MAX_MESSAGE_CHARS]

        with self._lock:
            self.sessions[key].append({"role": role, "content": safe_content})
            self.sessions[key] = self.sessions[key][-self.MAX_MESSAGES :]

            if len(self.sessions) > self.MAX_SESSIONS:
                oldest = next(iter(self.sessions))
                del self.sessions[oldest]

    def get_history(self, user_id: int, dataset_id: int):
        with self._lock:
            return list(self.sessions.get(self._key(user_id, dataset_id), []))

    def clear_history(self, user_id: int, dataset_id: int):
        with self._lock:
            self.sessions.pop(self._key(user_id, dataset_id), None)

    def build_context(self, user_id: int, dataset_id: int) -> str:
        history = self.get_history(user_id, dataset_id)
        if not history:
            return ""

        return "\nPREVIOUS DISCUSSION\n\n" + "".join(
            f"{'User' if item['role'] == 'user' else 'AI'}: {item['content']}\n\n"
            for item in history
        )


conversation_manager = ConversationContext()
