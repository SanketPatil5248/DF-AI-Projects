# Import required libraries
# streamlit -> used to build the web app UI
# genai -> used to connect with Google's Gemini AI
import streamlit as st
from google import genai


# ---------------- CONFIG ----------------
# This sets up the basic page settings of the web app
st.set_page_config(
    page_title="AI Code Reviewer",   # Title shown in browser tab
    page_icon="💻",                  # Icon in browser tab
    layout="wide"                   # Makes the layout use full screen width
)


# ---------------- API KEY ----------------
# We need an API key to connect to Gemini AI securely
# Streamlit stores secrets safely in st.secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]  # Try to get API key
except:
    # If key is missing, show error and stop app
    st.error("❌ API Key not found in Streamlit secrets.")
    st.stop()  # Stops execution so app doesn't crash later


# Initialize Gemini client using the API key
# This client will be used to send requests to AI
client = genai.Client(api_key=api_key)


# ---------------- UI ----------------
# Title and description shown on the app
st.title("💻 AI Code Reviewer")
st.write("Analyze, improve, and fix your code using Gemini 2.0 🚀")


# Dropdown for selecting programming language
# This helps AI give better, language-specific suggestions
language = st.selectbox(
    "Select Programming Language",
    ["Python", "JavaScript", "Java", "C++", "Other"]
)


# Text area where user pastes their code
code_input = st.text_area(
    "Paste your code here:",
    height=300,  # Controls size of input box
    placeholder="Write or paste your code here..."
)


# Create two columns (side-by-side buttons)
# This improves UI layout
col1, col2 = st.columns(2)


# ---------------- REVIEW CODE ----------------
# Button for reviewing code
if col1.button("🔍 Review Code"):

    # Check if user entered anything
    if code_input.strip() == "":
        st.warning("⚠️ Please enter code!")  # Show warning if empty
    else:
        # Show loading spinner while AI is working
        with st.spinner("Analyzing code..."):
            try:
                # Prompt sent to AI
                # We clearly tell AI WHAT to do and HOW to format output
                prompt = f"""
You are an expert {language} developer.

Review the code and respond in this format:

### 🐞 Bugs
- List issues clearly

### ⚡ Improvements
- Suggestions to improve code

### ✅ Best Practices
- Industry standards and tips

### 🚀 Optimized Code
Provide an improved version of the code

Code:
{code_input}
"""

                # Send request to Gemini AI model
                response = client.models.generate_content(
                    model="gemini-2.0-flash",  # Fast and efficient model
                    contents=prompt
                )

                # Extract text response from AI
                output = response.text

                # Display formatted output in app
                st.markdown(output)

                # Save output so user can download later
                st.session_state["review"] = output

            except Exception as e:
                # Handle errors (like API issues)
                st.error(f"❌ Error: {e}")


# ---------------- FIX CODE ----------------
# Button for automatically fixing code
if col2.button("⚡ Fix Code"):

    # Check if user entered anything
    if code_input.strip() == "":
        st.warning("⚠️ Please enter code!")
    else:
        # Show loading spinner while AI is working
        with st.spinner("Fixing code..."):
            try:
                # Prompt telling AI to only return corrected code
                prompt = f"""
You are an expert {language} developer.

Fix the following code and return ONLY the corrected version.

Code:
{code_input}
"""

                # Send request to Gemini AI
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                # Display fixed code with syntax highlighting
                st.subheader("✅ Fixed Code")
                st.code(response.text, language=language.lower())

            except Exception as e:
                # Handle errors
                st.error(f"❌ Error: {e}")


# ---------------- DOWNLOAD ----------------
# This allows user to download the review result
# session_state is used to store data across interactions
if "review" in st.session_state:
    st.download_button(
        label="📥 Download Review",
        data=st.session_state["review"],  # The saved AI response
        file_name="code_review.txt",      # File name for download
        mime="text/plain"
    )


# ---------------- FOOTER ----------------
# A simple footer for credits
st.markdown("---")
st.caption("Developed using the Streamlit framework and Gemini 2.0 Flash API")