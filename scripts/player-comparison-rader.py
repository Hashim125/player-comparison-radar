# Streamlit app for comparing football players using pizza plots

import streamlit as st
import pandas as pd
from mplsoccer import PyPizza
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from highlight_text import fig_text

# Define the paths to your font files
font_normal_path = 'fonts/Roboto/Roboto-Regular.ttf'
font_italic_path = 'fonts/Roboto/Roboto-Italic.ttf'
font_bold_path = 'fonts/Roboto/Roboto-Bold.ttf'

# Create FontProperties instances for each font
font_normal = FontProperties(fname=font_normal_path)
font_italic = FontProperties(fname=font_italic_path)
font_bold = FontProperties(fname=font_bold_path)


# Load the data
file_path = 'data/player_iteration_averages_League_One_1023.csv'
df = pd.read_csv(file_path)

# Derived metrics
df['Ground_Duels_Won_Pct'] = df['WON_GROUND_DUELS'] / (df['WON_GROUND_DUELS'] + df['LOST_GROUND_DUELS'])
df['Aerial_Duels_Won_Pct'] = df['WON_AERIAL_DUELS'] / (df['WON_AERIAL_DUELS'] + df['LOST_AERIAL_DUELS'])
df['Pass_Pct'] = df['SUCCESSFUL_PASSES'] / (df['SUCCESSFUL_PASSES'] + df['UNSUCCESSFUL_PASSES'])
df['Low_Cross_Pct'] = df['SUCCESSFUL_PASSES_BY_ACTION_LOW_CROSS'] / (df['SUCCESSFUL_PASSES_BY_ACTION_LOW_CROSS'] + df['UNSUCCESSFUL_PASSES_BY_ACTION_LOW_CROSS'])
df['High_Cross_Pct'] = df['SUCCESSFUL_PASSES_BY_ACTION_HIGH_CROSS'] / (df['SUCCESSFUL_PASSES_BY_ACTION_HIGH_CROSS'] + df['UNSUCCESSFUL_PASSES_BY_ACTION_HIGH_CROSS'])

# Filter for right wingback defenders
df_mins = df[df['playDuration'] >= 27000]
filtered_df = df_mins[df_mins['position'] == 'RIGHT_WINGBACK_DEFENDER']

# Columns to exclude from normalization
exclude_cols = ['iterationId','competitionName','season', 'squadId', 'squadName', 'playerId', 'playerName', 'firstname', 'lastname', 'birthdate', 'birthplace', 'leg', 'position', 'matchShare', 'playDuration']
cols_to_normalize = [col for col in df.columns if col not in exclude_cols]

# Normalize the data
df_percentiles = df_mins.copy()
df_percentiles[cols_to_normalize] = df[cols_to_normalize].rank(pct=True) * 100

# Parameters for the pizza plot
params = ["Ground_Duels_Won_Pct","Aerial_Duels_Won_Pct","Low_Cross_Pct","High_Cross_Pct","NUMBER_OF_PRESSES","BALL_WIN_NUMBER","BALL_WIN_NUMBER_BY_ACTION_INTERCEPTION","BALL_WIN_NUMBER_BY_ACTION_LOOSE_BALL_REGAIN","BYPASSED_OPPONENTS_BY_ACTION_DRIBBLE","PXT_DRIBBLE","PXT_PASS","PXT_PASS_PRO","PXT_DRIBBLE_PRO","ASSISTS"]

# Streamlit app UI
st.title('Player Profiling App')
st.markdown('Compare player performance using interactive pizza plots.')
st.markdown('Choose two players from below - players are right sided full backs with a minimum of 5 games played.')

# Player selection using dropdowns
player1 = st.selectbox('Select Player 1', filtered_df['playerName'].unique())
player2 = st.selectbox('Select Player 2', filtered_df['playerName'].unique())

# Filter for the selected players
player_1_row = df_percentiles[df_percentiles['playerName'] == player1]
player_2_row = df_percentiles[df_percentiles['playerName'] == player2]




# Ensure players are found
if not player_1_row.empty and not player_2_row.empty:
    values_1 = [round(val) for val in player_1_row[params].iloc[0].tolist()]
    values_2 = [round(val) for val in player_2_row[params].iloc[0].tolist()]

    params = ["Ground Duels\n Won %","Aerial Duels\n Won %","Low Cross %","High Cross %","Number of Presses","Ball Wins","Ball Wins\n by Interception",
          "Ball Wins\n by Loose Ball Regain","Opponents \n Bypassed \n by Dribbling","Dribble\n Expected Threat","Pass\n Expected Threat",
          "Progressive Pass\n Expected Threat","Progressive Dribble\n Expected Threat","Assists"]
    
    # Instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#EBEBE9",     # background color
        straight_line_color="#222222",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=1,               # linewidth of last circle
        last_circle_color="#222222",    # color of last circle
        other_circle_ls="-.",           # linestyle for other circles
        other_circle_lw=1               # linewidth for other circles
    )

    # Plot the pizza chart
    fig, ax = baker.make_pizza(
        values_1,
        compare_values=values_2,
        figsize=(12, 12),
        kwargs_slices=dict(facecolor="#1A78CF", edgecolor="#222222", linewidth=1),
        kwargs_compare=dict(facecolor="#FF9300", edgecolor="#222222", linewidth=1),
        kwargs_params=dict(color="#000000", fontsize=16, fontproperties=font_normal, va="center"),
        kwargs_values=dict(color="#000000", fontsize=16, fontproperties=font_normal),
        kwargs_compare_values=dict(color="#000000", fontsize=16, fontproperties=font_normal)
    )

    # Add title
    fig_text(
        0.515, 0.99, f"<{player1}> vs <{player2}>", size=20, fig=fig,
        highlight_textprops=[{"color": '#1A78CF'}, {"color": '#FF9300'}],
        ha="center", fontproperties=font_bold, color="#000000"
    )

    # Display the plot
    st.pyplot(fig)
else:
    st.error("One or both players not found in the filtered data.")
