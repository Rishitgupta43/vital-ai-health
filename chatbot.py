from flask import Flask, render_template, request
from google import genai

API_KEY = "AIzaSyCNcfrc0dnhgr3k7d7HGqidw6OfsCBeAhQ"
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)


def format_spacing(text):
    """
    Ensures one blank line after every bullet point.
    """
    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        formatted_lines.append(line)
        if line.strip().startswith("•"):
            formatted_lines.append("")  # add blank line

    return "\n".join(formatted_lines)


def get_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if hasattr(response, "text") and response.text:
            return format_spacing(response.text.strip())

        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    return format_spacing(part.text.strip())

        return "• System anomaly. Unable to generate response."

    except Exception as e:
        print("GEMINI ERROR:", e)
        return "⚠️ AI core malfunction. Check server terminal."


@app.route('/')
def home():
    return render_template('chatbot.html')


@app.route('/ask', methods=['POST'])
def ask():
    msg1 = request.form.get('message1', '').strip()
    msg2 = request.form.get('message2', '').strip()
    msg3 = request.form.get('message3', '').strip()

    if not msg1:
        return "• Please provide symptom details for assessment."

    combined_message = f"""
    You are V.I.T.A.L., an advanced AI clinical assessment system.

    Act as an experienced AI medical assistant.
    Provide thorough, medically responsible explanations.

    Explain clearly:
    • What the condition is
    • Why symptoms match
    • What is happening in the body
    • Practical home management
    • Warning signs

    Avoid vague phrases.
    Avoid repetition.
    Do not overlap ideas.

    INPUT DATA:

    Symptoms:
    {msg1}

    Vitals:
    {msg2}

    Facial Indicators:
    {msg3}

    ---

    STRICT OUTPUT FORMAT:

    🧠 VITAL Assessment

    Most Likely Causes:
    • Condition name with brief explanation of mechanism.

    • Second possible condition with reasoning.

    Why It Matches:
    • Clear link between symptom and condition.

    • Supporting clinical reasoning.

    Home Remedies:
    • Specific remedy with explanation of benefit.

    • Additional care step and its purpose.

    Precautions:
    • What to avoid and why.

    • Warning symptoms requiring attention.

    Recommended Action:
    • Immediate next step with reasoning.

    • When medical consultation becomes necessary.

    System Status:
    • Choose ONE:
    🟢 System Stable – Home care appropriate
    🟡 Monitor Closely – Reassess in 24–48 hrs
    🔴 Medical Attention Recommended

    Rules:
    • Detailed but structured.
    • No paragraphs.
    • Bullet format only.
    • No unnecessary follow-up questions.
    • Only ask if critical data is missing.
    """

    reply = get_response(combined_message)
    return reply if reply else "• No response generated."


if __name__ == "__main__":
    app.run(debug=True)