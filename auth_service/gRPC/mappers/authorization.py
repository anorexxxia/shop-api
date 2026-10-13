from domain.models import ChangePasswordModel, LoginModel, ResetPasswordModel
from google.protobuf.json_format import MessageToDict
from proto.auth_pb2 import ChangePasswordRequest, LoginRequest, ResetPasswordRequest


def authorization_to_server(request: LoginRequest):
    # preserving_proto_field_name нужен для того, чтоб переменные оставались в снейк_кейс
    request_dict = MessageToDict(request, preserving_proto_field_name=True)
    return LoginModel.model_validate(request_dict)

def grpc_to_change_password_model(request: ChangePasswordRequest): 
    request_dict = MessageToDict(request, preserving_proto_field_name=True)
    return ChangePasswordModel.model_validate(request_dict)

def grpc_to_reset_password(request: ResetPasswordRequest):
    request_dict = MessageToDict(request, preserving_proto_field_name=True)
    return ResetPasswordModel.model_validate(request_dict)