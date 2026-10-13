from domain.models import User
from google.protobuf.json_format import MessageToDict
from proto.auth_pb2 import RegisterRequest


def request_to_user(request: RegisterRequest) -> User:
    request_dict = MessageToDict(request, preserving_proto_field_name=True)

    return User.model_validate(request_dict)