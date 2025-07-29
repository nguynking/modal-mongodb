import modal

image = modal.Image.debian_slim().pip_install("pymongo[srv]")
app = modal.App(image=image)


@app.function(secrets=[modal.Secret.from_name("mongodb-secret")])
def ping():
    import os
    import urllib

    from pymongo import MongoClient
    from pymongo.server_api import ServerApi

    user, password = map(urllib.parse.quote_plus, (os.environ["MONGO_USER"], os.environ["MONGO_PASSWORD"]))
    host = os.environ["MONGO_HOST"]

    uri = f"mongodb+srv://{user}:{password}@{host}/"

    client = MongoClient(uri, server_api=ServerApi("1"))
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
