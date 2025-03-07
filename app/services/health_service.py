import platform
import os
import socket
from app.schemas.general_schema import HealthState, Version


def get_cpu_info():
    # This is a placeholder. Replace with your method of getting CPU info.
    return "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz"


def get_health_state() -> HealthState:
    return HealthState(
        model="gemini",
        chat_model="gemini",
        device=socket.gethostname(),
        arch=platform.machine(),
        cpu_info=get_cpu_info(),
        cpu_count=os.cpu_count(),
        cuda_devices=[],
        version=Version(
            build_date="2022-01-01",
            build_timestamp="1640995200",
            git_sha="abc123",
            git_describe="v1.0.0"
        )
    )
