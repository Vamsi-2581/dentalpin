"""Closed-vocabulary validation for agent list filters."""

import pytest
from pydantic import ValidationError

from app.modules.gdpr.tools import ListRequestsArgs
from app.modules.imaging_viewer.tools import ListRvgImportsArgs
from app.modules.purchase_orders.tools import ListPurchaseOrdersArgs


@pytest.mark.parametrize(
    ("model", "field"),
    [
        (ListRequestsArgs, "status"),
        (ListRequestsArgs, "request_type"),
        (ListPurchaseOrdersArgs, "order_status"),
        (ListRvgImportsArgs, "status"),
    ],
)
def test_invalid_agent_filter_is_rejected_for_the_named_field(model, field):
    with pytest.raises(ValidationError) as exc_info:
        model(**{field: "pending_approval"})

    assert field in str(exc_info.value)


@pytest.mark.parametrize(
    ("model", "params"),
    [
        (ListRequestsArgs, {"status": "received", "request_type": "access"}),
        (ListPurchaseOrdersArgs, {"order_status": "confirmed"}),
        (ListRvgImportsArgs, {"status": "failed"}),
    ],
)
def test_valid_agent_filters_remain_accepted(model, params):
    result = model(**params).model_dump(exclude_none=True)
    assert {key: result[key] for key in params} == params

