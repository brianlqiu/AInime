# AInime

This repository contains data collection scripts and the Jupyter notebook used to apply transfer learning to classify 94 different anime characters. 
A general description and reflection on the approach I took is provided below.

# Data Collection
The dataset was composed of 100+ images for each character pulled from Danbooru, a popular anime fanart aggregator.
The data was pre-processed and cropped to the face using `animeface-2009` to reduce filesizes and to possibly introduce some normalization.
The dataset was then split into test/validation sets with a split of 85-15.

# Training
The dataset was zipped and uploaded to Google Drive, which was accessible to Google Colab through mounting.
Tensorflow and Keras were used to create, build, and train the model.


Two popular CNN architectures were tested: Inception v3 and ResNet50. 
ResNet50 performed far better than Inception v3, achieving a final validation accuracy of **65%** whereas Inception v3 plateaued at around **50%**.

# Reflections
Although the accuracies may not seem too impressive, they are about what I expected. 
Many of these characters were difficult to distinguish between even for me, and since the dataset was comprised of fanart, that meant that the images were drawn in a 
wide variety of styles and at much different qualities.
Some data came from black-and-white manga panels, some were drawn in a chibi style, some were drawn in a more Westernized style, etc. 
If I were to attempt this again (which I probably will do), I would definitely improve the quality and consistency of my dataset.
