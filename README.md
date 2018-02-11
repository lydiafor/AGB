# AGB

Objectives

The objective of this assignment is to build a Naive Bayes model to predict the tissue type or brain region from the pattern of splicing of the samples. You will have to choose one of these two datasets.

The class values for the classification will be the brain region (amygdala, etc...) in the first set, or the tissue type (heart, etc..) in the second.
Separate the datasets into sets for training and testing. A subset of samples will be used for training and a different subset of samples for testing. Make sure that you use the same number of samples from each tissue type or brain region for training. For testing, balanced sets are relevant to build proper ROC curves, but in general you can evaluate the accuracy on the rest of the samples.
The attributes that describe each sample will be the PSI values of the SE event. We will discretize the PSI values into two possible values: up is PSI > 0.5 and down if PSI< 0.5. You can discard the cases that do not have a number assigned, i.e. NA.
For each class (brain region / tissue type), and for each attribute (SE event), you will have to measure the likelihoods (proportions) of each value up/down in each class. For instance, for event e, we will measure:
P(e_up|heart), P(e_down|heart) 
P(e_up|liver), P(e_down|iver)
...
Using as attributes the discretized inclusion of events, and using Mutual Information (Information Gain) on the training set, determine which attributes are the most informative to separate between the tumor types. The Mututal Information provides a single value per event, which gives a sense of how well the discretized PSI (attribute value) is associated to the tissue types (class values). Recall that for a given set of classification values S and an attribute A (event), the Mutual Information is defined as:
MI(S,A) = H(S) - H(S|A)
where the relative entropy is calculated as (see the course slides):

H(S|A) =    P(heart, e_up) log2 ( P(heart, e_up) / P(e_up) )  +  P(heart, e_down) log ( P(heart, e_down) / P(e_down) ) 
         +  P(liver, e_up) log2 ( P(liver, e_up) / P(e_up) )  +  P(liver, e_down) log ( P(liver, e_down) / P(e_down) ) 
         +  ...
Using the best predictive attributes, build a Naive Bayes model with the training set and use it to predict the tissue type / brain region on the testing set. The output of the program should be the resulting classification for each test case using the Naive Bayes classifier, together with a score and the real label. Remember that the scores can be transformed into a probability. The output should be of the form, e.g.:
score    prediction   label   sample

-20.04   heart        heart    id1
-30.03   heart        kidney   id2
-21.32   liver        liver    id3
...
Consider the use of pseudocounts and discuss whether they are necessary or not. 
Determine the accuracy of the model by computing the coincidences and the discrepancies between the predictions and the actual labels. You can calculate the following quantities:
TPR (true positive rate): proportion of samples that we predict correctly
FDR (false discovery rate): proportions of predictions that do not agree with the actual type.

Discuss the choice of a score (or probability) cut-off to select your predictions and thereby reduce the number of false positives. Can you find an optimal cut-off? 
Discuss whether this is a good classifier or not. Can you propose a way to improve the classifier?
Important

Since we are going to multiply probabilities, we will obtain in general very small numbers. This can become a problem as computers have a limitation in the number of decimals they can handle. A solution to this problem is to consider the logarithm of the probabilities. The products become sums and the maximization procedure to select the best hypothesis remain the same.
