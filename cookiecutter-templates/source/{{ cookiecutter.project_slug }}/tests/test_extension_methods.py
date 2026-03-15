from openfetch.core.app import OpenFetch
from dlt.extract.validation import PydanticValidator
from openfetch_{{ cookiecutter.target_service_slug }}.main import app as ext_module
try:
    from openfetch_{{ cookiecutter.target_service_slug }}.source import source as {{ cookiecutter.target_service_slug }}_source
except Exception as err:
    pass


def test_extension_is_openfetch():
    assert isinstance(
        ext_module, OpenFetch
    ), "Extension is not an instance of OpenFetch"


def test_extensions_contains_collect():
    assert (
        ext_module.collector is not None
    ), "Extension does not contain @app.collect decorator"


def test_extensions_contains_convert():
    assert (
        ext_module.converter is not None
    ), "Extension does not contain @app.convert decorator"


def test_extension_resources_use_models(subtests):
    for dlt_resource in ext_module.dlt_resources:
        with subtests.test(resource=dlt_resource.name):
            columns = dlt_resource.columns
            validator = isinstance(dlt_resource.validator, PydanticValidator)
            assert (
                columns and validator
            ), f"Extension resource '{dlt_resource.name}' must have columns and use Pydantic models for validation"


def test_extension_resources_use_assets(subtests):
    for dlt_resource in ext_module.dlt_resources:
        with subtests.test(resource=dlt_resource.name):
            model_used = (
                dlt_resource.validator.model
                if isinstance(dlt_resource.validator, PydanticValidator)
                else None
            )
            is_model_an_asset = model_used in ext_module.assets
            assert (
                is_model_an_asset
            ), f"Extension resource '{dlt_resource.name}' must have a corresponding OpenGraph asset defined for its Pydantic model"
