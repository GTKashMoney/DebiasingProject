# DebiasingProject

## Project Summary:  

Unintended biases in the dataset can cause unwanted correlations in the predictions of many deep models which can cause disastrous consequences in terms of ethics. Even the researchers in Meta have shown that their Deepfake Detection Challenge winners have a large bias towards lighter skin toned subjects [2]. Recent papers have demonstrated techniques such as regularization, data-augmentation, and other methods for de-biasing general models. We aim to apply these techniques to the existing models for the Deepfake Detection Challenge winners to compare the efficacy and practicality of these techniques on larger models. 

## Approach: 

Our first approach is to replicate the top winner of the Deepfake Detection Challenge model and modify it to have at least one de-biasing technique. Multiple de-biasing techniques would be more beneficial as it would allow for more comparisons, but that is considered a stretch goal. Another stretch goal would be to implement multiple models, say the top 5 winners of the Deepfake Detection Challenge as an example.  

Analysis of the results would include comparing the overall performance of a curated un-biased test set, a skewed in-lined biased test set, and a skewed out-of-line biased test set, where the out-of-line set would contain a distribution of biases that go against the bias in the training set. The performance will be measured with and without using the de-biasing technique over as many winning algorithms as we can implement in time. 

## Resources / Related Work:

We are looking to investigate a few de-biasing techniques such as post-training regularization techniques like [EnD](https://arxiv.org/abs/2103.02023), novel loss functions such as [BiasCon](https://proceedings.neurips.cc/paper/2021/hash/de8aa43e5d5fa8536cf23e54244476fa-Abstract.html), and data augmentatiion methods such as those described in [Lee et al](https://proceedings.neurips.cc/paper/2021/file/d360a502598a4b64b936683b44a5523a-Paper.pdf), and [Agarwal et al](https://openaccess.thecvf.com/content/WACV2022/html/Agarwal_Does_Data_Repair_Lead_to_Fair_Models_Curating_Contextually_Fair_WACV_2022_paper.html). EnD is a regularization strategy applied against a final trained model, which has been shown to improve the generalization on unbiased test sets. While BiasCon and all data-augmentation approaches require full-retraining of the target model. As a result, we will prioritize EnD for investigation due to the considerable computational advantages when using a pre-trained model.

## Datasets

A full description of the original challenge is available [here](https://www.kaggle.com/c/deepfake-detection-challenge/overview). The challenge seeks to build a model which can classify short videos as either authentic or generated (deepfake). The original dataset is approximately 470GB 
TThe original data is approximately 470GB, consisting of thousands of short convesational videos. Given the size of the dataset, we may run into concerns with traditional hardware, which can be alleviated through the use of a pre-trained model.

## Group Members:

Kyle Caverly
Steffen Lim
Arnold Nunez
Hannah White

