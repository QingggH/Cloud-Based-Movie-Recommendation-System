# Project Deployment to EC2

- **Name:** Yiqing Huang
- **EC2 Instance Type:** t2.micro
- **OS:** Ubuntu
- **Programming Language:** Python 3.13.1
- **Web Server Framework Used:** Flask
- **Build and Deploy instruction:**

  1. **Checkout Code**  
     The workflow automatically triggers whenever there is a push to the `main` branch. It fetches the latest code from the repository using the `actions/checkout@v3` GitHub Action.

  2. **Create SSH Key File**  
     Generate an SSH private key file (`ec2_key.pem`) from the `EC2_SSH_KEY` stored in GitHub Secrets. Proper permissions are applied to ensure the file's security.

  3. **Configure AWS CLI**  
     Set up the AWS CLI credentials using `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` stored in GitHub Secrets. This step allows the workflow to interact with AWS services like EC2.

  4. **Check EC2 Instance State**  
     Use the AWS CLI to check the current state of the EC2 instance (e.g., `running`, `stopped`). The state is stored as an environment variable for conditional actions in subsequent steps.

  5. **Start EC2 Instance**  
     If the EC2 instance is in a `stopped` state, start the instance and wait until it is running using the AWS CLI.

  6. **Get EC2 Public IP**  
     Retrieve the public IP address of the EC2 instance using the AWS CLI. This IP is saved as an environment variable for remote access in later steps.

  7. **Stop Old Application and Clean Files**  
     Connect to the EC2 instance using SSH, terminate any running Python processes (if applicable), and remove the old application files from the deployment directory.

  8. **Copy Code to EC2**  
     Use `scp` to securely copy the local codebase to the EC2 instance at the desired path (`/home/ubuntu/my_flask_app`).

  9. **Install Dependencies and Run Application**

     - SSH into the EC2 instance.
     - Update system packages and install `python3`, `pip`, and `venv`.
     - Create and activate a virtual environment.
     - Install the project dependencies specified in `requirements.txt`.
     - Run the Flask application in the background, logging output to `test.log`.

  10. **Create Environment File for Grader**  
      Generate a `grader-env.txt` file that contains the EC2 instance's public IP address (`SSH_HOST`) and the username (`SSH_USER`).

  11. **Upload Environment File as an Artifact**  
      Upload the `grader-env.txt` file as an artifact using `actions/upload-artifact@v4`, making it available for subsequent workflows or manual grading purposes.
