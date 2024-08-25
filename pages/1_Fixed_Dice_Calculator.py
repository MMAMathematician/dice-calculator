import streamlit as st
import numpy as np
from common.common import *

st.set_page_config(page_title="Fixed Dice Calculator")
st.title("Fixed Dice Calculator")

with st.sidebar:
    die_skill = st.selectbox('Size of Skill Die', [4, 6, 8, 10, 12, 20])
    die_tool = st.selectbox('Size of Tool Die', [0, 4, 6, 8, 10, 12, 20])
    die_assist = st.selectbox('Size of Assist Die', [0, 4, 6, 8, 10, 12, 20])
    num_assist = st.number_input("Number of Assist Dice", value=1)
    mod_base = st.slider('Base Modifier', max_value=20)
    mod_bonus = st.slider('Bonus Modifier', max_value=20)
    dif_score = st.slider('Difficulty Score', max_value=40)
    
    st.divider()

    mod_total = mod_base + mod_bonus
    
    dice = [die_skill, die_tool] + ([die_assist] * num_assist)
    dice = [die for die in dice if die != 0]
    
    df = dice_dist(dice, mod_total)
    
    print_summary_stats(df)

plot_graph_and_print_values(df, dif_score)