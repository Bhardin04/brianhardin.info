import os
import secrets

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # Application settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/site.db")
    USE_DATABASE: bool = os.getenv("USE_DATABASE", "true").lower() == "true"

    # GitHub OAuth settings
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    ADMIN_GITHUB_USERNAME: str = os.getenv("ADMIN_GITHUB_USERNAME", "")

    # Email settings
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "")
    TO_EMAIL: str = os.getenv("TO_EMAIL", "brian.hardin@icloud.com")

    # Social media
    GITHUB_URL: str = os.getenv("GITHUB_URL", "https://github.com/Bhardin04")
    LINKEDIN_URL: str = os.getenv(
        "LINKEDIN_URL", "https://www.linkedin.com/in/brian-hardin-csw-css-a71b0ba/"
    )
    TWITTER_URL: str = os.getenv("TWITTER_URL", "https://twitter.com/@BrianHardi16691")


settings = Settings()
