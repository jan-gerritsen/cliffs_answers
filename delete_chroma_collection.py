import chromadb


def delete_collection(collection_name):
    client = chromadb.PersistentClient(path="./chroma_data")
    try:
        client.get_collection(name="my_collection")
        client.delete_collection(name="my_collection")
    except:
        pass


if __name__ == "__main__":
    delete_collection('my_collection')