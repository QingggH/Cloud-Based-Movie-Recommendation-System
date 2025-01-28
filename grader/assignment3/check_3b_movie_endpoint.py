from .. import grader

movie_1_result_path = './assignment03-grader-result/movie-1-get-result.txt'
movie_not_exist_result_path = './assignment03-grader-result/movie-not-exist-get-result.txt'
movie_without_database_result_path_1 = './assignment03-grader-result/movie-without-database-connection-1.txt'
movie_without_database_result_path_2 = './assignment03-grader-result/movie-without-database-connection-2.txt'

error_flag = False

movie_1_content = grader.read_file(movie_1_result_path)
if not grader.check_status_code(movie_1_content, 200):
  print("-------------------------------------------------------------------------")
  print("Your result:")
  print(movie_1_content)
  print()
  print("Endpoint [GET] /movie/1 failed")
  print("Expected status code: 200")

  error_flag = True

if not grader.check_contains_target_string(
  movie_1_content,
  '{"movie":{"movieId":1,"title":"Toy Story (1995)","genres":"Adventure|Animation|Children|Comedy|Fantasy"}}'
):
  print("-------------------------------------------------------------------------")
  print("TEST: Check if the response body is correct")
  print("Your result:")
  print(movie_1_content)
  print()
  print("Endpoint [GET] /movie/1 failed")
  print("Expected response body: {\"movie\":{\"movieId\":1,\"title\":\"Toy Story (1995)\",\"genres\":\"Adventure|Animation|Children|Comedy|Fantasy\"}}")

  error_flag = True

movie_not_exist_content = grader.read_file(movie_not_exist_result_path)
if not grader.check_status_code(movie_not_exist_content, 400):
  print("-------------------------------------------------------------------------")
  print("TEST: Check if the status code is 400 when the movie does not exist")
  print("Your result:")
  print(movie_not_exist_content)
  print()
  print("Endpoint [GET] /movie/999999 failed")
  print("Expected status code: 400")

  error_flag = True

movie_without_database_content_1 = grader.read_file(movie_without_database_result_path_1)
movie_without_database_content_2 = grader.read_file(movie_without_database_result_path_2)
if not grader.check_status_code(movie_without_database_content_1, 503) and not grader.check_status_code(movie_without_database_content_2, 503):
  print("-------------------------------------------------------------------------")
  print("TEST: Check if the status code is 503 when the database connection is not available")
  print("Your result: (1)")
  print(movie_without_database_content_1)
  print()
  print("Your result: (2)")
  print(movie_without_database_content_2)
  print()
  print("Endpoint [GET] /movie/1 without database connection failed")
  print("Expected status code: 503")

  error_flag = True

if error_flag:
  exit(1)

print("All checks passed")