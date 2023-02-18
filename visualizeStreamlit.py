import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import numpy as np

st.title("Tonal Sentiment Analysis")

st.subheader("What is Tonal Analysis?")
with st.expander("See Explanation"):
    st.write("You might have heard of text analysis? It is the process of analysing emotions from a given text. But texts can be highly deceivable when it comes to analysing emotions and the true sentiment behind them. Simply a text isn't enough to understand what the speaker is trying to say. That is where Tonal Sentiment Analysis comes into the picture. Tonal Analysis is defined as using the speakers' various voice features such as loudness, pitch, frequency, etc., and quantifying them to retrieve insights which the speaker would exclusivley have. Tonal Analysis has wide use cases but we'll be focusing on how it can generate values that can give us an insight about what the company executives know about their company that others do not.")

#st.write("You might have heard of text analysis? It is the process of analysing texts from a document. But texts can be highly deceivable. Simply a text isn't enough to understand what the speaker is trying to say. That is where Tonal Sentiment Analysis comes into the picture. Tonal Analysis is defined as using the speakers' various voice features such as loudness, pitch, frequency, etc., and quantifying them to retrieve insights which the speaker would exclusivley have. Tonal Analysis has a wide use case but we'll be focussing on how it can generate values that can give us an insight about what the company executives know about their company that others do not.")

st.subheader("Analyzing Compass CEO - Robert Reffkin's Tonal Sentiment")
st.caption("The audio analyzed was released by CNBC after Robert Reffkin layed off his employs for the 3rd time")

# Displaying YouTube Video
st.video('https://youtu.be/72sz2zDQkqo') 
#st.audio(audio_file, format="audio/wav", start_time=0)

# Plotting area chart
data = pd.read_csv("compass_ceo_cnbc_visualise.csv")
later_data = data
data = data.reset_index(drop=True)
data = data.set_index("Sentence")

# Define options for dropdown menu
options = ['Sentence with highest conviction about future POSTIVE performance', 'Sentence with conviction about future NEGATIVE performance']

# Create dropdown menu and get user's selection
option = st.selectbox('Select an option', options)

# Find sentence with highest tonal score
if option == options[0]:
    max_sentence = later_data.loc[later_data['Robert Reffkin'].idxmax(), 'Sentence']
    st.subheader(f' **_:green["{max_sentence}"]_** ')
# Find sentence with lowest tonal score
elif option == options[1]:
    min_sentence = later_data.loc[later_data['Robert Reffkin'].idxmin(), 'Sentence']
    st.subheader(f' **_:red["{min_sentence}"]_** ')

# Show default message if no option is selected
else:
    st.write("Please select an option")

#data = data.fillna(0)

col1, col2, col3 = st.columns(3)
col2.metric(label="Average Tonal Sentiment Score", value=round(data['Robert Reffkin'].mean(), 4))#, delta=round(data['Robert Reffkin'].mean(), 4) - 0)
col3.metric("Maximum Tonal Score", value=round(data['Robert Reffkin'].max(), 4), delta = round(data['Robert Reffkin'].max() - data['Robert Reffkin'].mean(), 4))
col1.metric("Minimum Tonal Score", value=round(data['Robert Reffkin'].min(), 4), delta = round(data['Robert Reffkin'].min() - data['Robert Reffkin'].mean(), 4))

st.subheader("Robert Reffkin's value on our Tonal Sentiment Scale")
################################################################
# Define the values for the likert scale
likert_values = np.arange(-5, 6)

# Define the color scale for the likert scale
color_scale = alt.Scale(domain=likert_values,
                        range=["#FF0000", "#FF3333", "#FF6666", "#FF9999", "#FFCCCC",
                               "#EBEBEB", "#99CCFF", "#66A3FF", "#3380FF", "#004DFF"])

# Create the chart
chart = alt.Chart(pd.DataFrame({"tonal_values": likert_values})).mark_bar().encode(
    #x=alt.X("count()", title="Number of Responses"),
    y=alt.Y("tonal_values:O", title="Tonal Sentiment", axis=alt.Axis(labelAngle=0, ticks=False)),
    color=alt.condition(
        alt.datum.tonal_values == round(data['Robert Reffkin'].mean(), 0),
        alt.value("grey"),
        alt.Color('tonal_values:Q', scale=color_scale, legend=None)
    )
).properties(height=200, width=500)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
################################################################
st.subheader("Tonal Sentiment behind each of his sentences")
#my_bar.progress(round(data['Robert Reffkin'].mean(), 4), text=progress_text)
# Plotting metrics
diff = (data['Robert Reffkin'].mean() - data['Interviewer 1'].mean()) / 2

st.bar_chart(data['Robert Reffkin'])

############################################################################
