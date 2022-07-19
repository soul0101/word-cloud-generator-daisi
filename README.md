# word-cloud-generator-daisi
Word clouds (also known as text clouds or tag clouds) work in a simple way: the more a specific word appears in a source of textual data (such as a speech, blog post, or database), the bigger and bolder it appears in the word cloud.
## Applications of a Word Cloud 
1) Searching for Patterns in Data
2) Getting key points from large texts
3) Search Engine Optimization

This daisi provides rich functions to the user to generate a word cloud based on the input text. <br>
## Some key features include: 
1) User can define the shape of the word cloud. 
2) Modular background and contour colors.
3) Flexible quality and resolution of the generated image.

## Test API Call
``` python
import pydaisi as pyd
word_cloud_generator = pyd.Daisi("soul0101/Word Cloud Generator")

text = "generate wordcloud from this sentence"
result_wordcloud = word_cloud_generator.process_wordcloud(text).value
result_wordcloud.show()
```
