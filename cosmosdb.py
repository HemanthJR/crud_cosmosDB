from flask import Flask, request, jsonify
from azure.cosmos import CosmosClient, PartitionKey
import uuid

app = Flask(__name__)

URL = "https://cosmosrgeastus2fc6f447-8236-4ea6-985edb.documents.azure.com:443/"
KEY = "LXhbEKsvyizS1PMulb3Rbvm1SkAZhJ7ikpPy0Y4cLV4kyP5SBoIUsXN7yRs95k10M83lNJ3r8aH3ACDbvScTRQ=="
client = CosmosClient(URL, KEY)
DATABASE_NAME = 'userDetails'
CONTAINER_NAME = 'users'

database = client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(CONTAINER_NAME, partition_key=PartitionKey(path="/id"))

@app.route('/addUser', methods = ['POST'])
def add_user():
    data = request.json
    add_user = container.upsert_item({
        "id": str(uuid.uuid4()),
        "name": data['name'],
        "password": data['password'] 
    })
    print(data['name'])
    print(add_user)
    return jsonify(add_user)

@app.route('/viewData', methods = ['GET'])
def view_data():
    all_user = list(container.read_all_items())
    # for i in all_user.by_page():
    #     print(i)
    print(all_user)
    return jsonify(all_user)

@app.route('/updateUser/<uid>', methods = ['PUT'])
def updata_data(uid):
    # print(type(uid))
    data = request.json
    # print(data)
    find_record = container.read_item(item= uid, partition_key=uid)
    for key, value in data.items():
        if key not in ["id", "partition_key"]:
            find_record[key] = value
    update_item = container.replace_item(item = uid, body=find_record)
    print(find_record)

    return jsonify({"msg":"updated successfully...."})

@app.route('/deleteUser/<uid>', methods = ['DELETE'])
def delete_user(uid):
    print(uid)
    container.delete_item(item = uid, partition_key = uid)
    return jsonify({"msg":"deleted successfully..."})

if __name__ == "__main__":
    app.run(debug=True)