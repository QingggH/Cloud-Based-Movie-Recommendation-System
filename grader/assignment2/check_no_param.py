from .. import grader

result_path = './assignment02-grader-result/healthcheck-get-params-result.txt'

content = grader.read_file(result_path)

if not grader.check_status_code(content, 400):
  print("The status code is not 400")
  exit(1)

if not grader.check_contains_no_cache_header(content):
  print("The response does not contain Cache-Control: no-cache header")
  exit(1)

print("All checks passed")