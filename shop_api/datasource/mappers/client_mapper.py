from datasource.models import AddressOrm, ClientOrm
from web.models import RequestClient


def client_to_orm(client: RequestClient) -> ClientOrm:
    new_address = AddressOrm(**client.address.model_dump())
    new_client = ClientOrm(
        client_name=client.client_name,
        client_surname=client.client_surname,
        birthday=client.birthday,
        gender=client.gender,
        address=new_address
    )
    return new_client