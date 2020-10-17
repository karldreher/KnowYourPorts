#  Contributing

Contributions to this extension are welcome and will be included in future releases!

To start, please fork this repository.  PRs should be done into the `development` branch.  Pulls to Master will only be done by the repo owner, from the development branch.  

## Testing
Currently there is no automated testing, and this is a possible candidate for contribution.

At a high level, testing should include running the web.py either manually or through a local Docker build, using a web browser to use the frontend, and ensuring any changes you make do not change the ability to search ports.  

Follow the directions in [README.md](README.md) to build manually (section "Usage - Non-Docker Python Config") for quick changes, and eventually conduct testing against the Docker container.

Once your manual testing passes, proceed to PR to the `development` branch of this repository.