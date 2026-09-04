import runpod

from OpenAiServer.src.ai_search.faiss_singleton import FaissSingleton
from OpenAiServer.src.video_to_id import videoToId


instance = FaissSingleton().get_instance()


def handler(job):
    inputs = job["input"]

    search_type = inputs.get("searchType")
    query = inputs.get("q")

    if not search_type:
        return {
            "error": "Missing searchType"
        }

    if not query:
        return {
            "error": "Missing q"
        }

    results = instance.search(search_type, query)

    results = [
        {
            "url": f"/images/{result}",
            "id": videoToId[result.split("/")[1]]
        }
        for result in results
    ]

    return {
        "result": results
    }


runpod.serverless.start({
    "handler": handler
})
