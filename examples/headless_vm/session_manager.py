import json
import os
from instagrapi import Client


class SessionManager:
    def __init__(self, username: str, session_file: str = 'session.json'):
        self.username = username
        self.session_file = session_file
        self.cl = Client()

    def load_session(self) -> bool:
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                self.cl.set_settings(session_data)
                print('Session loaded successfully')
                return True
            except Exception as e:
                print(f'Failed to load session: {e}')
        return False

    def save_session(self) -> None:
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.cl.get_settings(), f)
            print('Session saved successfully')
        except Exception as e:
            print(f'Failed to save session: {e}')

    def login_with_session(self, password: str) -> bool:
        if self.load_session():
            try:
                self.cl.account_info()
                print('Using existing session')
                return True
            except Exception:
                print('Session expired, creating new one')
        try:
            self.cl.login(self.username, password)
            self.save_session()
            return True
        except Exception as e:
            print(f'Login failed: {e}')
            return False


if __name__ == '__main__':
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    session_mgr = SessionManager(username)
    if session_mgr.login_with_session(password):
        print('Ready to use Instagram API')
    else:
        print('Failed to establish session')
