# beanomatic
A beano reaction bot

### Installation:
1. Clone the repo, or otherwise get your hands on the code.

`git clone https://github.com/Birddude1230/beanomatic.git`

2. Get in the same directory as the files.

`cd beanomatic`

3. Create a virtual environment using `pipenv`. Not necessary, but it's a good idea to keep dependencies tied to the projects they're for.
Currently, only dependency is the `discord` package, needed for hopefully obvious reasons. 

`pipenv install`

4. Pass in your discord token. You can do this as an environment variable with the key of `DISCORD_TOKEN`. Pipenv will automatically get environment variables from a `.env` file alongside the Pipfile.
Alternatively, you could modify the code, and paste your discord token in the place of the line reading it from the environment variables.

`echo "export DISCORD_TOKEN=YourDiscordTokenHere" > .env`

### Running:
From the same `beanomatic` directory as above:

`pipenv run python main.py`

