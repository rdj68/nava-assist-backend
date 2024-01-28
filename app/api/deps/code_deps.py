import json
from vertexai.language_models import ChatMessage

def serialize_object(obj):
    print(json.dumps(obj, default=lambda o: o.__dict__))
    return json.dumps(obj, default=lambda o: o.__dict__)

def deserialize_object(serialized_obj):
    obj_dict = json.loads(serialized_obj)
    return ChatMessage(**obj_dict)