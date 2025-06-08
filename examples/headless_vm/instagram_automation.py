#!/usr/bin/env python3
import json
import logging
import os
import sys
import time

from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    PleaseWaitFewMinutes,
    MediaNotFound,
    UserNotFound,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_automation.log'),
        logging.StreamHandler(sys.stdout),
    ],
)


class InstagramAutomation:
    def __init__(self, username: str, password: str, session_file: str = 'instagram_session.json'):
        self.username = username
        self.password = password
        self.session_file = session_file
        self.logger = logging.getLogger(__name__)

        self.cl = Client()
        self.cl.delay_range = [2, 5]

        if os.getenv('CHALLENGE_EMAIL'):
            self.setup_challenge_handlers()

    def setup_challenge_handlers(self) -> None:
        def challenge_code_handler(username: str, choice):
            self.logger.info('Challenge required for %s, choice: %s', username, choice)
            return False

        self.cl.challenge_code_handler = challenge_code_handler

    def load_session(self) -> bool:
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                self.cl.set_settings(session_data)
                self.logger.info('Session loaded successfully')
                return True
            except Exception as e:
                self.logger.error('Failed to load session: %s', e)
        return False

    def save_session(self) -> None:
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.cl.get_settings(), f, indent=2)
            self.logger.info('Session saved successfully')
        except Exception as e:
            self.logger.error('Failed to save session: %s', e)

    def login(self) -> bool:
        if self.load_session():
            try:
                account = self.cl.account_info()
                self.logger.info('Using existing session for %s', account.username)
                return True
            except LoginRequired:
                self.logger.info('Session expired, creating new session')

        try:
            self.logger.info('Logging in as %s', self.username)
            self.cl.login(self.username, self.password)
            self.save_session()
            return True
        except ChallengeRequired:
            self.logger.error('Challenge required - manual intervention needed')
            return False
        except Exception as e:
            self.logger.error('Login failed: %s', e)
            return False

    def safe_request(self, func, *args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except PleaseWaitFewMinutes as e:
                wait_time = 300 * (attempt + 1)
                self.logger.warning('Rate limited, waiting %d seconds', wait_time)
                time.sleep(wait_time)
            except (MediaNotFound, UserNotFound) as e:
                self.logger.error('Not found error: %s', e)
                return None
            except Exception as e:
                self.logger.error('Request failed (attempt %d): %s', attempt + 1, e)
                if attempt == max_retries - 1:
                    raise
                time.sleep(30)
        return None

    def get_user_info(self, username: str):
        return self.safe_request(self.cl.user_info_by_username, username)

    def upload_photo(self, image_path: str, caption: str = ''):
        if not os.path.exists(image_path):
            self.logger.error('Image not found: %s', image_path)
            return None
        return self.safe_request(self.cl.photo_upload, image_path, caption)


def main() -> None:
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    if not username or not password:
        print('Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables')
        sys.exit(1)

    automation = InstagramAutomation(username, password)
    if automation.login():
        print('Successfully logged in!')
        user_info = automation.get_user_info(username)
        if user_info:
            print(f'Account: {user_info.full_name}')
            print(f'Followers: {user_info.follower_count}')
    else:
        print('Login failed!')


if __name__ == '__main__':
    main()
