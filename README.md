# Twilio Webhook Server

This repository contains the Flask-based webhook server that handles Twilio call flows.  
It provides TwiML instructions when a call is answered and stores call status updates for later reporting.

---

##  Overview

- **/voice**  
  Twilio hits this endpoint when a call is answered.  
  The server responds with TwiML (Twilio Markup Language) telling Twilio what to do — for example, to play a spoken message.

- **/webhook**  
  Twilio sends call status updates (queued, ringing, answered, completed, failed, etc.) to this endpoint.  
  The server logs these updates into a local file (`results.json`).

- **/results**  
  A debug endpoint to view the entire `results.json`.  
  This is useful to check the lifecycle of each call and verify that status callbacks are working correctly.

---

##  File Structure

- **webhook.py** → Main Flask app with `/voice`, `/webhook`, and `/results` routes.  
- **requirements.txt** → Python dependencies (`Flask`, `twilio`).  
- **results.json** → JSON log file that stores call events for each CallSid.

---

##  Example `results.json`

```json
{
  "CAd9549ed426856ad37c28b5df9ec17180": [
    {"status": "queued", "to": "+353894117081", "from": "+12025551234"},
    {"status": "ringing", "to": "+353894117081", "from": "+12025551234"},
    {"status": "completed", "to": "+353894117081", "from": "+12025551234"}
  ]
}
