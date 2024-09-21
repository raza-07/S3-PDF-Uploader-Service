from flask import Flask, request, render_template
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

S3_BUCKET = "your-s3-bucket-name"  # Add your S3 bucket name here
S3_KEY = "your-aws-access-key"  # AWS access key should be set via environment variables
S3_SECRET = "your-aws-secret-key"  # AWS secret key should be set via environment variables
S3_REGION = "your-region"  # Add your AWS region here


s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,  # Replace with environment variable or credential handling
    aws_secret_access_key=S3_SECRET,  # Replace with environment variable or credential handling
    region_name=S3_REGION
)

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part found in the request"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file and file.filename.endswith(".pdf"):  # Ensures only PDFs are uploaded
        try:
            s3_client.upload_fileobj(
                file,
                S3_BUCKET,
                file.filename,
                ExtraArgs={"ContentType": "application/pdf"}
            )
            return "File uploaded successfully!"
        except (NoCredentialsError, PartialCredentialsError) as e:
            return f"Error: {str(e)}"
    return "Only PDF files are allowed."

if __name__ == "__main__":
    app.run(debug=True)


# import os
# S3_KEY = os.getenv("AWS_ACCESS_KEY_ID")
# S3_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
