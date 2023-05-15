import streamlit as st
import BP2

bp = BP2.BP_Updater()


# def onClickUpdate():
#     st.write('Values:', values)
#     bp.update(values[0], values[1])


# page_type = st.radio(
#      "Which sheet do you want to update?",
# #      ('Influencer', 'Business page'))
# page_type = st.sidebar.button('Influencer')
# page_type = st.sidebar.button('Business page')


     
st.title('Database Updater')


# values = st.slider(
#      'Select a range',
#      2, 100, (2, 100), step=1)


@st.cache(suppress_st_warning=True)
def onClickUpdate():
     bp.update(starting_row, ending_row, st, page_type)
#      st.sucess('Process Done!')

# st.write('Done!') 
with st.sidebar:
    page_type = st.sidebar.selectbox(
    "Which would you like to update?",
    ("Influencers", "Business Pages", "Telegram")
)
    st.write(page_type, 'is selected.')
    starting_row = st.number_input('Insert starting row number', min_value=0, help='You need to enter starting row of your database table')
    st.write('The starting row is: ', starting_row)
    
    ending_row = st.number_input('Insert ending row number', min_value = starting_row + 1, max_value=10000)
    st.write('The ending row is: ', ending_row)

    updateButton = st.button('Update Date', on_click=onClickUpdate)
if page_type == 'Influencers':
     st.subheader('Influencers')
     df = bp.get_data('Influencers')
     df.index = range(2, len(df) + 2)
     st.dataframe(df)
     
elif page_type == 'Business Pages':
     st.subheader("Business Pages.")
     df = bp.get_data('Business Pages')
     df.index = range(2, len(df) + 2)
     st.dataframe(df)
     
elif page_type == 'Telegram':
     st.subheader("Telegram.")
     df = bp.get_data('Telegram')
     df.index = range(2, len(df) + 2)
     st.dataframe(df)

