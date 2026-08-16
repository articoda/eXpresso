# eXpresso

eXpresso is a small GitHub Actions bot that checks arXiv on weekday mornings for papers by authors in `authors_list` and emails the results to you.

## Install your own copy

1. Fork this repository and clone your fork.
2. Install and authenticate the GitHub CLI (`gh auth login`).
3. Enable 2-Step Verification on the Google account that will send the mail and create a Gmail app password for eXpresso.
4. From the repository root run:

   ```bash
   ./setup.sh
   ```

   The script stores the sender address, app password and destination address as GitHub Actions **Secrets**. It stores the greeting name, sender display name and subject as non-sensitive repository **Variables**. The app password is read with hidden terminal input and is not written to a local file.

5. Replace the contents of `authors_list` with the arXiv author names you want to follow, one per line, then commit and push the change.
6. If desired, edit the schedule near the top of `.github/workflows/send_email.yml`. The repository currently runs Monday-Friday at 06:00 UTC.

You can trigger a manual test from the Actions tab or with:

```bash
gh workflow run send_email.yml
```

## Files

```text
.
├── arxiv_query.py  
├── authors_list  
├── authors_test  
├── .github  
│   └── workflows  
│       └── send_email.yml  
├── .gitignore  
├── README.md  
├── requirements.txt  
├── send_test_email.py  
└── setup.sh  

```
