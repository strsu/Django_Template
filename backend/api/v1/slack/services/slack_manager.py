from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackManager:
    def __init__(self, channel, token):
        self.client = WebClient(token=token)
        self.channel = channel

    def post_ephemeral_message(self, user, text=None, blocks=None, thread_ts=None):
        try:
            response = self.client.chat_postEphemeral(
                user=user,
                channel=self.channel,
                text=text,
                blocks=blocks,
                thread_ts=thread_ts,
            )
            return self._handle_response(response)
        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")
            return None

    def post_message(self, text=None, blocks=None, thread_ts=None):
        """Helper method to send a message with text or blocks."""
        try:
            response = self.client.chat_postMessage(
                channel=self.channel, text=text, blocks=blocks, thread_ts=thread_ts
            )
            return self._handle_response(response)
        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")
            return None

    def block_msg(self, blocks, thread_ts=None):
        """
        Sends a message with block elements.
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "A message *with some bold text* and _some italicized text_.",
                },
            }
        ]
        """
        return self.post_message(blocks=blocks, thread_ts=thread_ts)

    def text_msg(self, text, thread_ts=None):
        """Sends a simple text message."""
        return self.post_message(text=text, thread_ts=thread_ts)

    def upload_files(self, byte_stream_list, file_name_list, title_list, comment=""):
        """Uploads multiple files to a Slack channel."""
        try:
            response = self.client.files_upload_v2(
                file_uploads=[
                    {
                        "file": byte_stream,
                        "filename": file_name,
                        "title": title,
                    }
                    for byte_stream, file_name, title in zip(
                        byte_stream_list, file_name_list, title_list
                    )
                ],
                channel=self.channel,
                initial_comment=comment,
            )
            return self._handle_response(response)
        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")
            return None

    def _handle_response(self, response):
        """Handles Slack API responses."""
        if response.get("ok"):
            return response.get("ts")
        return None
