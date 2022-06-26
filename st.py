import streamlit as st
import BP2

bp = BP2.BP_Updater()


# def onClickUpdate():
#     st.write('Values:', values)
#     bp.update(values[0], values[1])
page_type = st.radio(
     "Which sheet do you want to update?",
     ('Influencer', 'Business page'))

if page_type == 'Influencer':
     st.write('You selected Influencer.')
else:
     st.write("You selected Business page.")
st.write(page_type, '---')
@st.cache(suppress_st_warning=True)
def onClickUpdate():
    bp.update(starting_row, ending_row, st, page_type)
    
    st.write('Process Done!')

st.title('Database Updater')

starting_row = st.number_input('Insert starting row number', min_value=2, help='You need to enter starting row of your database table')
ending_row = st.number_input('Insert ending row number', min_value = starting_row + 1, max_value=10000)

# values = st.slider(
#      'Select a range',
#      2, 100, (2, 100), step=1)


updateButton = st.button('Update Date', on_click=onClickUpdate)
# st.write('Done!')
