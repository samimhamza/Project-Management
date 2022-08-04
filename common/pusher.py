import pusher
import environ
env = environ.Env()
environ.Env.read_env()

pusher_client = pusher.Pusher(
    app_id=env("PUSHER_APP_ID"),
    key=env("PUSHER_KEY"),
    secret=env("PUSHER_SECRET"),
    cluster=env("PUSHER_CLUSTER"),
    ssl=True
)
