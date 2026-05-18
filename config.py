from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_ROOT / "assets"
UPLOADS_DIR = ASSETS_DIR / "uploads"

APP_NAME = "CultureBridge"
APP_SUBTITLE = "Building Peace, One Culture at a Time"
WINDOW_SIZE = "1160x760"
MIN_WINDOW_SIZE = (980, 640)

CATEGORIES = ("All", "Food", "Festival", "Music", "Custom")
POST_CATEGORIES = CATEGORIES[1:]

COMMON_COUNTRIES = (
    "Nigeria",
    "Ghana",
    "Kenya",
    "South Africa",
    "Egypt",
    "India",
    "Japan",
    "China",
    "Brazil",
    "Mexico",
    "United States",
    "United Kingdom",
    "France",
    "Germany",
    "Canada",
)

THEME = {
    "bg": "#f7f7f2",
    "surface": "#ffffff",
    "surface_alt": "#eef4ed",
    "text": "#1e2723",
    "muted": "#5f6f66",
    "primary": "#2d6a4f",
    "primary_dark": "#1b4332",
    "accent": "#d88c3a",
    "danger": "#b42318",
    "warning_bg": "#fff3cd",
    "border": "#cbd5cf",
}

