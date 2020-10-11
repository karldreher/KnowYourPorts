# Use official Python3 parent image
FROM python:3.8-slim-buster

#Set working directory to /usr/local/src
WORKDIR /usr/local/src/knowyourports

#download port number definitions
ADD https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml .

#copy the rest of the app files
COPY . .

# Install any needed packages specified in requirements
RUN pip install --no-cache-dir flask==1.1.2 waitress==1.4.3

# Make port 80 available to the world outside this container
EXPOSE 80

# Run web.py when the container launches
CMD ["python", "web.py"]
