import streamlit as st

st.set_page_config(layout='wide')

st.title('Spotify Data Analysis')
st.subheader('About this App')

st.markdown("""
This app performs simple data analysis on the ***Spotify*** dataset.
* **Python libraries:**
    - pandas
    - streamlit
    - numpy
    - matplotlib
    - seaborn
* **Data source:** [Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
<img src= "https://mir-s3-cdn-cf.behance.net/project_modules/1400_opt_1/840361120717875.60b74ae5b9f13.gif">
""", unsafe_allow_html= True)