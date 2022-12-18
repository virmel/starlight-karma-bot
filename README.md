# Starlight Discord Bot

## Requirements

* flyctl
* Earthly
* Docker
* Python 3.11 (or pyenv)
* pipenv

## Get Started

```bash
# Create the default .env file. Edit it with your bot token
cp defaults.env .env

# Install dependencies
pipenv install

# Run the program
pipenv run python src/main.py

# Or, start up the copy in a container
earthly +up
```
