#!/usr/bin/pyton

from sklearn.metrics import accuracy_score
import itertools
import numpy as np
import matplotlib.pyplot as plt
import scikitplot as skplt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score




######################################################
################ BASIC PARAMETERS ####################
######################################################

# Function to calculate the accuracy with sklearn
def accuracy_sklearn(results_file):
	results = open(results_file, "r")
	predicted = []
	true = []
	for line in results:
		line = line.strip()
		if line:	
			line = line.split("\t")
			predicted.append(line[1])
			true.append(line[2])
		else:
			continue;
	
	score = accuracy_score(true, predicted)
	print("The score (sklearn) is %4f"%(score))

accuracy_sklearn("prediction_tissues_2.txt")


# Function to calculate the TPR and the FDR
def accuracy_TPR_FDR(results_file):
	results = open(results_file, "r")
	counter = 0
	TPR = 0
	FDR = 0
	for line in results:
		line = line.strip()
		if line:
			counter += 1
			line = line.split("\t")
			if line[1] == line[2]:
				TPR += 1
			else:
				FDR += 1
	print("The total number of samples is %d \n TPR = %4f \n FDR = %4f \n"%(counter, TPR/counter, FDR/counter))	
	

accuracy_TPR_FDR("prediction_tissues_2.txt")



######################################################
###################### PLOTS  ########################
######################################################

# Plotting a confusion matrix
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Organize the data and ompute confusion matrix
results = open("prediction_tissues_2.txt", "r")
array = []
array_ordered = []
predicted = []
true = []
for line in results:
	line = line.strip()
	if line:	
		line = line.split("\t")
		array.append(line)
	else:
		continue;
	line[3] = float(line[3])

array_ordered = sorted(array, key = lambda x: x[2])
#print(array_ordered)
true_labels = []
predicted_labels = []
for element in array_ordered:
	true_labels.append(element[2])
	predicted_labels.append(element[1])
	#print(element[1], element[2], "\n")

nerve_c = true_labels.count("Nerve")
lung_c = true_labels.count("Lung")
muscle_c = true_labels.count("Muscle")
heart_c = true_labels.count("Heart")
liver_c = true_labels.count("Liver")

print("Muestras por tejido:\n Nerve: %d\n Lung: %d\n Muscle: %d\n Heart: %d\n Liver: %d\n"%(nerve_c, lung_c, muscle_c, heart_c, liver_c))


cnf_matrix = confusion_matrix(true_labels, predicted_labels)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
class_names = ['Heart', 'Liver', 'Lung', 'Muscle', 'Nerve']
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                     title='Confusion matrix, without normalization')

#Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')

plt.show()


######################################################
#################### CUT-OFF  ########################
######################################################

# ordenamos por score y binarizamos segun TP=1 o FN=0


scores_list = []
TP_or_FN_list = []
FN_list = []
TP_list = []

for element in array:
	equal = 0
	if element[1] == element[2]:
		equal = 1
		TP_list.append(float(element[3]))
	else:
		FN_list.append(float(element[3]))
	element.append(equal)

	scores_list.append(element[3])
	TP_or_FN_list.append(element[4])	
	#print(element[1], element[2], element[3], element[4], "\n")


array_ordered_by_score = sorted(array, key = lambda x: x[3], reverse=True)
# array_ordered_by_equal = sorted(array_ordered_by_score, key = lambda x: x[3], reverse=True)

# for element in array_ordered_by_score:	
#  	print(element[1], element[2], element[3], element[4], "\n")


min_score = int(array_ordered_by_score[0][3])
max_score = int(array_ordered_by_score[-1][3])

#print(min_score, max_score)


cut_off_dict = {}
TPR_array = []
FPR_array = []
PPV_array = []
for i in range(min_score, max_score, -7000):
	cut_off_dict[i] = []
	TP = 0
	FP = 0
	TN = 0
	FN = 0
	for element in array_ordered_by_score:
		if element[3] < i:
			if element[4] == 1:
				TP += 1
			else:
				FP += 1
		if element[3] > i:
			if element[4] == 1:
				TN += 1
			else:
				FN += 1
	TPR = TP/(TP+FN)
	FPR = FP/(FP+TN)
	PPV = TP/(TP+FP)
	TPR_array.append(TPR)
	FPR_array.append(FPR)
	PPV_array.append(PPV)
	cut_off_dict[i] = [TP, FP, TN, FN, TPR, FPR]	

#ROC curve

auc = abs(np.trapz(TPR_array, FPR_array))

plt.figure()
plt.plot(FPR_array, TPR_array, 'b', label='AUC = %0.2f' % auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1], 'r--')
plt.xlim([0, 1])
plt.ylim([0, 1.05])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.title('ROC Curve')
plt.show()

#AUC


print(auc)
#for key, value in cut_off_dict.items():
#	print("TPR: %.4f\t FPR: %.4f\n"%(value[4], value[5]))	

# Precision-recall curves
plt.figure()
plt.plot(TPR_array, PPV_array)
plt.ylabel('Precision')
plt.xlabel('Recall')
plt.title('Precision Recall Curve')
plt.show()



