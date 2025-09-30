import streamlit as st
import google.generativeai as genai
import random

st.markdown(
    """
    <style>
    /* Change main background */
    .stApp {
        background-color: #fff9c4; /* soft yellow */
    }

    /* Change sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #fff176; /* brighter yellow */
    }

    /* Change chat bubbles */
    .stChatMessage {
        background-color: #fffde7; /* very light yellow */
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

user_emoji = "streamlit_chatbot/chill.jpg"
robot_img = "streamlit_chatbot/duck2.jpg"

# Configure Gemini API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Sidebar persona controls
with st.sidebar:
            st.title("Quack Menu")
            mood = st.select_slider("Mr. Quack's Mood", options=["Very Sad", "Sad", "Okay", "Happy", "Very Happy"], value="Okay")
            mode = st.radio("Mode", ["Friendly", "Formal", "Funny"], index=0)
            topics = st.multiselect("Topics", ["Movies", "Travel", "Food", "Sports"], default=["Food"])
            page = st.radio("Go to:", ["Chat", "Mini Game", "Duck Quiz Game"])
            

if page == "Chat":

    def initialize_session_state():
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def get_gemini_response(persona, user_prompt):
        """
        Combine persona + user prompt so the chatbot always acts in character.
        """
        full_prompt = f"""
        You are Mr. Quack 🦆, a chatbot with this persona:
        {persona}

        Always stay in character as Mr. Quack when replying.
        User: {user_prompt}
        """
        response = model.generate_content(full_prompt)
        return response.text

    def build_persona(mode, topics, mood):
        """
        Create a persona string based on sidebar settings.
        """
        persona = f"Your tone is {mode.lower()}."
        if topics:
            persona += f" You enjoy talking about {', '.join(topics)}."
        persona += f" Your current mood is {mood.lower()}."
        return persona

    def main():
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image("streamlit_chatbot/duck-removebg-preview.png", width=100)
        with col2:
            st.title("Mr. Quack")

        initialize_session_state()

        # Build persona string
        persona = build_persona(mode, topics, mood)

        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar=robot_img):
                    st.write(f"{message['content']}")
            else:
                with st.chat_message("user", avatar=user_emoji):
                    st.write(f"{message['content']}")

        # Chat input
        if prompt := st.chat_input("Chat with Mr. Quack"):
            with st.chat_message("user", avatar=user_emoji):
                st.write(prompt)

            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get persona-based response
            response = get_gemini_response(persona, prompt)

            with st.chat_message("assistant", avatar=robot_img):
                st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
        
    main()

elif page == "Mini Game":

    def mini_game():
        st.header("🎲 Guess the Number Game")
        st.write("I'm thinking of a number between 1 and 20. Can you guess it?")

        if "secret_number" not in st.session_state:
            st.session_state.secret_number = random.randint(1, 20)
            st.session_state.attempts = 0

        guess = st.number_input("Enter your guess:", min_value=1, max_value=20, step=1)
        if st.button("Submit Guess"):
            st.session_state.attempts += 1
            if guess == st.session_state.secret_number:
                st.success(f"🎉 Correct! The number was {st.session_state.secret_number}. You guessed it in {st.session_state.attempts} attempts.")
                # Reset for a new game
                st.session_state.secret_number = random.randint(1, 20)
                st.session_state.attempts = 0
            elif guess < st.session_state.secret_number:
                st.warning("Too low! Try again.")
            else:
                st.warning("Too high! Try again.")

    mini_game()

elif page == "Duck Quiz Game":
    def duck_quiz():

        st.header("🦆 Duck Quiz Game")
        st.write("Test your duck knowledge with this fun quiz!")

        # --- Quiz data ---
        quiz = [
            {
                "question": "What do ducks have on their feet?",
                "options": ["Claws", "Webbed feet", "Hooves", "Scales"],
                "answer": "Webbed feet"
            },
            {
                "question": "What sound do ducks make?",
                "options": ["Moo", "Quack", "Baa", "Woof"],
                "answer": "Quack"
            },
            {
                "question": "Where do most ducks like to live?",
                "options": ["Deserts", "Lakes and rivers", "Mountains", "Caves"],
                "answer": "Lakes and rivers"
            },
            {
                "question": "What do ducks often eat?",
                "options": ["Grass and insects", "Metal", "Plastic", "Rocks"],
                "answer": "Grass and insects"
            }
        ]

        # --- Initialize session state (use unique keys to avoid collisions) ---
        if "duck_q_index" not in st.session_state:
            st.session_state.duck_q_index = 0
            st.session_state.duck_q_score = 0
            st.session_state.duck_q_answered = False  # whether current question was submitted
            st.session_state.duck_q_choice = None

        index = st.session_state.duck_q_index

        # --- If there are still questions left ---
        if index < len(quiz):
            q = quiz[index]
            st.subheader(f"Question {index + 1} / {len(quiz)}")
            st.write(q["question"])

            # show radio with a stable key per question so answer persists per question
            choice = st.radio("Choose an answer:", q["options"], key=f"duck_q_radio_{index}")

            # Submit button (only counts once per question)
            if st.button("Submit Answer", key=f"duck_q_submit_{index}") and not st.session_state.duck_q_answered:
                st.session_state.duck_q_answered = True
                st.session_state.duck_q_choice = choice

                if choice == q["answer"]:
                    st.session_state.duck_q_score += 1
                    st.success("✅ Correct!")
                else:
                    # <-- this will show the correct answer when the user's choice is wrong
                    st.error(f"❌ Oops! The correct answer was: **{q['answer']}**")

            # If already answered, show the chosen answer and give a Next button
            if st.session_state.duck_q_answered:
                st.write(f"**Your answer:** {st.session_state.duck_q_choice}")
                # Next button to move on
                if st.button("Next", key=f"duck_q_next_{index}"):
                    st.session_state.duck_q_index += 1
                    st.session_state.duck_q_answered = False
                    st.session_state.duck_q_choice = None
                    # rerun to show next question
                    st.rerun()
        else:
            # Quiz finished
            st.success(f"🎉 Quiz finished! Your score: {st.session_state.duck_q_score}/{len(quiz)}")
            if st.button("Play Again"):
                st.session_state.duck_q_index = 0
                st.session_state.duck_q_score = 0
                st.session_state.duck_q_answered = False
                st.session_state.duck_q_choice = None
                st.rerun()
    duck_quiz()

# if __name__ == "__main__":
#     main()



