import pymongo


def connect_mongo(conn_str):
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        client.test
    except Exception:
        print("Unable to connect to the server")
    return client
