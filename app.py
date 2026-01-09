from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

# This route handles the initial call
@app.route("/voice", methods=['POST'])
def voice():
    r = VoiceResponse()
    r.say(
        "Hello. I can provide general information about non-emergency eye symptoms. "
        "I cannot help with eye pain or sudden vision changes. Please ask your question after the beep."
    )
    # Use Gather with speech input for live transcription
    r.gather(
        input='speech',
        action='/process',
        speechTimeout='auto',
        timeout=5
    )
    return Response(str(r), mimetype='text/xml')


# This route processes the user's speech
@app.route("/process", methods=['POST'])
def process():
    transcription = request.values.get("SpeechResult", "")
    transcription_lower = transcription.lower() if transcription else ""
    r = VoiceResponse()

    # Emergency keywords (multi-word phrases included)
    emergency_keywords = [
        "pain", "severe", "sudden", "vision loss",
        "can't see", "cannot see", "flashes", "floaters",
        "curtain falling", "curtain over eye", "trauma", "injury"
    ]

    if any(keyword in transcription_lower for keyword in emergency_keywords):
        r.say(
            "This could be an eye emergency. Sudden vision changes, pain, flashes, "
            "or a curtain falling over your vision require immediate in-person evaluation. "
            "Please seek urgent medical care immediately."
        )
        return Response(str(r), mimetype='text/xml')

    # Allergy symptoms
    allergy_keywords = ["itchy", "itching", "allergy", "pollen", "seasonal"]
    if any(word in transcription_lower for word in allergy_keywords):
        r.say(
            "Itchy eyes without pain are often related to allergies. Peer reviewed studies "
            "show this can be triggered by pollen, dust, or pet dander. Cold compresses and "
            "preservative free artificial tears may help. An eye care professional can confirm."
        )
        return Response(str(r), mimetype='text/xml')

    # Infection symptoms
    infection_keywords = ["red", "discharge", "crust", "pink eye", "goop"]
    if any(word in transcription_lower for word in infection_keywords):
        r.say(
            "Redness with discharge may be associated with an eye infection. Peer reviewed "
            "guidelines recommend avoiding touching the eyes and seeking evaluation to determine "
            "whether treatment is needed."
        )
        return Response(str(r), mimetype='text/xml')

    # Blurry vision
    blurry_keywords = ["blurry", "blurred", "foggy", "hard to focus"]
    if any(word in transcription_lower for word in blurry_keywords):
        r.say(
            "Blurry vision without pain can be related to dryness, fatigue, or uncorrected "
            "refractive error. If blur persists or worsens, an eye care professional should "
            "evaluate it."
        )
        return Response(str(r), mimetype='text/xml')

    # Dry eye
    dry_eye_keywords = ["dry", "gritty", "burning", "scratchy", "tired"]
    if any(word in transcription_lower for word in dry_eye_keywords):
        r.say(
            "Dry or gritty eye symptoms are commonly associated with reduced blinking, screen "
            "use, or dry eye conditions. Artificial tears and regular breaks from screens "
            "are commonly recommended in peer reviewed literature."
        )
        return Response(str(r), mimetype='text/xml')

    # Fallback if nothing matches
    r.say(
        "Your symptoms do not clearly match a specific category. If symptoms persist, "
        "change, or worsen, an eye care professional can provide individualized evaluation."
    )
    return Response(str(r), mimetype='text/xml')


# Required for running on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
