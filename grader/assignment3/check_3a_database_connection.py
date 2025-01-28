from .. import grader

with_database_result_path = './assignment03-grader-result/healthcheck-get-result-with-database-connection.txt'
without_database_result_path_1 = './assignment03-grader-result/healthcheck-get-result-without-database-connection-1.txt'
without_database_result_path_2 = './assignment03-grader-result/healthcheck-get-result-without-database-connection-2.txt'
resume_database_result_path = './assignment03-grader-result/healthcheck-get-result-with-resume-database-connection.txt'

error_flag = False

with_database_content = grader.read_file(with_database_result_path)
if not grader.check_status_code(with_database_content, 200):
  print("-------------------------------------------------------------------------")
  print("TEST: Check if the status code is 200")
  print("Your result:")
  print(with_database_content)
  print()
  print("Endpoint [GET] /healthcheck with database connection failed")
  print("Expected status code: 200")

  error_flag = True

without_database_content_1 = grader.read_file(without_database_result_path_1)
without_database_content_2 = grader.read_file(without_database_result_path_2)
if not grader.check_status_code(without_database_content_1, 503) and not grader.check_status_code(without_database_content_2, 503):
  print("-------------------------------------------------------------------------")
  print("TEST: Check if the status code is 503 when the database connection is not available")
  print("Your result: (1)")
  print(without_database_content_1)
  print()
  print("Your result: (2)")
  print(without_database_content_2)
  print()
  print("Endpoint [GET] /healthcheck without database connection failed")
  print("Expected status code: 503")

  error_flag = True

resume_database_content = grader.read_file(resume_database_result_path)
if not grader.check_status_code(resume_database_content, 200):
  print("-------------------------------------------------------------------------")
  print("Your result:")
  print(resume_database_content)
  print()
  print("Endpoint [GET] /healthcheck with resume database connection failed")
  print("Expected status code: 200")

  error_flag = True

if error_flag:
  exit(1)

print("All checks passed")





