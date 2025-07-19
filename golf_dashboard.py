import streamlit as st

st.set_page_config(page_title="Golf Cost Optimizer", layout="wide")
st.title("🏌️ Golf Expense & Practice Planner")

st.markdown("""
Welcome! This dashboard helps you estimate your monthly golf costs and practice quality,  
based on your rounds played, club membership, and practice preferences.  
Adjust the sliders and inputs in the sidebar to see your personalized results.
""")

# Sidebar Inputs
st.sidebar.header("🎯 Rounds per Month")
r9 = st.sidebar.slider(
    "9-hole rounds per month",
    0, 30, 4,
    help="Number of 9-hole rounds you typically play each month."
)
r18 = st.sidebar.slider(
    "18-hole rounds per month",
    0, 30, 0,
    help="Number of 18-hole rounds you typically play each month."
)

st.sidebar.header("🏌️ Course Selection")
course_9 = st.sidebar.selectbox(
    "Preferred club for 9-hole rounds",
    ["Hornung", "Bulawayo Country Club"],
    help="Choose where you usually play your 9-hole rounds."
)
course_18 = st.sidebar.selectbox(
    "Preferred club for 18-hole rounds",
    ["Hornung", "Bulawayo Country Club"],
    help="Choose where you usually play your 18-hole rounds."
)

st.sidebar.header("💳 BCC Membership")
bcc_membership = st.sidebar.radio(
    "Select your Bulawayo Country Club membership type",
    ["None", "Member ($35/mo)", "Prepaid ($75/mo)"],
    help=(
        "None: No membership, pay per round at BCC.\n"
        "Member: Pay $35 monthly + per round fees ($4 for 9 holes, $8 for 18 holes).\n"
        "Prepaid: Pay $75 monthly for unlimited rounds."
    )
)

st.sidebar.header("⛳ Practice Setup")
practice_sessions = st.sidebar.slider(
    "Driving range sessions per month",
    0, 30, 6,
    help="How many times you typically visit the driving range per month."
)
practice_location = st.sidebar.selectbox(
    "Practice location",
    ["TinCup", "Bulawayo Golf Club"],
    help=(
        "TinCup: $1 per 30 balls, no putting/chipping facilities.\n"
        "Bulawayo Golf Club: $5 per 100-ball bucket or $40 unlimited monthly plan, with short game facilities."
    )
)
practice_plan = None
if practice_location == "Bulawayo Golf Club":
    practice_plan = st.sidebar.radio(
        "Bulawayo GC practice plan",
        ["Pay per session ($5)", "Unlimited ($40/mo)"],
        help="Choose between paying per bucket or unlimited monthly access."
    )

st.sidebar.header("⚙️ Advanced Preferences")
budget = st.sidebar.number_input(
    "💰 Monthly budget cap ($)",
    min_value=0,
    value=80,
    help="The maximum amount you want to spend on golf and practice each month."
)

st.sidebar.markdown("**Weight your priorities (0–100):**\nAdjust to reflect what's most important to you.")
cost_weight = st.sidebar.slider(
    "Cost Savings",
    0, 100, 50,
    help="How important is keeping costs low when choosing golf options?"
)
practice_weight = st.sidebar.slider(
    "Practice Quality",
    0, 100, 30,
    help="How important is the quality and comprehensiveness of your practice sessions?"
)
experience_weight = st.sidebar.slider(
    "Full-Course Experience",
    0, 100, 20,
    help="How important is playing on a full-course (vs. just PAR 3 holes) for your enjoyment or skill?"
)

st.sidebar.header("🏌️ Practice Detail Priorities\n(Adjust to your training focus)")
full_swing = st.sidebar.slider(
    "Full Swing (Irons & Driver)",
    0, 100, 80,
    help="Importance of practicing full shots with irons and drivers."
)
ball_shape = st.sidebar.slider(
    "Ball Flight/Shot Shaping",
    0, 100, 70,
    help="Importance of practicing draws, fades, and controlling ball flight."
)
short_game = st.sidebar.slider(
    "Chipping/Pitching/Bunker",
    0, 100, 60,
    help="Importance of practicing your short game around the green."
)
putting = st.sidebar.slider(
    "Putting Practice",
    0, 100, 60,
    help="Importance of practicing putting skills."
)
ball_volume = st.sidebar.slider(
    "Ball Volume Preference",
    0, 100, 70,
    help="How many balls you prefer to hit per practice session."
)

# --- Cost Calculations ---
hornung_9_fee = 5
hornung_18_fee = 10
bcc_nonmember_9 = 8
bcc_nonmember_18 = 15
bcc_member_9 = 4
bcc_member_18 = 8
bcc_membership_fee = 35
bcc_prepaid_fee = 75

round_cost = 0
if course_9 == "Hornung":
    round_cost += r9 * hornung_9_fee
else:
    if bcc_membership == "None":
        round_cost += r9 * bcc_nonmember_9
    elif bcc_membership == "Member ($35/mo)":
        round_cost += r9 * bcc_member_9

if course_18 == "Hornung":
    round_cost += r18 * hornung_18_fee
else:
    if bcc_membership == "None":
        round_cost += r18 * bcc_nonmember_18
    elif bcc_membership == "Member ($35/mo)":
        round_cost += r18 * bcc_member_18

if bcc_membership == "Member ($35/mo)":
    round_cost += bcc_membership_fee
elif bcc_membership == "Prepaid ($75/mo)":
    round_cost += bcc_prepaid_fee

if practice_location == "TinCup":
    practice_cost = practice_sessions * 1
else:
    if practice_plan == "Pay per session ($5)":
        practice_cost = practice_sessions * 5
    else:
        practice_cost = 40

total_cost = round_cost + practice_cost

# --- Practice Quality Scoring ---
if practice_location == "TinCup":
    practice_score = 0.4 * full_swing + 0.5 * ball_volume
else:
    practice_score = 0.9 * full_swing + 0.8 * short_game + 0.8 * putting + 0.8 * ball_volume + 0.7 * ball_shape
practice_score = min(practice_score / 500 * 100, 100)

# --- Course Experience Scoring ---
if course_9 == "Bulawayo Country Club" or course_18 == "Bulawayo Country Club":
    experience_score = 100
else:
    experience_score = 40

# --- Weighted Overall Score (Scaled to 0-100) ---
weights_sum = cost_weight + practice_weight + experience_weight
if weights_sum == 0:
    overall_score = 0
else:
    raw_score = (
        cost_weight * (100 - min(total_cost, budget)) / 100 +
        practice_weight * practice_score / 100 +
        experience_weight * experience_score / 100
    )
    overall_score = raw_score / weights_sum * 100

# --- Display ---
st.subheader("📊 Summary")
st.markdown(f"**Estimated Monthly Cost:** ${total_cost:.2f}")
st.markdown(f"**Practice Quality Score:** {practice_score:.1f} / 100")
st.markdown(f"**Course Experience Score:** {experience_score} / 100")
st.markdown(f"**Weighted Overall Suitability Score:** {overall_score:.1f} / 100")

if total_cost > budget:
    st.warning("⚠️ Your estimated cost exceeds your monthly budget.")

st.caption("This weighted overall score combines your priorities and current choices to help you find the best balance between cost, practice quality, and course experience.")

# --- Practice suggestions based on practice detail priorities ---
max_practice_focus = max(full_swing, ball_shape, short_game, putting, ball_volume)
suggestions = []

# Suggest based on top priorities
if max_practice_focus in [full_swing, ball_shape]:
    suggestions.append("Focus on Bulawayo Golf Club for full swing and shot shaping practice.")
if max_practice_focus in [short_game, putting]:
    suggestions.append("Bulawayo Golf Club is recommended for short game and putting practice.")
if ball_volume >= 80 and practice_location == "Bulawayo Golf Club":
    if practice_plan == "Pay per session ($5)":
        suggestions.append("Consider upgrading to the Unlimited ($40/mo) plan for cost efficiency.")
elif practice_location == "TinCup":
    if max_practice_focus >= 70:
        suggestions.append("TinCup is economical but lacks short game facilities.")
    else:
        suggestions.append("TinCup is suitable for basic full swing practice on a budget.")

if not suggestions:
    suggestions.append("Your current practice setup matches your priorities well.")

st.subheader("💡 Practice Suggestions")
for s in suggestions:
    st.write("- " + s)
