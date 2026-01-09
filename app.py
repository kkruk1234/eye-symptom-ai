from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    r = VoiceResponse()
    r.say(
        "Hello. I can provide general information about non-emergency eye symptoms. "
        "I cannot help with eye pain or sudden vision changes. Please ask your question after the beep."
    )
    r.record(
        action="/process",
        max_length=20,
        transcribe=True,
        play_beep=True
    )
    return Response(str(r), mimetype='text/xml')


@app.route("/process", methods=['POST'])
def process():
    transcription = request.form.get("TranscriptionText", "").lower()
    r = VoiceResponse()
    emergency_keywords = ["pain", "sudden", "vision loss", "can't see", "flashes", "floaters"]

    if any(word in transcription for word in emergency_keywords):
        r.say("This could be an eye emergency. Please seek urgent in-person medical care immediately.")
    else:
        r.say(
            "Based on peer-reviewed ophthalmology sources, mild dry or gritty eye symptoms are often "
            "related to screen use, reduced blinking, or dry eye conditions. If symptoms worsen, "
            "an eye care professional should evaluate them."
        )
    return Response(str(r), mimetype='text/xml')
