#!/bin/bash
# =============================================
# Watsonx Orchestrate Agent Setup Script
# Author: Epameinondas Douros
# Description: Installs dependencies and imports tools & agent definitions
# =============================================

set -e  # Exit immediately if a command exits with a non-zero status

echo "-------------------------------------------"
echo "🚀 Starting Watsonx Orchestrate agent setup"
echo "-------------------------------------------"

# 1. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# 2. Import custom tools and knowledge base
echo "🧰 Importing Python tools into Orchestrate..."

orchestrate tools import -k python -f tools/gmail_auto_sender_tool.py -r requirements.txt --app-id google_oauth2_auth_code_ibm_184bdbd3
orchestrate tools import -k python -f tools/contracts_information_tool.py -r requirements.txt --app-id google_oauth2_auth_code_ibm_184bdbd3
orchestrate tools import -k python -f tools/client_lookup_tool.py -r requirements.txt --app-id google_oauth2_auth_code_ibm_184bdbd3
orchestrate tools import -k python -f tools/gmail_get_latest_email_tool.py -r requirements.txt --app-id google_oauth2_auth_code_ibm_184bdbd3

echo "Importing Knowledge Database"
orchestrate knowledge-bases import -f knowledge_base/answer_manual.yaml
orchestrate knowledge-bases import -f knowledge_base/inquiries_info.yaml

echo "Checking Knowledge Base Status"
orchestrate knowledge-bases status --name answer_manual
orchestrate knowledge-bases status --name inquiries_info

# 3. Import the agent YAML definition
echo "🤖 Importing the email handler agent..."
orchestrate agents import -f agents/email_handler.yaml

echo "-------------------------------------------"
echo "✅ Setup completed successfully!"
echo "Your Orchestrate tools and agent are now ready to use."
echo "-------------------------------------------"