# def format_timestamp(seconds: float):
#     """Convert seconds to MM:SS or HH:MM:SS format"""
#     hours = int(seconds // 3600)
#     minutes = int((seconds % 3600) // 60)
#     secs = int(seconds % 60)
#     if hours > 0:
#         return f"{hours:02d}:{minutes:02d}:{secs:02d}"
#     return f"{minutes:02d}:{secs:02d}"


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
