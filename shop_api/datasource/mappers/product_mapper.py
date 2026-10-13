from datasource.models import ProductOrm
from web.models import RequestProduct


def to_orm(new_producr: RequestProduct) -> ProductOrm:
    return ProductOrm(**new_producr.model_dump())