# Use official Python3 parent image
FROM python:3.9-slim-buster AS priveleged-db-setup

#Set working directory to /usr/local/src
WORKDIR /usr/local/src/knowyourports

#copy ports.py and requirements only
COPY "ports.py" "requirements.txt" ./

# Install any needed packages specified in requirements
RUN pip install --no-cache-dir -r requirements.txt

#download port number definitions
ADD https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml .

#setup database using priveleged user to be copied to runtime-image
RUN ["python", "/usr/local/src/knowyourports/ports.py"]


FROM python:3.9-slim-buster AS runtime-image

#Set working directory to /usr/local/src
WORKDIR /usr/local/src/knowyourports

# Create non-priveleged user
RUN adduser --disabled-password -gecos '' flask-user && \
    chgrp flask-user . && \
    chmod g+wx .

#Copy all app files.
COPY --chown=flask-user:flask-user . .

#Add database from previous stage
COPY --chown=flask-user:flask-user --from=priveleged-db-setup /usr/local/src/knowyourports/ports.sqlite .

# Install any needed packages specified in requirements
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-priveleged user
USER flask-user

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run a healthcheck every 30 seconds
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD python /usr/local/src/knowyourports/healthcheck.py

# Run web.py when the container launches
CMD ["python", "/usr/local/src/knowyourports/web.py"]
