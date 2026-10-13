from datasource.models import AddressOrm, SupplierOrm
from web.models import RequestSupplier


def supplier_to_orm(supplier: RequestSupplier) -> SupplierOrm:
    new_address = AddressOrm(**supplier.address.model_dump())
    new_supplier = SupplierOrm(
        name=supplier.name,
        phone_number=supplier.phone_number,
        address=new_address
    )
    return new_supplier