import streamlit as st
import pandas as pd
import numpy as np
import geemap.foliumap as geemap


st.title("Geo App Demo")

m = geemap.Map(center=[50.126, 8.707], zoom=18)
m.to_streamlit(height=600)