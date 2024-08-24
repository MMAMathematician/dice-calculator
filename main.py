import streamlit as st
import numpy as np
from scipy import stats
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

with st.sidebar:
    die_skill = st.selectbox('Size of Skill Die', [4, 6, 8, 10, 12, 20])
    die_tool = st.selectbox('Size of Tool Die', [0, 4, 6, 8, 10, 12, 20])
    die_assist = st.selectbox('Size of Assist Die', [0, 4, 6, 8, 10, 12, 20])
    mod_base = st.slider('Base Modifier', max_value=20)
    mod_bonus = st.slider('Bonus Modifier', max_value=20)
    dif_score = st.slider('Difficulty Score', max_value=40)

    mod_total = mod_base + mod_bonus
    
    dice = [die_skill, die_tool, die_assist]
    dice = [die for die in dice if die != 0]
    
    dist = np.array([1])
    for die in dice:
        unif = np.full((die), 1)
        dist = np.convolve(dist, unif)
        
    roll_nums = range(mod_total + len(dice), np.sum(dice) + mod_total + 1)
        
    df = pd.merge(left=pd.DataFrame(roll_nums, columns=['Score']), right=pd.DataFrame(dist, columns=['Frequency']), left_index=True, right_index=True)
    
    df['Win'] = df['Score'] >= dif_score
    
    scores = df.loc[df.index.repeat(df['Frequency'])]['Score']
    scores = np.array(scores).astype(float)

    win_rate = np.count_nonzero(scores >= dif_score)/len(scores)

    st.text(f'Min:      {np.min(scores)}')
    st.text(f'Q1:       {np.quantile(scores, 0.25)}')
    st.text(f'Mean:     {np.mean(scores)}')
    st.text(f'Median:   {np.median(scores)}')
    st.text(f'Mode(s):  {', '.join(map(str, statistics.multimode(scores)))}')
    st.text(f'Q3:       {np.quantile(scores, 0.75)}')
    st.text(f'Max:      {np.max(scores)}')
    st.text(f'IQR:      {stats.iqr(scores)}')
    st.text(f'STD:      {np.std(scores):.2f}')

sns.set_theme(rc={'axes.facecolor':'#0E1117',
                  'figure.facecolor':'#0E1117',
                  'axes.grid': False,
                  'text.color': 'white',
                  'axes.labelcolor': 'white',
                  'xtick.color': 'white',
                  'ytick.color': 'white',
                  'figure.edgecolor': 'white',
                  'axes.titlecolor': 'white'
})

fig = plt.figure()

ax = sns.histplot(data=df, x='Score', weights='Frequency', binwidth=1, discrete=True, stat="density", hue='Win', palette={True: '#4BFF4B', False: '#FF4B4B'}, legend=False)

st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Win Rate", value=f"{win_rate*100:.2f}%")

with col2:
    st.metric(label="Critical Rate", value=f"{1/len(scores)*100:.2f}%")