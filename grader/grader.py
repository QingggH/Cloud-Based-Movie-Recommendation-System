def read_file(file_path: str) -> str:
  try:
    with open(file_path, 'r') as f:
      return f.read()
  except FileNotFoundError as e:
    return ""

def check_status_code(content: str, expected_status_code: int) -> bool:
  return f"HTTP/1.1 {expected_status_code}" in content

def check_contains_no_cache_header(content: str) -> bool:
  return "Cache-Control: No-Cache" in content or "Cache-Control: no-cache" in content or "cache-control: no-cache" in content or "cache-control: no cache" in content