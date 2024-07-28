# Use an official Python runtime as a parent image
FROM python:3.12.1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt or pyproject.toml
RUN pip install --no-cache-dir poetry
RUN poetry install --no-dev

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["poetry", "run", "python", "main.py"]
