import platform
import os
import socket
import schemas


def get_cpu_info():
    # This is a placeholder. Replace with your method of getting CPU info.
    return "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz"


def get_health_state() -> schemas.HealthState:
    return schemas.HealthState(
        model="gemini",
        chat_model="gemini",
        device=socket.gethostname(),
        arch=platform.machine(),
        cpu_info=get_cpu_info(),
        cpu_count=os.cpu_count(),
        cuda_devices=[],  # Replace with your method of getting CUDA devices
        version=schemas.Version(
            build_date="2022-01-01",
            build_timestamp="1640995200",
            git_sha="abc123",
            git_describe="v1.0.0"
        )
    )


# Function to create prompt from request body
def create_prompt(request_body: schemas.CompletionRequest):
    language, prefix, suffix = None, None, None

    if request_body.language is not None:
        language = request_body.language
    if request_body.segments is not None:
        prefix = request_body.segments.get("prefix")
        suffix = request_body.segments.get("suffix")

    if prefix is None and suffix is None:
        return ""

    prompt = """# Generate 5 code snippets for the following prompt. The generated code snippets should follow these rules:
    1. The generated code snippets should be valid code in the language specified.
    2. The generated code snippets should be related to prefix or suffix.
    3. The generate code snippets should only contain code, No need to include the prompt, language, prefix, suffix, etc.
    4. Separate each code snippet with "|||"

    # Language: {}
    # Prefix code: {}
    # Suffix code: {}
    """.format(language, prefix, suffix)
    return prompt
