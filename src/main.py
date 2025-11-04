import streamlit as st
import time
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

# App Config
st.set_page_config(page_title="Math Adventures ", page_icon="🎲", layout="centered")

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.generator = PuzzleGenerator()
    st.session_state.tracker = PerformanceTracker()
    st.session_state.engine = AdaptiveEngine()
    st.session_state.current_difficulty = "easy"
    st.session_state.user = ""
    st.session_state.question = ""
    st.session_state.correct_answer = 0.0
    st.session_state.question_index = 0
    st.session_state.total_questions = 10
    st.session_state.in_progress = False

st.title(" Math Adventures: Adaptive Learning")
st.write("Welcome to the AI-powered math challenge! 🚀")

if not st.session_state.initialized:
    st.session_state.user = st.text_input(" Enter your name:")
    start_diff = st.selectbox("Choose starting difficulty:", ["Easy", "Medium", "Hard"])
    if st.button("Start Adventure ") and st.session_state.user.strip():
        st.session_state.initialized = True
        st.session_state.current_difficulty = start_diff.lower()
        st.session_state.in_progress = True
        st.rerun()

elif st.session_state.in_progress:
    st.markdown(f"###  Hi, {st.session_state.user}! Get ready to play!")
    st.write(f" Current Difficulty: **{st.session_state.current_difficulty.capitalize()}**")

    if st.session_state.question == "":
        q, ans = st.session_state.generator.generate_puzzle(st.session_state.current_difficulty)
        st.session_state.question = q
        st.session_state.correct_answer = ans
        st.session_state.tracker.start_timer()

    st.markdown(f"## {st.session_state.question}")
    user_input = st.text_input("Your answer:", key=f"answer_{st.session_state.question_index}")

    if st.button("Submit "):
        try:
            user_answer = float(user_input)
            response_time = st.session_state.tracker.stop_timer()
            correct = abs(user_answer - st.session_state.correct_answer) < 0.001

            st.session_state.tracker.log_attempt(
                user=st.session_state.user,
                difficulty=st.session_state.current_difficulty,
                question=st.session_state.question,
                user_answer=user_answer,
                correct_answer=st.session_state.correct_answer,
                correct=correct,
                response_time=response_time
            )

            if correct:
                st.success(f" Correct! Great job, {st.session_state.user}! ⏱️ {response_time}s")
            else:
                st.error(f" Oops! Correct answer was {st.session_state.correct_answer}. ⏱️ {response_time}s")

            st.session_state.question_index += 1
            st.session_state.question = ""  

            perf = st.session_state.tracker.summary()
            next_level = st.session_state.engine.update_level(st.session_state.user, perf)
            st.session_state.current_difficulty = next_level

            progress = st.session_state.question_index / st.session_state.total_questions
            st.progress(progress)

            if st.session_state.question_index >= st.session_state.total_questions:
                st.session_state.in_progress = False
                st.balloons()
                st.rerun()
            else:
                time.sleep(1)
                st.rerun()
        except ValueError:
            st.warning(" Please enter a valid number!")

else:
    st.header(" Session Summary")
    summary = st.session_state.tracker.summary()
    st.write(f"**Accuracy:** {summary['accuracy']}%")
    st.write(f"**Average Time:** {summary['avg_time']}s")
    st.write(f"**Questions Attempted:** {summary['total']}")
    next_level = st.session_state.engine.get_current_level(st.session_state.user)
    st.write(f"**Next Recommended Level:** {next_level.capitalize()} ")

    df = st.session_state.tracker.to_dataframe()
    st.dataframe(df)

    if not df.empty:
        st.subheader("Accuracy Trend Over Time")
        df["cumulative_accuracy"] = (df["correct"].cumsum() / (df.index + 1)) * 100
        st.line_chart(df["cumulative_accuracy"])


    if st.button("Save Results "):
        path = "data/sessions.csv"
        st.session_state.tracker.save_to_csv(path)
        st.success(" Session saved!")

    if st.button("Play Again "):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
