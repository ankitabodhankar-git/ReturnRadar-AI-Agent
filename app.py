import streamlit as st

st.set_page_config(
    page_title="ReturnRadar | Moolchand Store",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 ReturnRadar")
st.subheader("Moolchand Store — Return & Exchange Assistant")

st.write(
    "Ask questions about returns, exchanges, bills, tags, "
    "defective items, and store policy."
)

# Create a unique chat session
if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# Create ADK runner
if "runner" not in st.session_state:
    from google.adk.runners import InMemoryRunner
    from agent import app

    st.session_state.runner = InMemoryRunner(app=app)

# Store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm ReturnRadar 👋 "
                "I can help you understand Moolchand Store's "
                "return and exchange policy. What would you like to know?"
            )
        }
    ]

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Customer input
if prompt := st.chat_input(
    "Example: Can I exchange clothes bought 10 days ago?"
):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("assistant"):
        try:
            import asyncio

            async def fetch_response():
                return await st.session_state.runner.run_debug(
                    prompt,
                    session_id=st.session_state.session_id
                )

            res_events = asyncio.run(fetch_response())

            response_text = "".join([
                part.text
                for event in res_events
                if event.content and event.content.parts
                for part in event.content.parts
                if part.text
            ])

            st.markdown(response_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })

        except Exception as e:
            st.error(f"Sorry, an error occurred: {e}")