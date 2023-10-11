import openai
import streamlit as st
import streamlit.components.v1 as components
from streamlit_chat import message
import requests
import random

# Setting page title and header
st.set_page_config(page_title="DropRead", page_icon=":robot_face:")

header = st.container()
header.title("DropRead")
header.write("""<div class='fixed-header' style='text-align: center'/>""", unsafe_allow_html=True)
# Custom CSS for the sticky header
st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            z-index: 999;
        }
        
        .fixed - header {
        border - bottom: 1px solid black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Set org ID and API key
openai.api_key = "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"

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Users")
userSelector = st.sidebar.selectbox("Select a user:", (
"User 1", "User 2", "User 3", "User 4", "User 5", "User 6", "User 7", "User 8", "User 9", "User 10"))

# Given the user selector, get user id
userid = int(userSelector.split(" ")[1]) - 1

shouldUpdate = False

# Initialise session state variables
if 'userid' not in st.session_state or userid != st.session_state['userid']:
    shouldUpdate = True
if 'generated' not in st.session_state or userid != st.session_state['userid']:
    st.session_state['generated'] = []
if 'past' not in st.session_state or userid != st.session_state['userid']:
    st.session_state['past'] = []
if 'messages' not in st.session_state or userid != st.session_state['userid']:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant for a class. Help students with their questions."}
    ]
if 'model_name' not in st.session_state or userid != st.session_state['userid']:
    st.session_state['model_name'] = []
if 'conversation_id' not in st.session_state or userid != st.session_state['userid']:
    st.session_state['conversation_id'] = -1

if shouldUpdate:
    st.session_state['userid'] = userid
    # Send request to server to get conversations
    userReq = requests.get(f"http://127.0.0.1:5000/api/data/user/{userid}")
    user = userReq.json()

    # Get the conversation ids
    conversations = user["conversations"]

    # Overwrite conversation history with those
    st.session_state['generated'] = []
    st.session_state['past'] = []
    for conversation_id in conversations[:1]:
        # Update conversation id
        st.session_state['conversation_id'] = conversation_id
        conversationReq = requests.get(f"http://127.0.0.1:5000/api/data/conversation/{conversation_id}")

        # Get the conversation object
        conversation = conversationReq.json()

        # Append all past messages
        for i, msg in enumerate(conversation["usermessages"]):
            # Add to session state
            st.session_state['past'].append(msg["message"])
            st.session_state['generated'].append(conversation["botmessages"][i]["message"])

            # Add to chat history
            st.session_state['messages'].append({"role": "user", "content": msg["message"]})
            st.session_state['messages'].append(
                {"role": "assistant", "content": conversation["botmessages"][i]["message"]})

model_name = "GPT-3.5"
model = "gpt-3.5-turbo"


# generate a response; this part is easy
def generate_response(prompt):
    # Add the user's input to the chat history
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # Get the conversation id; will ignore if it's -1
    conversation_id = st.session_state['conversation_id']

    # Send request to server to get conversations
    reqJson = {"message": prompt, "userid": st.session_state['userid']}
    if conversation_id != -1:
        reqJson["conversation_id"] = conversation_id
    sendReq = requests.post("http://127.0.0.1:5000/api/conversation/send", json=reqJson)

    st.session_state['messages'].append({"role": "assistant", "content": sendReq.json()["response"]})
    st.session_state['conversation_id'] = sendReq.json()["conversation_id"]

    return sendReq.json()["response"]


# container for chat history
response_container = st.container()
# container for text box
container = st.container()
container.write("""<div class='fixed-footer'/>""", unsafe_allow_html=True)
### Custom CSS for the sticky header
st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-footer) {
            position: fixed;
            bottom: 50px;
            max-width: 700px;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)  # position: fixed; text-align: center;

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(user_input)
        # The following states need to be loaded to and synced with mongodb
        # The past session state is where we store the user's input
        st.session_state['past'].append(user_input)
        # The generated session state is where we store the model's output
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)

        # Add to chat history
        st.session_state['messages'].append({"role": "user", "content": user_input})
        st.session_state['messages'].append({"role": "assistant", "content": output})

        # Add to chat UI
        conversation_id = st.session_state['conversation_id']

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

js = f"""
    <script>
        function scroll(dummy_var_to_force_repeat_execution){{
            var textAreas = parent.document.querySelectorAll('section.main');
            for (let index = 0; index < textAreas.length; index++) {{
                textAreas[index].style.color = 'red'
                textAreas[index].scrollTop = textAreas[index].scrollHeight;
            }}
        }}
        scroll({len(st.session_state['generated'])})
        console.log("We scrolled here");
    </script>
"""

components.html(js)

style_stuff = """
        <style>
            body {box-sizing: border-box; margin: 0;}
            *, html {scroll-behavior: smooth !important;}
            @media print {
                [data-testid="stSidebar"] {display: none !important;}
                div#root div.css-1meupwp {display: block !important;}
            }
        </style>
        """
st.markdown(style_stuff, unsafe_allow_html=True)
