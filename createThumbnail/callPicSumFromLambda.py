import aiohttp
import asyncio


async def fetch_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise Exception("Failed to fetch image from URL: {}".format(url))


async def lambda_handler(event, context):
    print("toto")
    print("titi")
    print("toto")
    print("titi")
    url = "https://picsum.photos/200/300"

    try:
        image_content = await fetch_image(url)
        print("GGG--------------------------------")
        print("GGG--------------------------------")
        return {
            'statusCode': 200,
            'body': image_content,
            'headers': {
                'Content-Type': 'image/jpeg'
            }
        }
    except Exception as e:
        print(e)
        print("!!!!!!!!!!!!!!!!!")
        return {
            'statusCode': 500,
            'body': "Error occurred: {}".format(str(e))
        }
    finally:
        print("finally")


# Pour l'exécution de la fonction lambda
async def main():
    event = {}  # Mettez vos données d'événement ici
    context = {}  # Mettez votre contexte ici
    result = await lambda_handler(event, context)
    print(result)


# Exécution de la fonction lambda sans asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())
