import streamlit as st
import pandas as pd
import numpy as np
import BP2

bp = BP2.BP_Updater()


def onClickUpdate():
    st.write('Values:', values)
    bp.update(values[0], values[1])

st.title('Macaan')

values = st.slider(
     'Select a range',
     2, 100, (2, 100), step=1)


updateButton = st.button('Update', on_click=onClickUpdate)