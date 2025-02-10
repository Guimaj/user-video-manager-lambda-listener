import json
import pymongo
import os

def get_mongodb_collection():
    db_name = os.environ.get("databaseName")
    mongodb_uri = os.environ.get("mongoUri")
    collection_name = os.environ.get("collection")

    mongo_client = pymongo.MongoClient(mongodb_uri)
    db = mongo_client[db_name]
    collection = db[collection_name]

    return collection

def lambda_handler(event, context):
    try:
    
        for record in event['Records']:
            message_body = record['body']
            data = json.loads(message_body)
            
            arquivo_id = data.get("x-amz-arquivo-id")
            status = data.get("status")     
            
            collection = get_mongodb_collection()

            video = collection.find_one({"_id": arquivo_id})
            
            if video:
                collection.update_one({"_id": arquivo_id}, {"$set": {"status": status}})
                return {
                    "statusCode": 200,
                    "body": f"Status do vídeo '{arquivo_id}' atualizado para '{status}'."
                }
            else:
                return {
                    "statusCode": 404,
                    "body": f"Vídeo '{arquivo_id}' não encontrado."
                }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Erro ao processar mensagem: {str(e)}"
        }
