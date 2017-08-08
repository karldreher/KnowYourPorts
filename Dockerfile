# Use official Python3 parent image
FROM python:3-alpine

ADD . .

# Install any needed packages specified in requirements
RUN pip install flask

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "web.py"]
