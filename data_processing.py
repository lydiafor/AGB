import pickle
import random

#Funtion to extract all ids for each tissue
def get_ids_for_tissue(file_name):
	"""Return a dictionary with all ids for each tissue """
	
	f_tissue = open(file_name)
	tissue_dic = {}

	for line in f_tissue:
		elements = line.split()
		tissue = elements[2]
		id_sample = elements[0]
		if tissue != "Kidney":#we avoid kidney data because it has very few samples
			if tissue not in tissue_dic:
				tissue_dic[tissue] = [id_sample]
			else:
				tissue_dic[tissue].append(id_sample)

	f_tissue.close()
	return (tissue_dic)


tissue_ids = get_ids_for_tissue("tissue_types.txt")


#Function to create training and testing dataset

def create_data_sets(dic):
	training_set = {}
	testing_set = {}

	for tissue, ids in dic.items():			
		training = random.sample(ids, 100) #we select a training data of 100 samples for each tissue
		testing = [i for i in ids if i not in training]
		testing_set[tissue] = testing
		training_set[tissue] = training
	
	return(testing_set, training_set)

#Run the function to obtain ids for each dataset
datasets = create_data_sets(tissue_ids)
testing_ids = datasets[0]
training_ids = datasets[1]

#Store the tissues for testing ids
ftest = open("testing_tissue.p", "wb")
pickle.dump(testing_ids, ftest)
ftest.close()


#Function to extract psi values of each se event for all ids and all psi for each se event

def get_psi_for_ids(file_name):
	f_se = open(file_name)
	fo_se = open("psi_for_se.p", "wb")
	id_se_psi = {}
	se_psi = {}

	for line in f_se:
		line = line.strip()
		if line.startswith("GTEX"):
			ids = line.split("\t")

		else:
			elements = line.split("\t")
			se_event = elements[0]
			psi_val = elements[1:]
			se_psi[se_event] = []
			
			#Discretize psi values for each se event
			for p in psi_val:
				if p != "NA":
					if float(p) >= 0.5:
						pd = "up"
					elif float(p) < 0.5:
						pd = "down"
					
					se_psi[se_event].append(pd)

			for i in range(len(ids)):
				if ids[i] not in id_se_psi:
					id_se_psi[ids[i]] = {}

				if se_event not in id_se_psi[ids[i]].keys():
					id_se_psi[ids[i]][se_event] = psi_val[i]

	pickle.dump(se_psi, fo_se)
	fo_se.close()
	f_se.close()

	return id_se_psi

dic_ids = get_psi_for_ids("se_events.txt")

#Obtain the psi values for each id of testing dataset and export the dictionary

def create_testing_dataset(psi_ids, testing_ids):
	testing = {}
	ft = open("testing_dataset.p", "wb")

	for tissue, ids in testing_ids.items():
		for id1 in psi_ids.keys():
			if id1 in ids:
				testing[id1] = {}
				for se, psi in psi_ids[id1].items():
					if psi != "NA":
						#Discretize testing psis
						if float(psi) >= 0.5:
							testing[id1][se] = "up"
						elif float(psi) <= 0.5:
							testing[id1][se] = "down"

	pickle.dump(testing, ft)
	ft.close()

#Run function to export the testing set
create_testing_dataset(dic_ids, testing_ids)

#Function to create the training dataset with psi for each event for each tissue.
def create_training_dataset(psi_ids, training_ids):
	training = {}
	ft = open("training_dataset.p", "wb")

	for tissue, ids in training_ids.items():
		training[tissue] = {}
		for id1 in ids:			
			for id2 in psi_ids.keys():
				if id1 == id2:
					for se, psi in psi_ids[id2].items():
						if psi != "NA":
							#Discretize training psis
							if float(psi) >= 0.5:
								p = "up"
							elif float(psi) < 0.5:
								p = "down"

							if se not in training[tissue].keys():
								training[tissue][se] = [p]
							else:
								training[tissue][se].append(p)

	pickle.dump(training, ft)
	ft.close()

#Run function to export training dataset
create_training_dataset(dic_ids, training_ids)

