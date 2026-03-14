from flask import Flask, render_template, request
from google import genai

API_KEY = "AIzaSyACoyOjDgYdXn2zPMhgJfGap5jUcTFlKyA"

client = genai.Client(api_key=API_KEY)

app = Flask(__name__)


def format_response(text):

    lines = text.split("\n")
    formatted = []

    for line in lines:

        line = line.strip()

        if line.startswith("•") or line.startswith("-"):
            formatted.append(line)
            formatted.append("")  # blank line after bullet

        else:
            formatted.append(line)

    return "\n".join(formatted)


def get_response(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if response.text:
            text = response.text.strip()
            return format_response(text)

        return "• Unable to generate response."

    except Exception as e:
        print(e)
        return "• AI system error."


@app.route("/")
def home():
    return render_template("chatbot.html")


@app.route("/ask", methods=["POST"])
def ask():

    msg1 = request.form.get("message1")
    msg2 = request.form.get("message2")
    msg3 = request.form.get("message3")

    sleep_hours = request.form.get("sleep_hours")
    sleep_quality = request.form.get("sleep_quality")
    wake_refreshed = request.form.get("wake_refreshed")

    exercise_freq = request.form.get("exercise_freq")
    exercise_type = request.form.get("exercise_type")

    diet_type = request.form.get("diet_type")
    processed_food = request.form.get("processed_food")

    alcohol = request.form.get("alcohol")
    smoking = request.form.get("smoking")
    caffeine = request.form.get("caffeine")

    prompt = f"""

You are V.I.T.A.L, an advanced AI clinical health assistant.

Analyze symptoms and lifestyle factors.

Symptoms:
{msg1}

Vitals:
{msg2}

Facial Indicators:
{msg3}

Sleep:
Average hours: {sleep_hours}
Sleep quality: {sleep_quality}
Wake refreshed: {wake_refreshed}

Exercise:
Frequency: {exercise_freq}
Type: {exercise_type}

Diet:
Diet type: {diet_type}
Ultra processed food: {processed_food}

Substances:
Alcohol: {alcohol}
Smoking: {smoking}
Caffeine: {caffeine}

Respond strictly in bullet points.

FORMAT RULES:
• Every statement must begin with "•"
• One idea per bullet
• No paragraphs
• Leave one blank line after each bullet

Explain:

• Most likely causes
• Why symptoms match
• Lifestyle impact
• Home remedies
• Precautions
• When medical help is required

"""

    reply = get_response(prompt)

    return reply


if __name__ == "__main__":
    app.run(debug=True)