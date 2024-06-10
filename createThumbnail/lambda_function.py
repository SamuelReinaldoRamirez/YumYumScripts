import boto3
import json

def lambda_handler(event, context):
    # Initialiser le client Lambda AWS
    lambda_client = boto3.client('lambda')
    # Événement pour grabTtkVideoUrl
    grabTtkVideoUrl_event = {
        "url": event["urlmain"]
    }
    print(event)

    # Appeler grabTtkVideoUrl
    response_grabTtkVideoUrl = lambda_client.invoke(
        FunctionName='grabTtkVideoUrl',
        InvocationType='RequestResponse',
        Payload=json.dumps(grabTtkVideoUrl_event)
    )

    # Récupérer la valeur de la clé 'play_url' de la réponse de grabTtkVideoUrl
    grabTtkVideoUrl_body = json.loads(response_grabTtkVideoUrl['Payload'].read())
    body = json.loads(grabTtkVideoUrl_body["body"])
    print(body)
    play_url = body["play_url"]
    # Événement pour grabTiktokThumbUrl
    grabTiktokThumbUrl_event = {
        "url_tiktok": event["urlmain"]
    }

    # Appeler grabTiktokThumbUrl
    response_grabTiktokThumbUrl = lambda_client.invoke(
        FunctionName='grabTiktokThumbUrl',
        InvocationType='RequestResponse',
        Payload=json.dumps(grabTiktokThumbUrl_event)
    )
    # Récupérer les valeurs nécessaires de la réponse de grabTiktokThumbUrl
    grabTiktokThumbUrl_body = json.loads(response_grabTiktokThumbUrl['Payload'].read())
    author_unique_id = grabTiktokThumbUrl_body["body"]["author_unique_id"]
    embed_product_id = grabTiktokThumbUrl_body["body"]["embed_product_id"]
    thumbnail_url = grabTiktokThumbUrl_body["body"]["thumbnail_url"]

    place_id =event["place_id"]

    # Événements pour urlContentToS3
    urlContentToS3_events = [
        {
            "url": play_url,
            "s3_key": f"{place_id}/{author_unique_id}/{embed_product_id}.mp4"
        },
        {
            "url": thumbnail_url,
            "s3_key": f"{place_id}/{author_unique_id}/{embed_product_id}.jpg"
        }
    ]

    results = []
    # Appeler urlContentToS3 pour chaque événement
    for event in urlContentToS3_events:
        response_urlContentToS3 = lambda_client.invoke(
            FunctionName='urlContentToS3',
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
        )
        # Ajouter la réponse à la liste des résultats
        results.append(json.loads(response_urlContentToS3['Payload'].read()))

    return results
