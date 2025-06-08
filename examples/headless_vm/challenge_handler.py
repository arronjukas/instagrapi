import imaplib
import email
import re
import time
import os
from typing import Optional
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice


def get_code_from_email(username: str, email_addr: str, email_password: str) -> Optional[str]:
    """Extract verification code from Gmail inbox"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, email_password)
        mail.select("inbox")

        result, data = mail.search(None, "(UNSEEN)")
        if result != "OK":
            return None

        ids = data[0].split()
        for num in reversed(ids[-5:]):
            mail.store(num, "+FLAGS", "\\Seen")
            result, data = mail.fetch(num, "(RFC822)")

            if result == "OK":
                msg = email.message_from_bytes(data[0][1])

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                code_match = re.search(r"\b(\d{6})\b", body)
                if code_match and 'instagram' in body.lower():
                    return code_match.group(1)

        mail.logout()
    except Exception as e:
        print(f"Email code extraction failed: {e}")

    return None


def challenge_code_handler(username: str, choice: ChallengeChoice):
    """Handle challenge codes for Instagram verification"""
    email_addr = os.getenv('CHALLENGE_EMAIL')
    email_password = os.getenv('CHALLENGE_EMAIL_PASSWORD')

    if choice == ChallengeChoice.EMAIL and email_addr:
        print(f"Waiting for email verification code for {username}")
        for _ in range(12):  # wait up to 2 minutes
            code = get_code_from_email(username, email_addr, email_password)
            if code:
                print(f"Found verification code: {code}")
                return code
            time.sleep(10)

    return False


def setup_challenge_client() -> Client:
    """Setup client with challenge resolution"""
    cl = Client()
    cl.challenge_code_handler = challenge_code_handler
    cl.delay_range = [2, 5]
    return cl


if __name__ == "__main__":
    cl = setup_challenge_client()
    # Use this client for Instagram operations
