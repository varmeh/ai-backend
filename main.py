import uvicorn
from os import environ as env


### ----------------- Environment Variable Configuration ----------------- ###
# load_dotenv() finds and loads variables from a .env file.
# If .env is absent or a variable isn't found, it uses variables from the host environment.
# It uses .env variables for local runs and host variables for deployments
from dotenv import load_dotenv

load_dotenv()


host = env.get("HOSTNAME")
port = int(env.get("PORT", 8000))

if __name__ == "__main__":
    __package__ = "app"
    uvicorn.run("app.app:app", host=host, port=port, reload=True, log_level="debug")
