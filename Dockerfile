# Use official Python3 parent image, upgrade alpine packages
FROM python:3-alpine
RUN apk update && apk upgrade --available

ADD . .

# Install any needed packages specified in requirements
RUN pip install --upgrade pip
RUN pip install flask waitress

RUN wget https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml


# Make port 80 available to the world outside this container
EXPOSE 80

# Run web.py when the container launches

CMD ["python", "web.py"]
