import streamlit as st
import numpy as np
import pandas as pd
import statistics
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

def dice_dist(dice, mod_total):
    dist = np.array([1])
    for die in dice:
        unif = np.full((die), 1)
        dist = np.convolve(dist, unif)
        
    roll_nums = range(mod_total + len(dice), np.sum(dice) + mod_total + 1)
        
    df = pd.merge(left=pd.DataFrame(roll_nums, columns=['Score']), right=pd.DataFrame(dist, columns=['Frequency']), left_index=True, right_index=True)
    
    df['Critical Hits'] = 0
    df.loc[df['Score'] == np.sum(dice) + mod_total, 'Critical Hits'] = 1
    
    return df

def calculate_quartile(cumcount, scores, count, quartile):
    pos = quartile * count
    idx = np.searchsorted(cumcount, pos)
    if cumcount[idx] == pos:
        return (scores[idx] + scores[idx + 1]) / 2
    else:
        return scores[idx]

def print_summary_stats(df):
    scores = np.array(df['Score'])
    freqs = np.array(df['Frequency'])
    count = freqs.sum()
    fx = scores * freqs
    mean = fx.sum() / count
    variance = ((freqs * scores ** 2).sum() / count) - mean ** 2
    std = np.sqrt(variance)
    minimum = np.min(scores)
    maximum = np.max(scores)
    cumcount = np.cumsum(freqs)
    Q1 = calculate_quartile(cumcount, scores, count, 0.25)
    median = calculate_quartile(cumcount, scores, count, 0.50)
    Q3 = calculate_quartile(cumcount, scores, count, 0.75)
    IQR = Q3 - Q1
    max_frequency = np.max(freqs)
    modes = scores[freqs == max_frequency]
    
    st.text(f'Min:      {minimum:.2f}')
    st.text(f'Q1:       {Q1:.2f}')
    st.text(f'Mean:     {mean:.2f}')
    st.text(f'Median:   {median:.2f}')
    st.text(f'Mode(s):  {', '.join(map(str, modes))}')
    st.text(f'Q3:       {Q3:.2f}')
    st.text(f'Max:      {maximum:.2f}')
    st.text(f'IQR:      {IQR:.2f}')
    st.text(f'STD:      {std:.2f}')
    
def plot_graph_and_print_values(df, dif_score):
    df['Win'] = df['Score'] >= dif_score
    
    count = df['Frequency'].sum()
    
    win_rate = df.loc[df['Win'] == True]['Frequency'].sum()/count
    
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
        st.metric(label="Critical Rate", value=f"{df['Critical Hits'].sum()/count*100:.2f}%")