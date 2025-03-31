import re

def parse_file_ids(a: str, b: str) -> list[int]:
    pattern = r'https?://[^/]+/storage/(\d+)'
    matches = re.findall(pattern, a) + re.findall(pattern, b)
    return [int(match) for match in matches]
