import streamlit as st


def style_base_layout_home():

    st.markdown('''
    <style>
        .stApp{
        background:#97a7bf !important;
        }

        .stApp div[data-testid="stColumn"]{
            background: #E0E3FF !important;
            padding: 2rem !important;
            border-radius: 5rem !important;    
        }


    <style/>

''',unsafe_allow_html=True)

    
def style_base_layout_dashboard():

    st.markdown('''
    <style>
        .stApp{
        background:#97bfac !important;
        }


    <style/>

''',unsafe_allow_html=True)


    
def style_base_layout():

    st.markdown('''
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');


        /* hide top toolbar of streamlit */

        #MainMenu, footer, header  {visibility: hidden;}

        .block-container{
        padding-top: 1rem;
        }
        h1{
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3rem  !important;
            line-height: 1.2 !important;
            margin-bottom: 0rem !important;
        }
          
        h2{
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem  !important;
            line-height: 0.9 !important;
            margin-bottom: 0rem !important;
            color: #32343D !important;
        }
        h3, h4, p,{
            font-family: 'Outfit', sans-serif !important;
            color: #32343D !important;
        }

        button{
            border-radius: 0.5rem !important;
            background-color: #5865f2 !important;
            color: #fff !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            transition: transform 0.3s ease-in-out !important;
            } 

        button[kind="secondary"]{
            border-radius: 0.5rem !important;
            background-color: #73c7eb !important;
            color: #fff !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            transition: transform 0.3s ease-in-out !important;
            } 

        button[kind="tertiary"]{
            border-radius: 0.5rem !important;
            background-color: black !important;
            color: #fff !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            transition: transform 0.3s ease-in-out !important;
            } 
        
            button:hover{
            transform: scale(1.05) !important;
    <style/>

''',unsafe_allow_html=True)