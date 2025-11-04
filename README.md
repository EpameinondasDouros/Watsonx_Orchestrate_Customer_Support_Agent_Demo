# Watsonx Orchestrate Customer Support Agent Demo

An end-to-end reference implementation that showcases how to build an email-driven customer support workflow on **IBM watsonx Orchestrate**. The demo covers everything from configuring Gmail connectivity to drafting and sending contract-specific replies with reusable agent tools.

---

## Why This Repo?
- Automate email triage and responses with an orchestration-first approach.
- Reuse purpose-built tools (client lookup, contract details, Gmail send/fetch).
- Demonstrate how to capture user approval before sending outbound messages.
- Provide repeatable setup scripts and requirements for fast onboarding.

---

## Repository Layout
```
Watsonx_Orchestrate_Customer_Support_Agent_Demo/
├── Email_VM/
│   ├── agents/
│   │   └── email_handler.yaml        # Orchestrate agent definition + flow logic
│   ├── tools/
│   │   ├── client_lookup_tool.py     # Sample client metadata lookup
│   │   ├── contracts_information_tool.py
│   │   ├── gmail_auto_sender_tool.py # OAuth-powered Gmail send helper
│   │   ├── gmail_get_latest_email_tool.py
│   │   └── __init__.py
│   ├── requirements.txt              # Python deps for the tools runtime
│   ├── setup_orchestrate_agent.sh    # Convenience script to publish the agent
│   └── client_secret_creator.ipynb   # Notebook to bootstrap OAuth credentials
├── LICENSE
└── README.md
```

---

## Prerequisites
- Python 3.11 (matching the `requirements.txt` tested environment)
- Access to an **IBM watsonx Orchestrate** tenant with agent builder privileges
- Gmail account (Workspace or personal) with API enabled
- Google Cloud project with the *Gmail API* turned on and an OAuth **Desktop App** client ID
- `client_secret.json` downloaded from Google Cloud (place it under `Email_VM/`)

---

## Quick Start

1. **Clone and enter the repo**
   ```bash
   git clone <this_repo_url>
   cd Watsonx_Orchestrate_Customer_Support_Agent_Demo/Email_VM
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Generate Gmail OAuth tokens**
   - Ensure `client_secret.json` (Desktop App client) is in `Email_VM/`.
   - Run the helper script/notebook:
     ```python
     # quick_token_bootstrap.py (create temporarily)
     from pathlib import Path
     from google_auth_oauthlib.flow import InstalledAppFlow

     SCOPES = [
         "https://www.googleapis.com/auth/gmail.send",
         "https://www.googleapis.com/auth/gmail.readonly",
     ]

     flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
     creds = flow.run_local_server(port=0)
     Path("token.json").write_text(creds.to_json())
     print("token.json created with scopes:", creds.scopes)
     ```
   - Complete the consent screen; a `token.json` is saved alongside the tools.
   - Treat `token.json` as a secret (do not commit it).

4. **Publish the agent (optional script)**
   ```bash
   ./setup_orchestrate_agent.sh
   ```
   The script can be adapted to push the `email_handler.yaml` agent and register tools inside your watsonx Orchestrate workspace.

---

## Core Components

- **`email_handler.yaml`**  
  Defines the conversational flow:
  - Looks up a client.
  - Retrieves contract details.
  - Drafts an email body.
  - Presents the draft to the user for review and explicit approval.
  - Sends the email only if the user confirms.
  - Reports status back to the user.

- **Gmail Tooling**
  - `gmail_auto_sender_tool.py`: sends emails through OAuth2 without storing raw tokens in code.
  - `gmail_get_latest_email_tool.py`: fetches the most recent email for context gathering.
  - Both rely on the shared OAuth credentials generated earlier.

- **Business Data Tools**
  - `client_lookup_tool.py` and `contracts_information_tool.py` simulate CRM and contract repositories so the demo runs end-to-end without external systems.

---

## Running in watsonx Orchestrate
1. Upload the tools (or point your orchestrate runtime to this repo).
2. Register the tools and agent via the Agent Builder UI or the included shell script.
3. Trigger the agent inside Orchestrate:
   - Ask the agent to draft an email for a specific client.
   - Review the proposed content.
   - Approve or request changes; the tool respects your decision before sending.

---

## Common Troubleshooting

| Issue | Likely Cause | Resolution |
|-------|--------------|------------|
| `invalid_scope: Bad Request` when fetching emails | Refresh token was created without the Gmail Read scope | Regenerate `token.json` with both `gmail.send` and `gmail.readonly` scopes |
| `redirect_uri_mismatch` during OAuth flow | Using Web client credentials instead of Desktop App | Create a Desktop App OAuth client in Google Cloud |
| Consent screen blocked (`access_denied`) | Gmail account not listed as tester | In Google Cloud Console → OAuth consent screen → add the email under Test Users |
| Missing `WXO_SECURITY_SCHEMA_*` env var | Connection not registered for Orchestrate | Export the expected env vars or configure via Orchestrate UI |

---

## Security Notes
- Keep `client_secret.json` and `token.json` out of version control.
- Rotate OAuth tokens periodically and revoke unused ones from your Google Account Security settings.
- If you plan to productionize, migrate secrets into your preferred secret manager and enforce least-privilege scopes.

---

## Contributing
1. Fork the repo & create a feature branch.
2. Make changes and add/update tests or sample transcripts.
3. Submit a PR describing the enhancements; please exclude any regenerated secrets.

---

## License

This project is released under the [Apache 2.0 License](LICENSE).

---

Happy orchestrating! Feel free to adapt the tools or YAML flows to suit your own email-driven support scenarios.
