import pickle
import math

dataset = pickle.load(open("training_dataset.p", "rb"))
se_events = pickle.load(open("psi_for_se.p", "rb"))

##Calculate probabilities up/down for each se event

prob_se = {}

for se, psi in se_events.items():
	n = len(psi)
	if n == 0:
		continue
	else:
		prob_se[se] = {}
		p_up = psi.count("up") / n
		p_down = psi.count("down") / n
		prob_se[se] = (p_up, p_down)

#compute likelihoods for each tissue/event

likelihood = {}
relative_entropy = {}

for tissue in dataset:
	likelihood[tissue] = {}
	p_tissue = 1/len(dataset) #Consider uniform prior probabilities
	
	for se, psi in dataset[tissue].items():
		n = len(psi)

		#likelihood for each se event and pair values up/down
		like_up = psi.count("up") / 100
		like_down = psi.count("down") / 100

		if like_up == 0:
			log_lik_up = -999
		else:
			log_lik_up = math.log2(like_up)

		if like_down == 0:
			log_lik_down = -999
		else:
			log_lik_down = math.log2(like_down) 
		
		likelihood[tissue][se] = (log_lik_up, log_lik_down)

		#relative entropy

		if n > 0:
			jointp_up = psi.count("up") / n
			jointp_down = psi.count("down") / n

			if jointp_up == 0:
				log_joint_up = -999
			else:
				log_joint_up = math.log2(jointp_up)

			if jointp_down == 0:
				log_joint_down = -999
			else:
				log_joint_down = math.log2(jointp_down)

		
			if prob_se[se][0] == 0:
				log_se_up = -999
			else:
				log_se_up = math.log2(prob_se[se][0])

			if prob_se[se][1] == 0:
				log_se_down = -999
			else:
				log_se_down = math.log2(prob_se[se][1])
			
			
			rel_entr_up = jointp_up * (log_joint_up - log_se_up)
			rel_entr_down = jointp_down * (log_joint_down - log_se_down)

			rel_entropy = rel_entr_up + rel_entr_down

			if se not in relative_entropy:
				relative_entropy[se] = rel_entropy
			else:
				relative_entropy[se] += rel_entropy


#Compute mutual information for each tissue/se event

total_entropy = math.log2(len(dataset)) #uniform prior probabilities

mutual_information = []

#Compute the mutual information for each 
for se, rel_entr in relative_entropy.items():
	mut_inf = total_entropy - rel_entr
	if mut_inf < 0:
		mut_inf = 0

	data = tuple([se, mut_inf])
	mutual_information.append(data)

mutual_information_sorted = sorted(mutual_information, key=lambda x: x[1], reverse=True)

best_attributes = []
for element in mutual_information_sorted:
	if element[1] > 2:
		best_attributes.append(element[0])

likelihood_filtered = {}

for tissue in likelihood:
	likelihood_filtered[tissue] = {}
	for se, lik in likelihood[tissue].items():
		if se in best_attributes:
			likelihood_filtered[tissue][se] = lik

fl = open("likelihood_filt.p", "wb")
pickle.dump(likelihood_filtered, fl)
fl.close()


