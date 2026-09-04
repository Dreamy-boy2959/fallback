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

    # RunPod chỉ thực hiện tìm kiếm vector trên GPU
    results = instance.search(search_type, query)

    # Thay vì trả về URL trên server như trước, ta trả về file_name 
    # để phía Laptop tự nhận diện và load ảnh từ ổ cứng local
    results = [
        {
            "file_name": result,  # Tên file/đường dẫn gốc từ kết quả tìm kiếm vector
            "id": videoToId[result.split("/")[1]] if "/" in result and len(result.split("/")) > 1 else None
        }
        for result in results
    ]

    return {
        "result": results
    }


runpod.serverless.start({
    "handler": handler
})
