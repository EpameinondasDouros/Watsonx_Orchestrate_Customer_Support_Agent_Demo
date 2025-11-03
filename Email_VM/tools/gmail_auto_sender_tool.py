import base64
import logging
from email.message import EmailMessage
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import requests
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)


@tool(
    name="gmail_auto_sender",
    description="Send an email through gmail integration. Use it when you are asked to send an email. Input is the email's body",
    permission=ToolPermission.READ_ONLY,
)

def gmail_auto_sender(email_body: str, destination_email: str):
    """Create and send an email message using Gmail API."""

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
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )

    send_message = None

    # Create Gmail API client
    service = build("gmail", "v1", credentials=creds)

    # Create the email message
    message = EmailMessage()
    message.set_content(str(email_body))
    message["To"] = destination_email
    message["From"] = "epadouros@gmail.com"
    message["Subject"] = "Automated Email From Watsonx Orchestrate"

    # Encode the message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}

    # Send the message
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )

    logger.info("Message Id: %s", send_message["id"])

    return email_body
