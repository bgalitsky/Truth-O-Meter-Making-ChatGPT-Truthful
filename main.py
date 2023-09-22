import streamlit as st
import streamlit_theme as stt
from streamlit.report_thread import get_report_ctx
import streamlit_authenticator as stauth
import datetime
import json
import os
import truthometer
from truthometer.fact_checker_via_web import FactCheckerViaWeb


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'{f.read()}', unsafe_allow_html=True)


def main():
    ctx = get_report_ctx()
    st.set_page_config(layout='wide', page_title="Truth-o-meter")
#    local_css("visualization/highlight.css")

    stt.set_theme({'primary': '#EA6B4F'})
    st.set_option('deprecation.showfileUploaderEncoding', False)

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #EA6B4F; size=5;'>{}</h1>".format('Truth-O-Meter: MAKING ChatGPT TRUTHFUL'),
                unsafe_allow_html=True)

    st.markdown('Despite its capabilities, GPT-4 has similar limitations to earlier GPT models: it is not fully reliable (e.g. can suffer from “hallucinations”) : OpenAI (2023) https://cdn.openai.com/papers/gpt-4.pdf')
    st.markdown('This is a demo of a system that addresses this exact issue. It takes a text generated by GPT and verifies it against the web knowledge.')

    pad_text = """The deepest cave in the world is the "Veryovkina Cave" located in Abkhazia, Georgia, with a depth of 2,212 meters (7,257 feet). The expeditions to explore the cave have been led by the Ukrainian Speleological Association, with diver Gennadiy Samokhin leading the dives to reach the cave's lower depths"""
    input_text = st.text_area(label='Enter the text to verify and correct', value=pad_text)
    
    
    col_tool, _ = st.columns([0.1, 0.8])
    with col_tool:
        tool_selector = st.selectbox('Select the system', options=('Bing', 'Google Search'))

    col_group, _ = st.columns([0.3, 0.7])
    with col_group:
        with st.expander("Search options"):
            token_option = st.checkbox('Use the default token', value=True)
            token = st.text_input(label='Token:')
    st.write("")
    
    fact_checker = FactCheckerViaWeb()
    
    
    sess_id = ctx.session_id
    run = st.button('Check and correct')
    # st.markdown(sess_id)
    if tool_selector == "Bing":
        is_bing = True
    else:
        is_bing = False
    
    api_key = None
    if not token_option:
        api_key = token
    
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    if os.path.exists("counter_api{}.txt".format(date)):
        with open("counter_api{}.txt".format(date), "r") as f:
            cur = int(f.readlines()[0])
    else:
        cur = 0
    if cur < 50:
        cur += 1
        with open("counter_api{}.txt".format(date), "w") as f:
            f.write(str(cur))
    else:
        assert api_key is not None, "The maximum number of checks for the default token has been reached for today. Please provide another token."
    
    if run:
        html_report_filename = fact_checker.perform_and_report_fact_check_for_text(input_text, is_bing, api_key)
        #html_report_filename = "verification_page_Alexander_Pushk.html"
        with open(html_report_filename, "r") as f:
            st.markdown(f.read().split("<body>")[1].split("</body>")[0], unsafe_allow_html=True)
        
        
if __name__ == '__main__':
    main()
