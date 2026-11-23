
import yaml
from openai import OpenAI

#Class to create an agent reading it's informations from config.yaml

config = yaml.safe_load(open("config.yaml"))

class Agent:
    def __init__(self, config):
        self.name = config["name"]
        self. model = config["model"]
        self.base_url = config["base_url"]

    def ask(self, messages):
        print("Logic for ask")
        

