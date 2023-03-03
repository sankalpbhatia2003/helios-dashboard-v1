import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import altair as alt
import pandas as pd
import numpy as np

st.title("Tonal Sentiment Analysis")

st.subheader("What is Tonal Analysis?")
with st.expander("See Explanation"):
    st.write("""Hi there! A Tonal Sentiment score is a way to measure how a person's voice sounds when they're speaking, and whether it sounds positive, negative, or neutral.
When we communicate with other people, we use both our words and our tone of voice to convey meaning. Sometimes we might say something that sounds nice, but if our tone of voice is angry or sarcastic, the person we're talking to might think we're actually being mean.
That's why it's important to measure both the tone of voice and the text sentiment together. If we only look at the words someone is saying, we might miss important clues about how they're really feeling. But if we also pay attention to their tone of voice, we can get a better sense of their emotions and intentions.
For example, imagine your friend says "I'm fine" when you ask them how they're doing. If they say it with a cheerful tone of voice, you might think they're actually doing great. But if they say it with a sad or angry tone of voice, you might realize that they're actually not doing so well.
So, by measuring both the tone of voice and the text sentiment together, we can better understand what someone is really trying to say.""")

#st.write("You might have heard of text analysis? It is the process of analysing texts from a document. But texts can be highly deceivable. Simply a text isn't enough to understand what the speaker is trying to say. That is where Tonal Sentiment Analysis comes into the picture. Tonal Analysis is defined as using the speakers' various voice features such as loudness, pitch, frequency, etc., and quantifying them to retrieve insights which the speaker would exclusivley have. Tonal Analysis has a wide use case but we'll be focussing on how it can generate values that can give us an insight about what the company executives know about their company that others do not.")

st.subheader("Analyzing Compass CEO - Robert Reffkin's Tonal Sentiment")
st.caption("The audio analyzed was released by CNBC Television on 9th Jan 2023 after Robert Reffkin layed off his employs for the 3rd time")

emotion = 'Disgust'

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

################################################################
with st.expander("ℹ️ Information about the Emotion Classifier"):
    st.info("""The Convolutional Neural Network (CNN) Speech Emotion Classifier model was built to classify emotions from audio files. The model is trained on the RAVDESS dataset, "The Ryerson Audio-Visual Database of Emotional Speech and Song" by Livingstone & Russo, which is licensed under CC BY-NA-SC 4.0. RAVDESS contains 7,356 files that includes 24 professional actors (12 female, 12 male), vocalizing two lexically-matched statements in a North American accent.
The purpose of this model is to classify emotions majorly into 8 emotions: neutral, calm, happy, sad, angry, fearful, surprise, and disgust with a current accuracy of 64% The model also includes the classification of the speakers’ gender. This machine learning model was developed to accompany and enhance the insights generated from Helios’ Tonal Sentiment Data. """)
    
st.subheader("Overall Audio Emotion: _:orange[{}]_ {}".format(emotion, '🤨'))
################################################################
#data = data.fillna(0)

col1, col2, col3 = st.columns(3)
col2.metric(label="Average Tonal Sentiment Score", value=round(data['Robert Reffkin'].mean(), 4))#, delta=round(data['Robert Reffkin'].mean(), 4) - 0)
col3.metric("Maximum Tonal Score", value=round(data['Robert Reffkin'].max(), 4), delta = round(data['Robert Reffkin'].max() - data['Robert Reffkin'].mean(), 4))
col1.metric("Minimum Tonal Score", value=round(data['Robert Reffkin'].min(), 4), delta = round(data['Robert Reffkin'].min() - data['Robert Reffkin'].mean(), 4))

st.subheader("Robert Reffkin's value on our Tonal Sentiment Scale")
################################################################
# Define the color gradient
cmap = LinearSegmentedColormap.from_list('RedBlue', ['#FF0000', '#0000FF'])

# Define the x-axis values
x = np.linspace(-5, 5, num=100)

# Set the value to indicate with a vertical line
val = data['Robert Reffkin'].mean()

# Find the index of the closest value to `val` in the x-axis array
idx = np.abs(x - val).argmin()

# Create the plot
fig, ax = plt.subplots(figsize=(10,0.5))
ax.axvline(x=x[idx], color='black', lw=2)
ax.imshow(np.array([x]), aspect='auto', cmap=cmap, extent=[-5, 5, -1, 1])
ax.set_xlim([-5, 5])
ax.set_ylim([-1, 1])
ax.set_xticks(np.arange(-5, 6, 1))
ax.set_yticks([])

ax.set_facecolor('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

ax.set_xlabel('Tonal Sentiment Score')

# Display the plot in the Streamlit app
st.pyplot(fig)
################################################################
st.subheader("Tonal Sentiment behind each of his sentences")

# Plotting metrics
diff = (data['Robert Reffkin'].mean() - data['Interviewer 1'].mean()) / 2

st.bar_chart(data['Robert Reffkin'])
################################################################
