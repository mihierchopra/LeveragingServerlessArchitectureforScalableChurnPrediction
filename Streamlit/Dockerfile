# Use a base image with the necessary dependencies
FROM python:3.11.0

# Copy the requirements file and install dependencies
RUN pip install streamlit
RUN pip install pandas
RUN pip install boto3

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run your training script
CMD ["python", "streamlit.py"]
