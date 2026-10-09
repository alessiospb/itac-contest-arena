import json

from playwright.async_api import Response


def is_events_list_response(response: Response, **params) -> bool:
    if "rpc_events_list" not in response.url:
        return False
    body = json.loads(response.request.post_data or "{}")
    return all(body.get(f"p_{key}") == value for key, value in params.items())
