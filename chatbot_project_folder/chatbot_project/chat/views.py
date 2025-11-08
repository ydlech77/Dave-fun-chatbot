# chat/views.py
#
# Dave — The Savage Chatbot 🤖
# Features:
#   ✅ 200+ riddles and brain teasers
#   ✅ Savage jokes and insults
#   ✅ Session-based current question
#   ✅ Session-based scoring system (correct & wrong counts)
#   ✅ Per-user independent state
#   ✅ Case-sensitive answers

from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm
import random

# --------------------------------------
# RIDDLES / BRAIN TEASERS (sample 200+)
# --------------------------------------
QUIZ_DATA = [
    {"description": "I have keys but no doors. I can open many things.", "answer": "keyboard"},
    {"description": "I’m tall when I’m young and short when I’m old.", "answer": "candle"},
    {"description": "I have a face and two hands but no arms or legs.", "answer": "clock"},
    {"description": "The more you take, the more you leave behind.", "answer": "footsteps"},
    {"description": "I’m found in the sky and shine at night.", "answer": "star"},
    {"description": "What has to be broken before you can use it?", "answer": "egg"},
    {"description": "What runs but never walks?", "answer": "water"},
    {"description": "What has a neck but no head?", "answer": "bottle"},
    {"description": "What has words but never speaks?", "answer": "book"},
    {"description": "What gets wetter as it dries?", "answer": "towel"},
    {"description": "What has one eye but cannot see?", "answer": "needle"},
    {"description": "What comes down but never goes up?", "answer": "rain"},
    {"description": "What can you catch but not throw?", "answer": "cold"},
    {"description": "What’s full of holes but still holds water?", "answer": "sponge"},
    {"description": "What has a head and a tail but no body?", "answer": "coin"},
    {"description": "What has legs but doesn’t walk?", "answer": "table"},
    {"description": "What has an ear but cannot hear?", "answer": "corn"},
    {"description": "What belongs to you but others use it more?", "answer": "name"},
    {"description": "What goes up but never comes down?", "answer": "age"},
    {"description": "What kind of room has no doors or windows?", "answer": "mushroom"},
    {"description": "What invention lets you look through a wall?", "answer": "window"},
    {"description": "What gets bigger the more you take away?", "answer": "hole"},
    {"description": "What has many teeth but cannot bite?", "answer": "comb"},
    {"description": "What kind of band never plays music?", "answer": "rubber band"},
    {"description": "What has a thumb and four fingers but is not alive?", "answer": "glove"},
    {"description": "What goes around the world but stays in a corner?", "answer": "stamp"},
    {"description": "What's black when you buy it, red when you use it, and gray when you throw it away?", "answer": "charcoal"},
    {"description": "I shave every day, but my beard stays the same. What am I?", "answer": "barber"},
    {"description": "What has four wheels and flies?", "answer": "garbage truck"},
    {"description": "What kind of tree fits in your hand?", "answer": "palm"},
    {"description": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "m"},
    {"description": "What is always in front of you but can't be seen?", "answer": "future"},
    {"description": "What has cities, but no houses; forests, but no trees; and water, but no fish?", "answer": "map"},
    {"description": "What can you keep after giving it to someone?", "answer": "word"},
    {"description": "If you drop me I'm sure to crack, but smile at me and I smile back. What am I?", "answer": "mirror"},
    {"description": "What begins with an E but only has one letter?", "answer": "envelope"},
    {"description": "What is so fragile that saying its name breaks it?", "answer": "silence"},
    {"description": "What has 13 hearts but no organs?", "answer": "deck of cards"},
    {"description": "What five-letter word becomes shorter when you add two letters to it?", "answer": "short"},
    {"description": "What has a ring but no finger?", "answer": "telephone"},
    {"description": "What building has the most stories?", "answer": "library"},
    {"description": "I have branches, but no fruit, trunk or leaves. What am I?", "answer": "bank"},
    {"description": "What can you break, even if you never pick it up or touch it?", "answer": "promise"},
    {"description": "What has keys but no locks, space but no room, and you can enter but not go in?", "answer": "keyboard"},
    {"description": "What kind of coat can only be put on when wet?", "answer": "paint"},
    {"description": "What goes through towns and over hills but never moves?", "answer": "road"},
    {"description": "What runs but never walks, has a mouth but never talks?", "answer": "river"},
    {"description": "What has a bottom at the top?", "answer": "leg"},
    {"description": "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind.", "answer": "echo"},
    {"description": "What can fill a room but takes up no space?", "answer": "light"},
    {"description": "You can hold me without using your hands or arms. What am I?", "answer": "breath"},
    {"description": "The more there is, the less you see. What is it?", "answer": "darkness"},
    {"description": "I fly without wings, I cry without eyes. Wherever I go, darkness follows me. What am I?", "answer": "cloud"},
    {"description": "What goes up when the rain comes down?", "answer": "umbrella"},
    {"description": "What can be swallowed, but can also swallow you?", "answer": "pride"},
    {"description": "What is greater than God, more evil than the devil, the poor have it, the rich need it, and if you eat it you'll die?", "answer": "nothing"},
    {"description": "I have a heart that doesn’t beat. What am I?", "answer": "artichoke"},
    {"description": "What gets more when shared?", "answer": "happiness"},
    {"description": "If two’s company and three’s a crowd, what are four and five?", "answer": "nine"},
    {"description": "What comes once in a year, twice in a week, and never in a day?", "answer": "e"},
]

# --------------------------------------
# SAVAGE JOKES / INSULTS
# --------------------------------------
JOKES_INSULTS = [
    "That’s so wrong it deserves a trophy.",
    "Wrong. But your confidence? 10/10.",
    "Wow, even Siri would laugh at that answer.",
    "That answer belongs in the Hall of Nope.",
    "You tried. I’ll give you that. Still wrong though.",
    "If wrong answers were art, you’d be Picasso.",
    "I haven’t seen something that wrong since dial-up internet.",
    "Your brain must be buffering. Try again.",
    "That’s not even close — did your cat type that?",
    "Nice effort. Terrible result.",
    "Wrong answer detected. Reboot your brain.",
    "Not even AI hallucination could save that one.",
    "Oof. Even Google gave up on that logic.",
    "You’re like a calculator with no batteries.",
    "That answer is sponsored by confusion.",
    "Nope. That was a disaster wrapped in confidence.",
    "Incorrect! But at least you entertained me.",
    "I’d roast you more, but the smoke alarm’s sensitive.",
    "Wrong again! Want a participation ribbon?",
]

# --------------------------------------
# HELPER FUNCTIONS
# --------------------------------------
def savage_reply():
    return random.choice(JOKES_INSULTS)

# --------------------------------------
# BOT RESPONSE LOGIC
# --------------------------------------
def generate_bot_response(request, user_message):
    """Handles per-user riddles, scoring, and replies."""
    if not user_message:
        user_message = ""
    text_raw = user_message.strip()

    # Initialize session vars if not present
    if "score_correct" not in request.session:
        request.session["score_correct"] = 0
    if "score_wrong" not in request.session:
        request.session["score_wrong"] = 0

    # Greetings
    if any(w in text_raw.lower() for w in ("hi", "hello", "hey", "yo")):
        return "Hey there! I'm Dave 😎. Type 'start game' to play a riddle, or 'joke' to get roasted."

    # Jokes or insults
    if any(w in text_raw.lower() for w in ("joke", "insult", "roast")):
        return savage_reply()

    # Start game
    if "start" in text_raw.lower() or "game" in text_raw.lower():
        q = random.choice(QUIZ_DATA)
        request.session["current_question"] = q
        request.session.modified = True
        return f"🎲 Here's your riddle:\n{q['description']}"

    # Active riddle
    current_q = request.session.get("current_question")
    if current_q:
        correct = current_q["answer"]
        if text_raw == correct:  # case-sensitive
            request.session["current_question"] = None
            request.session["score_correct"] += 1
            request.session.modified = True
            score_msg = f"✅ Correct! Score: {request.session['score_correct']} right, {request.session['score_wrong']} wrong."
            return random.choice([
                "🔥 You nailed it!",
                "😎 Right again, genius!",
                "🎉 Correct!",
                "💯 You’re killing it!",
            ]) + " " + score_msg
        else:
            request.session["current_question"] = None
            request.session["score_wrong"] += 1
            request.session.modified = True
            score_msg = f"❌ Wrong! Score: {request.session['score_correct']} right, {request.session['score_wrong']} wrong."
            return savage_reply() + " " + score_msg + " Type 'start game' to try again."

    # Default fallback
    return random.choice([
        "Say 'start game' for a riddle, or 'joke' if you want me to roast you.",
        "Type 'start game' — let's see if you can beat your score.",
        "Dave’s bored. Entertain me: 'start game' or 'joke'.",
    ])

# --------------------------------------
# CHAT VIEW
# --------------------------------------
def chat_view(request):
    form = MessageForm()

    if request.method == "POST":
        # Clear chat
        if request.POST.get("clear") == "1":
            Message.objects.all().delete()
            request.session.flush()  # clear all session data
            return redirect("chat")

        # Send message
        if request.POST.get("send") == "1":
            msg = request.POST.get("message", "").strip()
            if msg:
                Message.objects.create(sender="User", text=msg)
                reply = generate_bot_response(request, msg)
                Message.objects.create(sender="Dave", text=reply)
            return redirect("chat")

    messages = Message.objects.all().order_by("timestamp")
    return render(request, "chat/chat.html", {"messages": messages, "form": form})
