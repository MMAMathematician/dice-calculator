import streamlit as st
import numpy as np
import pandas as pd
from common.common import *

def dice_dist_adv(dice, adv):
    dist = np.array([1])
    if adv: 
        for die in dice:
            pdf = 2 * np.arange(1, die + 1) - np.full((die), 1)
            dist = np.convolve(dist, pdf)
    else:
        for die in dice:
            pdf = 2 * die - 2 * np.arange(1, die + 1) + np.full((die), 1)
            dist = np.convolve(dist, pdf)
        
    roll_nums = range(len(dice), np.sum(dice) + 1)
        
    df = pd.merge(left=pd.DataFrame(roll_nums, columns=['Score']), right=pd.DataFrame(dist, columns=['Frequency']), left_index=True, right_index=True)
    
    return df['Frequency']

st.set_page_config(page_title="First Encounter Showdown Calculator")
st.title("First Encounter Showdown Calculator")

with st.sidebar:
    d10 = st.number_input("Number of Player d10s", value=4)
    d20 = st.number_input("Number of Enemy d20s", value=1)
    
    st.divider()
        
    num_adv_ply = st.number_input("Number of Player Advantages", value=0, min_value=0, max_value=d10)
    num_dis_ply = st.number_input("Number of Player Disadvantages", value=0, min_value=0, max_value=d10-num_adv_ply)
        
    num_adv_ene = st.number_input("Number of Enemy Advantages", value=0, min_value=0, max_value=d20)
    num_dis_ene = st.number_input("Number of Enemy Disadvantages", value=0, min_value=0, max_value=d20-num_adv_ene)
    
    st.divider()
    
    mod = st.slider('Total Modifier', min_value=-10, max_value=10, value=0)
    
    st.divider()
    
    dice_player = [10] * (d10 - num_adv_ply - num_dis_ply)
    dice_player_adv = [10] * (num_adv_ply)
    dice_player_dis = [10] * (num_dis_ply)
    
    df_player = np.array([1], dtype=np.int64)
    
    if (dice_player != []):
        df_player = dice_dist(dice_player, mod)
        df_player = df_player['Frequency']
        
    if (dice_player_adv != []):
        df_player_adv = dice_dist_adv(dice_player_adv, True)
        df_player = np.convolve(df_player, df_player_adv)
        
    if (dice_player_dis != []):
        df_player_dis = dice_dist_adv(dice_player_dis, False)
        df_player = np.convolve(df_player, df_player_dis)
    
    dice_enemy = [20] * (d20 - num_adv_ene - num_dis_ene)
    dice_enemy_adv = [20] * (num_adv_ene)
    dice_enemy_dis = [20] * (num_dis_ene)
    
    df_enemy = np.array([1], dtype=np.int64)
    
    if (dice_enemy != []):
        df_enemy = dice_dist(dice_enemy, 0)
        df_enemy = df_enemy['Frequency']
    
    if (dice_enemy_adv != []):
        df_enemy_adv = dice_dist_adv(dice_enemy_adv, True)
        df_enemy = np.convolve(df_enemy, df_enemy_adv)
        
    if (dice_enemy_dis != []):
        df_enemy_dis = dice_dist_adv(dice_enemy_dis, False)
        df_enemy = np.convolve(df_enemy, df_enemy_dis)
    df_enemy = df_enemy[::-1]
    
    dist = np.convolve(df_player, df_enemy)
        
    roll_nums = range(mod + len(dice_player + dice_player_adv + dice_player_dis) - np.sum(dice_enemy + dice_enemy_adv + dice_enemy_dis), np.sum(dice_player + dice_player_adv + dice_player_dis) - len(dice_enemy + dice_enemy_adv + dice_enemy_dis) + mod + 1)
        
    df = pd.merge(left=pd.DataFrame(roll_nums, columns=['Score']), right=pd.DataFrame(dist, columns=['Frequency']), left_index=True, right_index=True)
    
    print_summary_stats(df)
    
plot_graph_and_print_values(df, 0, show_crit=False)