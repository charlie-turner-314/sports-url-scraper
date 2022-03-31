from pymongo import MongoClient, ReplaceOne


def insert_games(games, client: MongoClient):
    sportspowerDB = client["sportspowerDB"]
    eventUrlCol = sportspowerDB["eventurls"]
    operations = []
    for game in games:
        operations.append(
            ReplaceOne({"gameId": game['gameId']}, game, upsert=True)
        )

    x = eventUrlCol.bulk_write(operations)
    print(x.modified_count)
