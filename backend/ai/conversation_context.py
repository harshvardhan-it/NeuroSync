from collections import defaultdict


class ConversationContext:

    def __init__(self):
        self.sessions = defaultdict(list)

    def add_message(
        self,
        dataset_id: int,
        role: str,
        content: str
    ):
        self.sessions[
            dataset_id
        ].append(
            {
                "role": role,
                "content": content
            }
        )

        # Keep last 10 messages
        self.sessions[
            dataset_id
        ] = self.sessions[
            dataset_id
        ][-10:]

    def get_history(
        self,
        dataset_id: int
    ):
        return self.sessions.get(
            dataset_id,
            []
        )

    def clear_history(
        self,
        dataset_id: int
    ):
        if dataset_id in self.sessions:
            del self.sessions[
                dataset_id
            ]

    def build_context(
        self,
        dataset_id: int
    ) -> str:

        history = self.get_history(
            dataset_id
        )

        if not history:
            return ""

        context = (
            "\nPREVIOUS DISCUSSION\n\n"
        )

        for msg in history:

            role = (
                "User"
                if msg["role"]
                == "user"
                else "AI"
            )

            context += (
                f"{role}: "
                f"{msg['content']}\n\n"
            )

        return context


conversation_manager = (
    ConversationContext()
)