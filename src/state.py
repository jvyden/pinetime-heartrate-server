import time
import os;

class State:
    # dynamic state
    heart_rate: int = -1;
    last_valid_contact: float = 0;

    # configuration
    DEVICE_NAME = os.environ.get("DEVICE_NAME", "InfiniTime");
    HOST = os.environ.get("HOST", "localhost");
    PORT = int(os.environ.get("PORT", "8765"));
    WEB_ENABLE = bool(os.environ.get("WEB_ENABLE", "true"))
    OSC_ENABLE = bool(os.environ.get("OSC_ENABLE", "true"))
    OSC_HOST = os.environ.get("OSC_HOST", "127.0.0.1");
    OSC_PORT = int(os.environ.get("OSC_PORT", "9000"));
