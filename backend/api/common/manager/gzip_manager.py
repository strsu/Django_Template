import gzip
import json


class GzipManager:

    @classmethod
    def compress_JSON(cls, data):
        # Convert serializable data to JSON string
        json_data = json.dumps(data)
        # Convert JSON string to bytes
        encoded = json_data.encode("utf-8")
        # Compress
        compressed = gzip.compress(encoded)
        return compressed

    @classmethod
    def decompress_JSON(cls, compressed_json):
        # Decompress a compressed JSON data to bytes and decode it to string
        data = gzip.decompress(compressed_json).decode("utf-8")
        # Convert JSON string into Python dictionary
        decompressed = json.loads(data)
        return decompressed
