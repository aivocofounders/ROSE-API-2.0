from twilio.rest import Client as TwilioClient

TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = "121336763"
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


agent_id = ""
api_key = ""
phone_number = "+9178143509"
websocket_url = f"wss://call.aivoco.on.cloud.vispark.in/ws/{api_key}/{agent_id}"

twiml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="{websocket_url}"></Stream>
  </Connect>
  <Pause length="3600"/>
</Response>"""

call = twilio_client.calls.create(
            twiml=twiml_content,
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER
        )

print(f"Call started: {call.sid}")