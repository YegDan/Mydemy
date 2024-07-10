FROM python:3.10-slim


RUN apt-get update && apt-get install -y iputils-ping
# Set the working directory in the container
WORKDIR /user

# Copy the dependencies file to the working directory
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . .

# Expose port 8000 to allow communication to/from server
EXPOSE 8081

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8081"]