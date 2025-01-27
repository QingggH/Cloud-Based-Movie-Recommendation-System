from .. import grader

ingest_movies_command_result_path = './assignment03-grader-result/ingest-movies-command-check-result.txt'

ingest_movies_command_content = grader.read_file(ingest_movies_command_result_path)

if not grader.check_contains_target_string(
  ingest_movies_command_content,
  "Row count is the same"
):
  print("-------------------------------------------------------------------------")
  print("TEST: Check if the row count is the same after duplicate ingestion")
  print("Your result:")
  print(ingest_movies_command_content)
  print()
  print("Command [ingest_movies] failed")
  print("Expected Row count is the same")

  exit(1)

print("All checks passed")