import torch

from .faiss_impl import FaissSearch
import os
import torch
# ====== Cấu hình ======
index_file = "/content/drive/MyDrive/AIC2026/fallback (CLIP cũ, xài đc)/OpenAiServer/res/index_all.faiss"
metadata_file = "/content/drive/MyDrive/AIC2026/fallback (CLIP cũ, xài đc)/OpenAiServer/res/metadata_all.json"

class FaissSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("Initializing FaissSingleton...")
        # Initialization logic here (called only once for the first instance)
        self._instance = FaissSearch(
            index_file,
            metadata_file,
            "cpu")
        pass

    def get_instance(self):
        return self._instance