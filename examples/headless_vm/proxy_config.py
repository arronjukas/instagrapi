import os
import time
from typing import Optional
from instagrapi import Client
from instagrapi.exceptions import PleaseWaitFewMinutes, RateLimitError


class ProxyClient:
    def __init__(self, username: str, proxy_config: Optional[str] = None):
        self.username = username
        self.cl = Client()

        if proxy_config:
            self.setup_proxy(proxy_config)

        self.setup_rate_limiting()

    def setup_proxy(self, proxy_config: str) -> None:
        """Configure proxy for Instagram requests"""
        try:
            self.cl.set_proxy(proxy_config)
            host = proxy_config.split('@')[1] if '@' in proxy_config else proxy_config
            print(f'Proxy configured: {host}')
        except Exception as e:
            print(f'Proxy setup failed: {e}')

    def setup_rate_limiting(self) -> None:
        """Configure intelligent delays between requests"""
        self.cl.delay_range = [2, 5]
        self.last_request_time = 0.0
        self.request_count = 0
        self.start_time = time.time()

    def rate_limited_request(self, func, *args, **kwargs):
        """Execute function with rate limiting protection"""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                current_time = time.time()
                time_since_last = current_time - self.last_request_time
                if time_since_last < 2:
                    time.sleep(2 - time_since_last)

                result = func(*args, **kwargs)
                self.last_request_time = time.time()
                self.request_count += 1

                if self.request_count > 50:
                    elapsed = time.time() - self.start_time
                    if elapsed < 3600:
                        sleep_time = 3600 - elapsed
                        print(f'Hourly limit reached, sleeping for {sleep_time:.0f} seconds')
                        time.sleep(sleep_time)
                    self.request_count = 0
                    self.start_time = time.time()

                return result

            except (PleaseWaitFewMinutes, RateLimitError):
                wait_time = 300 + (attempt * 300)
                print(f'Rate limited, waiting {wait_time} seconds (attempt {attempt + 1})')
                time.sleep(wait_time)

            except Exception as e:
                print(f'Request failed (attempt {attempt + 1}): {e}')
                if attempt == max_retries - 1:
                    raise
                time.sleep(30)

        return None


proxy_config = os.getenv('INSTAGRAM_PROXY')  # e.g., "http://user:pass@proxy.com:8080"
client = ProxyClient('username', proxy_config)
