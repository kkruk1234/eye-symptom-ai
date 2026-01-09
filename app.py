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

    emergency_keywords = [
        "pain", "severe", "sudden", "vision loss",
        "can't see", "cannot see", "flashes", "floaters",
        "curtain", "trauma", "injury"
    ]

    dry_eye_keywords = [
        "dry", "gritty", "burning", "scratchy", "tired"
    ]

    allergy_keywords = [
        "itchy", "itching", "allergy", "pollen", "seasonal"
    ]

    infection_keywords = [
        "red", "discharge", "crust", "pink eye", "goop"
    ]

    blurry_keywords = [
        "blurry", "blurred", "foggy", "hard to focus"
    ]

    if any(word in transcription for word in emergency_keywords):
        r.say(
            "This could be an eye emergency. Sudden vision changes, pain, or flashes "
            "require urgent in-person evaluation. Please seek immediate medical care."
        )

    elif any(word in transcription for word in allergy_keywords):
        r.say(
            "Itchy eyes without pain are often related to allergies. Peer reviewed studies "
            "show this can be triggered by pollen, dust, or pet dander. Cold compresses and "
            "preservative free artificial tears may help. An eye care professional can confirm."
        )

    elif any(word in transcription for word in infection_keywords):
        r.say(
            "Redness with discharge may be associated with an eye infection. Peer reviewed "
            "guidelines recommend avoiding touching the eyes and seeking evaluation to determine "
            "whether treatment is needed."
        )

    elif any(word in transcription for word in blurry_keywords):
        r.say(
            "Blurry vision without pain can be related to dryness, fatigue, or uncorrected "
            "refractive error. If blur persists or worsens, an eye care professional should "
            "evaluate it."
        )

    elif any(word in transcription for word in dry_eye_keywords):
        r.say(
            "Dry or gritty eye symptoms are commonly associated with reduced blinking, screen "
            "use, or dry eye conditions. Artificial tears and regular breaks from screens "
            "are commonly recommended in peer reviewed literature."
        )

    else:
        r.say(
            "Your symptoms do not clearly match a specific category. If symptoms persist, "
            "change, or worsen, an eye care professional can provide individualized evaluation."
        )

    return Response(str(r), mimetype='text/xml')
