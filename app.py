from groq import Groq
import pandas as pd
import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="AI Email Reply Assistant",
    page_icon="📧",
    layout="wide"
)

# Title
st.title("📧 AI Email Reply Assistant")

st.markdown("""
Generate professional customer support replies using AI.
""")

# Gemini Client
client = Groq(
    api_key=st.secrets["API_KEY"]
)

# Mode selector
mode = st.radio(
    "Choose Mode",
    ["Single Message", "Bulk CSV Upload"]
)

# -----------------------------
# SINGLE MESSAGE MODE
# -----------------------------

if mode == "Single Message":

    customer_message = st.text_area(
        "Customer Message",
        height=200,
        placeholder="Type customer message here..."
    )

    tone = st.selectbox(
        "Select Tone",
        [
            "Professional",
            "Friendly",
            "Formal",
            "Apologetic"
        ]
    )

    if st.button("Generate Reply"):

        if customer_message.strip() == "":
            st.warning("Please enter a message.")

        else:

            prompt = f"""
            Write a {tone} customer support email reply.

            Customer message:
            {customer_message}

            Keep the response professional and concise.
            """

            with st.spinner("Generating reply..."):

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                reply = response.choices[0].message.content.strip()

            st.success("✅ Reply Generated!")

            st.subheader("📩 AI Reply")

            st.write(reply)

# -----------------------------
# BULK CSV MODE
# -----------------------------

else:

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.subheader("📄 Uploaded Data")

        st.dataframe(df)

        tone = st.selectbox(
            "Select Tone",
            [
                "Professional",
                "Friendly",
                "Formal",
                "Apologetic"
            ]
        )

        if st.button("Generate Bulk Replies"):

            replies = []

            with st.spinner("Generating replies..."):

                for message in df["message"]:

                    prompt = f"""
                    Write a {tone} customer support email reply.

                    Customer message:
                    {message}

                    Keep the response professional and concise.
                    """

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    reply = response.choices[0].message.content.strip()

                    replies.append(reply)
                    time.sleep(1)

            df["ai_reply"] = replies

            st.success("✅ Replies Generated!")

            st.subheader("📋 Results")

            st.dataframe(df)

            csv = df.to_csv(index=False)

            st.download_button(
                label="⬇ Download Replies",
                data=csv,
                file_name="generated_replies.csv",
                mime="text/csv"
            )