import streamlit as st
import openai
from dotenv import load_dotenv
import os
import json

#load environment viariable
load_dotenv()
#load API KEY
openai.api_key = os.environ.get("API_KEY")

#read existing json
def get_aidata():
    with open("./Questionnaire JSON/questionnaire_chatcmpl-7j2DpsP10z3gRn3DQVle0JHZ9clbd.json", 'r') as file:
        ai_response = json.load(file)
    return ai_response['questions'] 


#Questionnaire function setup
def create_questionnaire(context, q_num):
    q_prompt = f"Create {q_num} research questions on the topic: {context}. It must be JSON formatted with question and options to select."
    # This is the latest model that is available.
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
        # Notice how you need to specify the role of the user and system in the conversation. You need to ask for less questions at a time.
            {"role": "system", "content" : "You are the research questionnaire developer"},
            {"role": "user", "content" : q_prompt }
        ]
    )
    prompt_id    = response['id']
    created_date = response['created']
    # write the json returned by chat-gpt api to a .json file which will need futher clean-up.
    return response["choices"][0]["message"]["content"]



def display_question(question):
    question_type = question.get('question_type', 'text')
    question_text = question['question']
    options = question.get('options', [])

    st.write(f"**Question:** {question_text}")

    if question_type == 'multiple_choice':
        answer = st.radio("Choose one option:", options)
    elif question_type == 'likert_scale':
        answer = st.select_slider("Choose your response:",options=options)
    elif question_type == 'checkbox':
        answer = [st.checkbox (item) for item in options]
    elif question_type == 'dropdown':
        answer = st.selectbox("Select your option:", options)
    elif question_type == 'ranking':
        answer = st.multiselect("Select your option:", options, placeholder="Choose option base on rank")
    elif question_type == 'rating':
        answer = st.radio("Select your rating:", options, horizontal=True)
    else:
        answer = st.text_input("Your answer:")
        

    return answer


# APPLICATION
def main():

    st.header ("Create a Questionnaire")

    #Set up user input with sidebar
    user_input =  st.sidebar.text_area("Type your survey goal and let AI create your survey.\n\nType specifically what you want to know.",
                placeholder="I want to understand how likely people are to switch from gas to electricity",key="user_input_state")
    #create a generate button             
    generate_btn = st.sidebar.button("Generate")

    #Set up user input
    #user_input = st.text_input("Type your survey goal and let AI create your survey.\n\nType specifically what you want to know.",
    #              placeholder="I want to understand how likely people are to switch from gas to electricity")

 #set up a premium user checker
    if st.sidebar.checkbox("Premium User"):
        q_num = st.sidebar.number_input("Input number of questions",step=5, min_value=10)
    else :
        q_num = 7


 

    #get context from user
    if user_input is None:
        if generate_btn:
            #needs to write session state function
            st.sidebar.write("AI needs survey goal to create questionnaire")
    elif generate_btn:
            #context = user_input
#fetch AI data
        #questions = create_questionnaire(context,q_num)
        questions = get_aidata() 
        
        #create form for AI output
        with st.form(key='questionnaire_form'):
            for i, question in enumerate(questions, 1):
                st.subheader(f"Question {i}")
                user_answer = display_question(question)
                #st.write("Your answer:", user_answer)
                st.write("---")

            submitted = st.form_submit_button(label='Accept')

            if submitted:
                # Do something with the collected responses
                # For example, you can store the responses in a database or process them further.
                pass


if __name__ == "__main__":
    main()






    
    


# def form_callback():
#     st.write(st.session_state.my_slider)
#     st.write(st.session_state.my_checkbox)

