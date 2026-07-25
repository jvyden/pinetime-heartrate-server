import os;

class State:
    heart_rate: int = -1;
    DEVICE_NAME = os.environ.get("DEVICE_NAME", "InfiniTime");
    HOST = os.environ.get("HOST", "localhost");
    PORT = int(os.environ.get("PORT", "8765"));
