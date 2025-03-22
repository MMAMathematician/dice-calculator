import streamlit as st
import numpy as np
import pandas as pd
from common.common import *

st.set_page_config(page_title="First Encounter Showdown Calculator")
st.title("First Encounter Showdown Calculator")

with st.sidebar:
    d10 = st.number_input("Number of Player d10s", value=4)
    d20 = st.number_input("Number of Enemy d20s", value=1)
    
    st.divider()
    
    mod = st.slider('Total Modifier', min_value=-10, max_value=10, value=0)
    
    st.divider()
    
    dice_player = [10] * d10
    df_player = dice_dist(dice_player, mod)
    
    dice_enemy = [20] * d20
    df_enemy = dice_dist(dice_enemy, 0).iloc[::-1]
    
    dist = np.convolve(df_player['Frequency'], df_enemy['Frequency'])
        
    roll_nums = range(mod + len(dice_player) - np.sum(dice_enemy), np.sum(dice_player) - len(dice_enemy) + mod + 1)
        
    df = pd.merge(left=pd.DataFrame(roll_nums, columns=['Score']), right=pd.DataFrame(dist, columns=['Frequency']), left_index=True, right_index=True)
    
    print_summary_stats(df)
    
plot_graph_and_print_values(df, 0, show_crit=False)