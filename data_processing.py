import random

#Funtion to extract info for tissue descriptio
def get_ids_for_tissue(file_name):
	"""Return a dictionary with all ids for each tissue """
	
	f_tissue = open(file_name)
	tissue_dic = {}
	
	for line in f_tissue:
		elements = line.split()
		tissue_dic[elements[0]] = elements[2]
	return tissue_dic

#Function ti extract information about psi values of certain se events in all ids

def get_psi_se_for_ids(file_name):
	f_se = open(file_name)
	id_se_psi = {}

	for line in f_se:
		line = line.strip()
		if line.startswith("GTEX"):
			ids = line.split("\t")

	else:
		elements = line.split("\t")
		se_event = elements[0]
		psi_val = elements[1:]

		for i in range(len(ids)):
			if ids[i] not in id_se_psi:
				id_se_psi[ids[i]] = {}

			if se_event not in id_se_psi[ids[i]].keys():
				id_se_psi[ids[i]][se_event] = psi_val[i]

	return id_se_psi

#Function to merge both files and obtain the psi values for each event for each tissue

def get_psi_se_for_tissues(psis, tisues):
	tissue_psi = {}

	for id_sample in psis.keys():
		tissue = tisues[id_sample]
		if tissue not in tissue_psi:
			tissue_psi[tissue] = {}
	
		for se, psi in psis[id_sample].items():
			if psi == "NA":
				continue

			if se not in tissue_psi[tissue].keys():
				tissue_psi[tissue][se] = [psi]
			else:
				tissue_psi[tissue][se].append(psi)

	return(tissue_psi)

#Function to create training and testing set

def create_data_sets(dic):
	training_set = {}
	testing_set = {}

	for tissue in dic:
		training_set[tissue] = {}
		testing_set[tissue] = {}
		for se, psi in dic[tissue].items():
			n_psi = len(psi)
			n_test = round((n_psi)/3)
			
			testing = random.sample(psi, n_test)
			training = [p for p in psi if p not in testing or p == "1.0"]
			testing_set[tissue][se] = testing
			training_set[tissue][se] = training

	return(testing_set, training_set)


#Function to discretize psi values to up and down

def discretize_psi(dic):
	for tissue in dic:
		for psi in dic[tissue].values():
			for i in range(len(psi)):
				if float(psi[i]) >= 0.5:
					psi[i] = "up"
				elif float(psi[i]) < 0.5:
					psi[i] = "down"
				
	return(dic)

dic1 = get_ids_for_tissue("tissue_types.txt")
dic2 = get_psi_se_for_ids("se_events.txt")
dic3 = get_psi_se_for_tissues(dic2, dic1)

testing = create_data_sets(dic3)[0]
training = create_data_sets(dic3)[1]

testing_discr = discretize_psi(testing)
training_discr = discretize_psi(training)





