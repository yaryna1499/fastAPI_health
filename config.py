from environs import Env

env = Env()
env.read_env()

APP_NAME = env("APP_NAME")
EXPOSE_PORT = env.int("EXPOSE_PORT")
OTLP_GRPC_ENDPOINT = env("OTLP_GRPC_ENDPOINT")