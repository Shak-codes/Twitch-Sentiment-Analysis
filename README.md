<h1 align="center">Twitch-Sentiment-Analysis</h1>

&nbsp;&nbsp;&nbsp;&nbsp;**1. Introduction.** The purpose of this analysis is to aid my Twitch Classifier report. That report handles predicting the channel origin of messages given their pairwise letter combination frequency. If you're unfamiliar with Twitch, they are a live streaming service where creators broadcast content on their own Twitch channel while interacting with viewers in real time through chat. The report explains motivation behind these predictions. Essentially, each Twitch channel fosters their own community with distinct tone and quirks in their messaging. Intuitively this makes sense, because different channels attract different types of viewers and these communities naturally develop their own linguistic patterns. However this intuitive understanding lacks any statistical evidence to actually support the belief. This is where sentiment analysis comes into play. We aim to create our own models that can accurately determine the sentiment of the various channels within the RDC group, and hope to extend this to other channels to validate our hypothesis that each channel's community exhibits a unique communication style reflected in their chat communication.

&nbsp;&nbsp;&nbsp;&nbsp;**2. Data.** Our analysis involves collecting message data from the creators at RDC, alongside a few Splatoon streamers(Kyo and Shadow). While we aim to make separate models for Kyo and Shadow's chat, we will also have a single model for the entirety of the five RDCGaming channels(RDCGaming, RDCGamingTwo, RDCGamingThree, RDCGamingFour, RDCGamingFive) since the five chats belong to their overall community, so by developing a single model for the entire community, it will perform well in each individual subset.

&nbsp;&nbsp;&nbsp;&nbsp;***2.1. Data.*** In terms of the chat messages collected, it's fairly rudimentary. Any message sent in these chats by a real person(not a robot), that doesn't include any links or commands will be collected. For each message, the following is recorded: the username of the sender, the message content itself, the Twitch channel the message originates from (which is then mapped to the individual streaming at the time. Ie. If Desmond is streaming on RDCGamingTwo, the message would belong to Desmond's chat. NOTE: This is only applicable to the RDC group and not Shadow/Kyo), and finally the date the message was sent.

&nbsp;&nbsp;&nbsp;&nbsp;**3. Methodology.** Initially, sentiment analysis was to be performed inside the Twitch Classifier report. The idea was to simply use the `cardiffnlp/twitter-roberta-base-sentiment` model, which is a RoBERTa architecture model tuned on social media data(Twitter/X to be specific). This model is designed to perform well on informal and noisy text, which I initially thought would generalize well to Twitch chats but this is not the case at all. Firstly, Twitch chat has their own unique quirks essentially not seen in any other media: inside jokes, emotes, and just general Twitch verbage such as spamming "W" are all things this pre-trained social media model fails to pick up on. As a result we will create our own model by training it on handpicked chat message data.

&nbsp;&nbsp;&nbsp;&nbsp;***3.1. Classifiers.*** Typical sentiment analysis works with positive, negative, and neutral sentiment. However, we wish to have a much better understanding of chat dynamics and so our model will extend to encapsulate the following tones:

- Positive: General positivity
- Hyped: Intense excitement
- Laughter: Humor
- Negative: General dislike/criticism
- Upset: Anger/Frustration
- Toxic: Lighthearted harassment
- Neutral: Non emotional messages
- Shocked: Surprise/Disbelief

&nbsp;&nbsp;&nbsp;&nbsp;***3.2. Classification.*** Given these
