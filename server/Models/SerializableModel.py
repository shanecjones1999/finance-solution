import json


class SerializableModel:
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, SerializableModel):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [item.to_dict() if isinstance(
                    item, SerializableModel) else item for item in value]
            else:
                result[key] = value
        return result

    def to_json(self):
        return json.dumps(self.to_dict(), default=str)
