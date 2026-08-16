#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
    echo "GitHub CLI (gh) is required: https://cli.github.com/"
    exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
    echo "Please authenticate GitHub CLI first with: gh auth login"
    exit 1
fi

if [[ ! -f .github/workflows/send_email.yml ]]; then
    echo "Run this script from the root of your eXpresso repository."
    exit 1
fi

REPO="$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null || true)"
if [[ -z "$REPO" ]]; then
    echo "Could not determine the GitHub repository from this clone."
    exit 1
fi

echo "Configuring eXpresso for $REPO"
echo

read -r -p "Your name (for 'Good morning ...') [there]: " RECIPIENT_NAME
RECIPIENT_NAME="${RECIPIENT_NAME:-there}"

read -r -p "Gmail address used to send the email: " EMAIL_USER
if [[ -z "$EMAIL_USER" ]]; then
    echo "The sender email cannot be empty."
    exit 1
fi

read -r -p "Address that should receive the email [$EMAIL_USER]: " EMAIL_TO
EMAIL_TO="${EMAIL_TO:-$EMAIL_USER}"

read -r -p "Sender display name [Morning eXpresso]: " SENDER_NAME
SENDER_NAME="${SENDER_NAME:-Morning eXpresso}"

read -r -p "Email subject [eXpresso]: " EMAIL_SUBJECT
EMAIL_SUBJECT="${EMAIL_SUBJECT:-eXpresso}"

read -r -s -p "Gmail app password (input hidden) (generate from App Password in your Google Account): " EMAIL_PASS
echo
if [[ -z "$EMAIL_PASS" ]]; then
    echo "The Gmail app password cannot be empty."
    exit 1
fi

echo "Saving GitHub Actions secrets and variables..."
printf '%s' "$EMAIL_USER" | gh secret set EMAIL_USER -R "$REPO"
printf '%s' "$EMAIL_PASS" | gh secret set EMAIL_PASS -R "$REPO"
printf '%s' "$EMAIL_TO"   | gh secret set EMAIL_TO   -R "$REPO"
unset EMAIL_PASS

gh variable set RECIPIENT_NAME --body "$RECIPIENT_NAME" -R "$REPO"
gh variable set SENDER_NAME    --body "$SENDER_NAME"    -R "$REPO"
gh variable set EMAIL_SUBJECT  --body "$EMAIL_SUBJECT"  -R "$REPO"

# Scheduled workflows are disabled by default on newly forked public repos.
gh workflow enable send_email.yml -R "$REPO" >/dev/null 2>&1 || true

echo
echo "Configuration saved."
echo "Next: edit 'authors_list' with the arXiv authors you want to follow."
echo "The default schedule is in .github/workflows/send_email.yml."
echo
read -r -p "Trigger a test email now? [Y/n]: " RUN_TEST
RUN_TEST="${RUN_TEST:-Y}"
if [[ "$RUN_TEST" =~ ^[Yy]$ ]]; then
    gh workflow run send_email.yml -R "$REPO"
    echo "Test workflow requested. Check the Actions tab for its result."
fi
