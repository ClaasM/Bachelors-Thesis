from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# %matplotlib inline whatever the fuck that does


wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color='black',
                      width=2500,
                      height=2000
                      ).generate(" ".join([word for element in subj_docs for word in element[0]]))
plt.figure(1, figsize=(13, 13))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
