# KnowYourPorts
An application for looking up TCP/IP ports.  


KnowYourPorts currently has two components:  a web app and a console application.
Each of these can be used to quickly check a TCP/IP port number for it's function.  

A good IT professional should memorize the well-known ports, but an even better one will use a tool like this to keep their brainpower free for more practical matters.  

KnowYourPorts is built on Python 3 and uses the Service Name and Port Number Registry from IANA, located here: http://www.iana.org/assignments/port-numbers

This app claims no affiliation with IANA.  


## Usage - Console
```
python ports.py <port number>
```
Example:
```
>python ports.py 23
23
Telnet
```
The whole command (including python and the full path to the ports app) can easily be aliased to whatever is a good mnemonic, I would suggest simply "ports".


## Usage - Web
Start "web.py".  Open a web browser to the specified URL.  
This requires [Flask](http://flask.pocoo.org/) and the Python standard library.  With those two requirements satisfied, this is a self-contained web app.  

You can check out a hosted version here:  http://knowyourports.pythonanywhere.com/

## License

KnowYourPorts is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

KnowYourPorts is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with KnowYourPorts.  If not, see <http://www.gnu.org/licenses/>.
