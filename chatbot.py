from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import json
import os

# ===== CONFIG =====
API_KEY = os.environ.get("AIzaSyBVEgdRtjij2Hh7XDpnP2vgN08357Cn2DU")  # use env variable for safety
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-3-flash-preview")

app = Flask(__name__)
DATA_FILE = "users.json"

# ===== LOAD USERS =====
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# ===== SAVE USERS =====
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ===== FORMAT RESPONSE =====
def format_response(text):
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()
        if line.startswith("•"):
            formatted.append(line)
            formatted.append("")  # blank line after bullet
        else:
            formatted.append(line)

    return "\n".join(formatted)

# ===== AI RESPONSE =====
def get_response(prompt):
    try:
        response = model.generate_content(prompt)

        if response.text:
            return format_response(response.text.strip())

        return "• No response generated."

    except Exception as e:
        print("ERROR:", e)
        return "⚠️ AI core malfunction."

# ===== LOGIN =====
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        name = request.form.get("name")
        country = request.form.get("country").lower()

        heart = request.form.get("q1")
        diabetes = request.form.get("q2")
        bp = request.form.get("q3")
        respiratory = request.form.get("q4")
        stress = request.form.get("q5")
        custom = request.form.get("custom_issue")

        history = f"""
Country: {country}

Heart Disease: {heart}
Diabetes: {diabetes}
High Blood Pressure: {bp}
Respiratory Issues: {respiratory}
Stress/Anxiety: {stress}

Other Issues: {custom if custom else "None"}
"""

        users = load_users()

        users[name] = {
            "history": history.strip(),
            "country": country,
            "chats": []
        }

        save_users(users)

        return redirect(url_for("dashboard", username=name))

    return render_template("login.html")

# ===== DASHBOARD =====
@app.route("/dashboard/<username>")
def dashboard(username):

    users = load_users()
    user = users.get(username, {})

    history = user.get("history", "")
    chats = user.get("chats", [])

    return render_template(
        "dashboard.html",
        username=username,
        history=history,
        chats=chats
    )

# ===== CHAT PAGE =====
@app.route("/chat/<username>")
def chat(username):
    return render_template("chatbot.html", username=username)

# ===== ASK =====
@app.route("/ask/<username>", methods=["POST"])
def ask(username):

    users = load_users()
    user = users.get(username, {})

    history = user.get("history", "")
    country = user.get("country", "india")

    msg1 = request.form.get("message1", "").strip()
    msg2 = request.form.get("message2", "").strip()
    msg3 = request.form.get("message3", "").strip()

    if not msg1:
        return "• Please provide symptom details."

    emergency_numbers = {
        "india": "112",
        "usa": "911",
        "uk": "999",
        "canada": "911",
        "australia": "000"
    }

    ambulance = emergency_numbers.get(country, "local emergency number")

    prompt = f"""
You are V.I.T.A.L., an advanced AI medical assistant.

User Background:
{history}

Symptoms:
{msg1}

Vitals:
{msg2}

Facial Indicators:
{msg3}

---

🧠 VITAL Assessment

Most Likely Causes:
• Cause with explanation

• Second possible cause

Why It Matches:
• Reason

• Supporting logic

Home Remedies:
• Remedy with benefit

• Additional step

Precautions:
• Avoid actions

• Warning signs

Recommended Action:
• Next step

• When to seek help

System Status:
• Choose ONE:
🟢 Stable
🟡 Monitor
🔴 Medical Emergency

IMPORTANT:
If 🔴:
• Say SEEK IMMEDIATE HELP
• Ambulance: {ambulance}

Rules:
• Bullet format only
• One blank line after each bullet
• No paragraphs
"""

    reply = get_response(prompt)

    if username in users:
        users[username]["chats"].append({
            "user": f"{msg1} | {msg2} | {msg3}",
            "ai": reply
        })
        save_users(users)

    return reply

# ===== RUN =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)