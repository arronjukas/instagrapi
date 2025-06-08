from instagrapi import Client
import os

cl = Client()
cl.delay_range = [1, 3]

username = os.getenv('INSTAGRAM_USERNAME', 'your_username')
password = os.getenv('INSTAGRAM_PASSWORD', 'your_password')

try:
    print(f"Attempting to login as {username}...")
    cl.login(username, password)
    user_info = cl.account_info()
    print(f"Successfully logged in as: {user_info.username}")
    print(f"Followers: {user_info.follower_count}")
    print(f"Following: {user_info.following_count}")
except Exception as e:
    print(f"Error: {e}")
    print("This may be due to Instagram's security measures")
