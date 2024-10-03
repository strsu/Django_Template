class SlackBlockManager:

    @classmethod
    def rich_text_section(cls): ...

    @classmethod
    def get_text_element(cls, text, is_bold=False, is_italic=False):
        element = {
            "type": "text",
            "text": text,
            "style": {
                "bold": is_bold,
                "italic": is_italic,
            },
        }
        return element

    @classmethod
    def get_emoji_element(cls, emoji):
        element = {"type": "emoji", "name": emoji}
        return element
