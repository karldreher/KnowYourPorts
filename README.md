# KnowYourPorts
KnowYourPorts is a web application for looking up TCP/IP ports.  

This can be used to quickly check a TCP/IP port number for it's function.  

You can check out a hosted version here:  https://knowyourports.azurewebsites.net/


A good IT professional should memorize the well-known ports, but an even better one will use a tool like this to keep their brainpower free for more practical matters.  

KnowYourPorts is built on Python 3 and uses the Service Name and Port Number Registry from IANA, located here: http://www.iana.org/assignments/port-numbers

KnowYourPorts uses several other components:  
* Flask for the web application framework.
* SQLITE for data storage.
* Waitress to act as a WSGI server to the Flask app.



## Usage - Web
After installing the requirements, start "web.py".  Open a web browser to the specified URL.

```bash
$ wget https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml 
$ pip install Flask
$ pip install waitress
$ (export PORT=4000; python web.py) # This sets the port to run on, 80 is default
```



## Usage - Docker
Docker is the preferred methodology for deploying KnowYourPorts.  A dockerfile is included in this repo which fulfills all the requirements above.  With Docker installed, this is easy to build and run.

```bash
$ docker build -t knowyourports
$ docker run -p 80:80 knowyourports 

```

You can also utilize the official [Docker Hub version of KnowYourPorts](https://hub.docker.com/r/karldreher/knowyourports).
```
docker pull karldreher/knowyourports
```



## License

KnowYourPorts is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

KnowYourPorts is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with KnowYourPorts.  If not, see <http://www.gnu.org/licenses/>.
