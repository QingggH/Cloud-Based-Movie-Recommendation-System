from grader import read_file, check_status_code, check_contains_no_cache_header

def check_wrong_method(method: str):
  content = read_file(f'./assignment02-grader-result/healthcheck-{method}-result.txt')
  if not check_status_code(content, 400):
    print(f"The status code is not 400 for {method}")
    exit(1)

  if not check_contains_no_cache_header(content):
    print(f"The response does not contain Cache-Control: no-cache header for {method}")
    exit(1)

check_wrong_method('post')
check_wrong_method('put')
check_wrong_method('patch')
check_wrong_method('delete')

print("All checks passed")