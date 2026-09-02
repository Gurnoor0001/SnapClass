import streamlit as st


def style_base_layout_home():

    st.markdown('''
    <style>
        .stApp{
            background: linear-gradient(135deg, #0F1123 0%, #1A1B3A 50%, #0F1123 100%) !important;
        }

        .stApp div[data-testid="stColumn"]{
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px) !important;
            padding: 2rem !important;
            border-radius: 1.5rem !important;
            border: 1px solid rgba(108, 99, 255, 0.15) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        }

    </style>

''',unsafe_allow_html=True)

    
def style_base_layout_dashboard():

    st.markdown('''
    <style>
        .stApp{
            background: linear-gradient(135deg, #0F1123 0%, #1A1B3A 50%, #0F1123 100%) !important;
        }

        .stApp div[data-testid="stColumn"]{
            background: transparent !important;
            padding: 2rem !important;
            border-radius: 1.5rem !important;    
        }

        /* Reduce gap between elements */
        .stElementContainer, .stVerticalBlock {
            gap: 0rem !important;
        }

        div[data-testid="stHeader"] ~ div .block-container > div > div {
            gap: 0rem !important;
        }
        
    </style>

''',unsafe_allow_html=True)


    
def style_base_layout():

    st.markdown('''
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined');


        /* hide top toolbar of streamlit */

        #MainMenu, footer, header  {visibility: hidden;}

        .block-container{
            padding-top: 1rem;
        }

        /* ── Typography ── */
        h1{
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3rem  !important;
            line-height: 1.2 !important;
            margin-bottom: 0rem !important;
            color: #E8E6F0 !important;
        }
          
        h2{
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem  !important;
            line-height: 0.9 !important;
            margin-bottom: 0rem !important;
            color: #C8C5D6 !important;
        }

        h2.header-title{
            color: #6C63FF !important;
        }

        h3, h4, p, label, span:not([data-testid="stIconMaterial"]){
            font-family: 'Outfit', sans-serif !important;
            color: #B0ADCC !important;
        }

        /* Ensure Material icons render as glyphs, not text */
        span[data-testid="stIconMaterial"] {
            font-family: 'Material Symbols Outlined' !important;
            font-size: 1.25rem !important;
            font-variation-settings: 'FILL' 1 !important;
        }

        /* ── Text Input Fields ── */
        div[data-testid="stTextInput"] label{
            color: #8B87A8 !important;
            font-size: 0.85rem !important;
            font-weight: 400 !important;
            letter-spacing: 0.03em !important;
        }

        div[data-testid="stTextInput"] input{
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid rgba(108, 99, 255, 0.25) !important;
            border-radius: 0.75rem !important;
            color: #E8E6F0 !important;
            padding: 0.75rem 1rem !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
        }

        div[data-testid="stTextInput"] input:focus{
            border-color: #6C63FF !important;
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.2), 0 0 20px rgba(108, 99, 255, 0.1) !important;
            background: rgba(255, 255, 255, 0.08) !important;
            outline: none !important;
        }

        div[data-testid="stTextInput"] input::placeholder{
            color: #5A577A !important;
            opacity: 1 !important;
        }

        /* ── Password toggle button inside input ── */
        div[data-testid="stTextInput"] button{
            background: rgba(108, 99, 255, 0.15) !important;
            border: 1px solid rgba(108, 99, 255, 0.3) !important;
            border-radius: 0.5rem !important;
            color: #6C63FF !important;
            padding: 0.3rem 0.5rem !important;
            box-shadow: none !important;
            font-size: 0 !important;
        }

        div[data-testid="stTextInput"] button span{
            font-family: 'Material Symbols Outlined' !important;
            font-size: 1.25rem !important;
            color: #8B87C8 !important;
        }

        div[data-testid="stTextInput"] button:hover{
            background: rgba(108, 99, 255, 0.3) !important;
            transform: none !important;
        }

        /* ── Primary Buttons ── */
        button{
            border-radius: 0.75rem !important;
            background: linear-gradient(135deg, #6C63FF 0%, #5A4FE8 100%) !important;
            color: #FFFFFF !important;
            padding: 0.6rem 1.4rem !important;
            border: none !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
        } 

        button:hover{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 25px rgba(108, 99, 255, 0.45) !important;
            background: linear-gradient(135deg, #7B73FF 0%, #6C63FF 100%) !important;
        }

        button[kind="secondary"]{
            border-radius: 0.75rem !important;
            background: rgba(108, 99, 255, 0.12) !important;
            color: #B0ADCC !important;
            padding: 0.6rem 1.4rem !important;
            border: 1px solid rgba(108, 99, 255, 0.35) !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: none !important;
        } 

        button[kind="secondary"]:hover{
            transform: translateY(-2px) !important;
            background: rgba(108, 99, 255, 0.25) !important;
            border-color: #6C63FF !important;
            color: #E8E6F0 !important;
            box-shadow: 0 4px 20px rgba(108, 99, 255, 0.25) !important;
        }

        button[kind="tertiary"]{
            border-radius: 0.75rem !important;
            background: rgba(255, 255, 255, 0.08) !important;
            color: #C8C5D6 !important;
            padding: 0.6rem 1.4rem !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: none !important;
        } 

        button[kind="tertiary"]:hover{
            transform: translateY(-2px) !important;
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(108, 99, 255, 0.4) !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0F1123;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(108, 99, 255, 0.4);
            border-radius: 3px;
        }

    </style>

''',unsafe_allow_html=True)