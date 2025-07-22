"""
Utility functions for the restaurant management system
"""
from datetime import datetime
from typing import List, Any, Optional
from config.settings import SEPARATOR_CHAR


def format_currency(amount: float) -> str:
    """Format a float as currency."""
    return f"${amount:.2f}"


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format a timestamp for display."""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%H:%M:%S")


def print_header(title: str, width: int = 60, char: str = SEPARATOR_CHAR) -> None:
    """Print a formatted header."""
    print(f"\n{char * width}")
    print(f"{title.center(width)}")
    print(f"{char * width}")


def print_section_header(title: str, width: int = 60) -> None:
    """Print a section header."""
    print(f"\n{title}")
    print("-" * width)


def validate_email(email: str) -> bool:
    """Basic email validation."""
    return "@" in email and "." in email and len(email) > 5


def validate_phone(phone: str) -> bool:
    """Basic phone number validation."""
    # Remove common separators
    cleaned = phone.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
    return cleaned.isdigit() and len(cleaned) >= 10


def mask_card_number(card_number: str) -> str:
    """Mask credit card number for security."""
    if len(card_number) < 4:
        return card_number
    return f"****-****-****-{card_number[-4:]}"


def calculate_percentage(part: float, whole: float) -> float:
    """Calculate percentage safely."""
    if whole == 0:
        return 0.0
    return (part / whole) * 100


def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate string to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_list(items: List[Any], separator: str = ", ") -> str:
    """Format a list as a string."""
    return separator.join(str(item) for item in items)
