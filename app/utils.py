import yaml
from passlib.context import CryptContext

def load_config():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
        return config
    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)