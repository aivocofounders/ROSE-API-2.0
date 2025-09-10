# 📞 AI Voice Agent Integration with Twilio  

This project demonstrates how to connect Twilio’s Voice API with **AIVoco’s AI Agent** in real time using a WebSocket stream.  

With this integration, you can place an outbound call via Twilio, and bridge the audio to an AI agent running on AIVoco’s infrastructure.  

---

## 🚀 Prerequisites  

- Python 3.8+  
- [Twilio Account](https://www.twilio.com/try-twilio) (you will get free trial credits)  
- A Twilio phone number with **voice capability**  
- Your AIVoco **API Key** and **Agent ID** (available at [playground.aivoco.com](https://playground.aivoco.com))  

---

## 📦 Installation  

Clone the repository and install dependencies:  

```bash
pip install twilio
```

---

## 🔑 Environment Variables  

Set your Twilio credentials and phone numbers in the script:  

```python
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_registered_number"  # Example: "+121336763"

# From AIVoco
agent_id = "your_agent_id"
api_key = "your_api_key"
```

---

## 🌐 WebSocket URL  

The audio stream from Twilio will be bridged to the following WebSocket endpoint:  

```
wss://call.aivoco.on.cloud.vispark.in/ws/{api_key}/{agent_id}
```

Replace `{api_key}` and `{agent_id}` with the credentials you receive from [playground.aivoco.com](https://playground.aivoco.com).  

---

## 📜 Code Example  

```python
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
```

---

## 📚 References  

- [Twilio Docs: Connect <Stream>](https://www.twilio.com/docs/voice/twiml/connect/stream)  
- [Twilio Voice Quickstart](https://www.twilio.com/docs/voice/quickstart/python)  

---

## 🎯 Notes  

- **API Key & Agent ID**: You’ll get these from [playground.aivoco.com](https://playground.aivoco.com).  
- **Twilio Trial Account**: By default, you can only call verified numbers until you upgrade your Twilio account.  
- **Call Flow**:  
  1. Twilio dials the number.  
  2. Audio is streamed in real time to AIVoco’s AI Agent via WebSocket (`wss://call.aivoco.on.cloud.vispark.in/ws/{api_key}/{agent_id}`).  
  3. The AI agent processes and responds back to the call.  

---

👉 With this setup, you can build interactive AI-driven phone agents powered by **AIVoco + Twilio**.  
