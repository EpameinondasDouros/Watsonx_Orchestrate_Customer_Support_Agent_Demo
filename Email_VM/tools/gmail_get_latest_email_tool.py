import base64
import logging
from typing import Any, Dict, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)


def _extract_plain_text(payload: Optional[Dict[str, Any]]) -> str:
    """Extract the first available text body from a Gmail message payload."""
    if not payload:
        return ""

    body = payload.get("body", {})
    data = body.get("data")
    mime_type = payload.get("mimeType", "")

    if data:
        try:
            decoded = base64.urlsafe_b64decode(data.encode()).decode("utf-8", errors="ignore")
            # Prefer plain text but fall back to HTML if that's all we have
            if mime_type in {"text/plain", "text/html"}:
                return decoded
        except (base64.binascii.Error, UnicodeDecodeError) as decode_error:
            logger.warning("Failed to decode message body: %s", decode_error)

    for part in payload.get("parts", []):
        text = _extract_plain_text(part)
        if text:
            return text

    return ""


@tool(
    name="gmail_get_latest_email",
    description="Retrieve the most recent email from the authenticated Gmail inbox.",
    permission=ToolPermission.READ_ONLY,
)

def gmail_get_latest_email() -> Dict[str, Any]:
    """Fetch the latest email message details using Gmail API."""

    token = ""
    refresh_token = ""
    token_uri = ""
    client_id = ""
    client_secret = ""

    creds = Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret,
        scopes=[
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.readonly"
        ],
    )

    send_message = None

    # Create Gmail API client
    service = build("gmail", "v1", credentials=creds)

    try:
        response = (
            service.users()
            .messages()
            .list(userId="me", maxResults=1)
            .execute()
        )
        messages = response.get("messages", [])
        if not messages:
            logger.info("No messages found in the inbox.")
            return {"status": "empty", "message": "No messages found."}

        latest_id = messages[0]["id"]
        message = (
            service.users()
            .messages()
            .get(userId="me", id=latest_id, format="full")
            .execute()
        )

        payload = message.get("payload", {})
        headers = payload.get("headers", [])
        header_lookup = {h["name"].lower(): h["value"] for h in headers}

        latest_email = {
            "id": latest_id,
            "threadId": message.get("threadId"),
            "subject": header_lookup.get("subject"),
            "from": header_lookup.get("from"),
            "to": header_lookup.get("to"),
            "date": header_lookup.get("date"),
            "snippet": message.get("snippet"),
            "body": _extract_plain_text(payload),
        }

        logger.info("Retrieved latest email id %s with subject %s", latest_id, latest_email["subject"])
        return latest_email

    except HttpError as error:
        logger.error("Gmail API HttpError while retrieving latest email: %s", error)
        return {"status": "error", "message": str(error)}
    except Exception as error:
        logger.exception("Unexpected error while retrieving latest email")
        raise
