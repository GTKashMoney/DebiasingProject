# DebiasingProject
## Project Summary:  

Unintended biases in the dataset can cause unwanted correlations in the predictions of many deep models which can cause disastrous consequences in terms of ethics. Even the researchers in Meta have shown that their Deepfake Detection Challenge winners have a large bias towards lighter skin toned subjects [2]. Recent papers have demonstrated techniques such as regularization, data-augmentation, and other methods for de-biasing general models. We aim to apply these techniques to the existing models for the Deepfake Detection Challenge winners to compare the efficacy and practicality of these techniques on larger models. 

## Approach: 

Our first approach is to replicate the top winner of the Deepfake Detection Challenge model and modify it to have at least one de-biasing technique. Multiple de-biasing techniques would be more beneficial as it would allow for more comparisons, but that is considered a stretch goal. Another stretch goal would be to implement multiple models, say the top 5 winners of the Deepfake Detection Challenge as an example.  

Analysis of the results would include comparing the overall performance of a curated un-biased test set, a skewed in-lined biased test set, and a skewed out-of-line biased test set, where the out-of-line set would contain a distribution of biases that go against the bias in the training set. The performance will be measured with and without using the de-biasing technique over as many winning algorithms as we can implement in time. 