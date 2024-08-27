import streamlit as st
import numpy as np
from scipy import stats
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from common.common import *

st.set_page_config(page_title="Variable Dice Calculator")
st.title("Variable Dice Calculator")

with st.sidebar:
    d2_skill = st.number_input("Number of d2s", value=0)
    d4_skill = st.number_input("Number of d4s", value=1)
    d6_skill = st.number_input("Number of d6s", value=1)
    d8_skill = st.number_input("Number of d8s", value=1)
    d10_skill = st.number_input("Number of d10s", value=2)
    d12_skill = st.number_input("Number of d12s", value=1)
    d20_skill = st.number_input("Number of d20s", value=0)
    
    st.divider()
    
    die_tool = st.selectbox('Size of Tool Die', [0, 2, 4, 6, 8, 10, 12, 20])
    die_assist = st.selectbox('Size of Assist Die', [0, 2, 4, 6, 8, 10, 12, 20])
    num_assist = st.number_input("Number of Assist Dice", value=1)
    
    mod_base_dist = st.selectbox('Distribution of Base Modifier', ['Binomial', 'Constant'])
    
    mod_base = st.slider('Base Modifier', max_value=20, disabled=(mod_base_dist != 'Constant'))
    mod_bonus = st.slider('Bonus Modifier', max_value=20)
    dif_score = st.slider('Difficulty Score', max_value=40)
    
    st.divider()
    
    possible_skill_die = [2, 4, 6, 8, 10, 12, 20]
    counts_skill_die = [d2_skill, d4_skill, d6_skill, d8_skill, d10_skill, d12_skill, d20_skill]
    
    df = pd.DataFrame(columns=['Score', 'Frequency', 'Critical Hits'])
    
    other_dice = [die_tool] + ([die_assist] * num_assist)
    other_dice = [die for die in other_dice if die != 0]
    
    for i, die_skill in enumerate(possible_skill_die):
        if counts_skill_die[i] != 0:
            df_new = dice_dist([die_skill] + other_dice, mod_bonus)
            df = pd.merge(df, df_new, on='Score', how='outer', suffixes=('_old', '_new'))
            
            df['Frequency_old'].fillna(0, inplace=True)
            df['Frequency_new'].fillna(0, inplace=True)
            df['Critical Hits_old'].fillna(0, inplace=True)
            df['Critical Hits_new'].fillna(0, inplace=True)
            
            df['Frequency_new'] = df['Frequency_new'] * counts_skill_die[i]
            df['Critical Hits_new'] = df['Critical Hits_new'] * counts_skill_die[i]
            
            df['Frequency'] = df['Frequency_old'] + df['Frequency_new']
            df['Critical Hits'] = df['Critical Hits_old'] + df['Critical Hits_new']
            
            df = df[['Score', 'Frequency', 'Critical Hits']]
    
    if mod_base_dist == 'Binomial':
        x = np.arange(0, die_skill + 1)
        binom_counts = stats.binom.pmf(x, die_skill, 0.25)

        dist = np.convolve(df['Frequency'], binom_counts)
        dist_crits = np.convolve(df['Critical Hits'], binom_counts)
        
        roll_nums = np.arange(min(df['Score']), max(df['Score']) + die_skill + 1)
            
        df = pd.merge(left=pd.DataFrame(roll_nums, columns=['Score']), right=pd.DataFrame(dist, columns=['Frequency']), left_index=True, right_index=True)
        df = pd.merge(left=df, right=pd.DataFrame(dist_crits, columns=['Critical Hits']), left_index=True, right_index=True)
    
    elif mod_base_dist == 'Constant':
        df['Score'] = df['Score'] + mod_base
        
    
    print_summary_stats(df)
    
plot_graph_and_print_values(df, dif_score)