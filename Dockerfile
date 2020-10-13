# Use official Python3 parent image
FROM python:3.8-slim-buster

#Set working directory to /usr/local/src
WORKDIR /usr/local/src/knowyourports

# Create non-priveleged user
RUN adduser --disabled-password -gecos '' flask-user

#copy the rest of the app files
COPY . .

# Install any needed packages specified in requirements
RUN pip install --no-cache-dir flask==1.1.2 waitress==1.4.3

# Switch to non-priveleged user
USER flask-user
WORKDIR /home/flask-user

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run a healthcheck every 30 seconds
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD python /usr/local/src/knowyourports/healthcheck.py

#download port number definitions
ADD --chown=flask-user https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml .

# Run web.py when the container launches
CMD ["python", "/usr/local/src/knowyourports/web.py"]
