"""Twitter API Authentication"""

from app.bootstrap.config import Settings
from app.core.exceptions import TwitterAuthenticationError


class TwitterAuthenticator:
    """Handle Twitter API authentication"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._validate_credentials()
    
    def _validate_credentials(self) -> None:
        """Validate that bearer token is configured"""
        if not self.settings.twitter_bearer_token:
            raise TwitterAuthenticationError(
                "Twitter Bearer Token is not configured"
            )
    
    def get_headers(self) -> dict[str, str]:
        """Get authentication headers for Twitter API"""
        return {
            "Authorization": f"Bearer {self.settings.twitter_bearer_token}",
            "Content-Type": "application/json"
        }
