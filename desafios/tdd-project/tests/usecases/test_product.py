from store.schemas.product import ProductOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


"""


async def test_usecases_get_should_not_found():
    with pytest.raises(Exception) as err:
        await product_usecase.get(id=UUID("d4a7e0c1-5b8f-4f6e-9c8b-2c3d1a9b0f7d"))
    breakpoint()
    assert (
        err.value.args[0]
        == "Product not found with filter: UUID('d4a7e0c1-5b8f-4f6e-9c8b-2c3d1a9b0f7d')"
    )
"""
