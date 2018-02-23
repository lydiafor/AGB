import pickle

dataset = pickle.load(open("testing_dataset.p", "rb"))
likelihood = pickle.load(open("likelihood_filt.p", "rb"))
id_tissue = pickle.load(open("testing_tissue.p", "rb"))

#iterate testing dataset to make the tissue prediction
prediction = {}

for id_test in dataset:
	prediction[id_test] = {}
	for tissue in likelihood:
		p_tissue = 1/len(likelihood)
		prediction[id_test][tissue] = p_tissue

		for se1, psi in dataset[id_test].items():
			if se1 in likelihood[tissue]:
				if psi == "up":
					prob = likelihood[tissue][se1][0]
				elif psi == "down":
					prob = likelihood[tissue][se1][1]

				prediction[id_test][tissue] += prob

#print results of preditions

for id_test in prediction:
	#Get the real label of our ids
	for tissue, ids in id_tissue.items():
		if id_test in ids:
			real_tissue = tissue

	tissue_prediction = ""
	#Perform the prediction for our id
	n = 0
	for tiss, prob in prediction[id_test].items():
		n += 1
		if n == 1:
			max_prob = prob
			predi_tissue = tiss
		else:
			if prob > max_prob:
				max_prob = prob
				predi_tissue = tiss

	#Print the results
	print("%s\t%s\t%s\t%.5f\n" %(id_test, predi_tissue, real_tissue, max_prob))



			