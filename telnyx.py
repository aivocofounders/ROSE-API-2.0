import os
import json
import urllib.request
import urllib.error
import random


TELNYX_API_URL = "https://api.telnyx.com/v2/calls"


def create_call(
    api_key: str,
    connection_id: str,
    to_number: str,
    from_number: str,
    webhook_url: str,
) -> None:
    payload = {
        "connection_id": connection_id,
        "to": to_number,
        "from": from_number,
        "webhook_url": webhook_url,
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        TELNYX_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            print(f"Status: {resp.status}")
            print(body)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"HTTPError {e.code}: {error_body}")
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")


if __name__ == "__main__":
    api_key = "KEY0199"
    connection_id = "275604"
    to_number = "+917815843509"
    from_number = "+14157075426"
    aivoco_api_key = "Umhzz8Kers0itZiYcO5"
    aivoco_agent_id = "be91ce6f-4"
    webhook_url = f"https://call.aivoco.on.cloud.vispark.in/ws/{aivoco_api_key}/{aivoco_agent_id}"

    create_call(
        api_key=api_key,
        connection_id=connection_id,
        to_number=to_number,
        from_number=from_number,
        webhook_url=webhook_url,
    )