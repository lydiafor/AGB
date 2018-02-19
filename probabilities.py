import pickle
import math

dataset = pickle.load(open("training.p", "rb"))
se_events = pickle.load(open("se_events.p", "rb"))

#Calculate probabilities

prob_se = {}

for se, psi in se_events.items():
	n = len(psi)
	if n == 0:
		continue
	else:
		prob_se[se] = {}
		p_up = psi.count("up") / n
		p_down = psi.count("down") / n
		prob_se[se]["up"] = p_up
		prob_se[se]["down"] = p_down


likelihood = {}
relative_entropy = {}
total_entropy = 0

for tissue in dataset:
	likelihood[tissue] = {}
	p_tissue = 1/len(dataset)
	entropy_tissue = -(p_tissue * math.log(p_tissue))
	total_entropy += entropy_tissue
	
	for se, psi in dataset[tissue].items():
		n = len(psi)
		if n == 0:
			continue
		else:
			jointp_up = psi.count("up") / n
			jointp_down = psi.count("down") / n
			p_se_up = prob_se[se]["up"]
			p_se_down = prob_se[se]["down"]

			
			if p_se_up == 0 or jointp_up == 0:
				condp_up = 0
				rel_entrp_up = 0
			else:
				condp_up = jointp_up / p_se_up
				rel_entrp_up = jointp_up * math.log(jointp_up / p_se_up)

			if p_se_down == 0 or jointp_down == 0:
				condp_down = 0
				rel_entrp_down = 0
			else:
				condp_down = jointp_down / p_se_down
				rel_entrp_down = jointp_down * math.log(jointp_down / p_se_down)

			lik_up = (condp_up * p_se_up) 
			lik_down = (condp_down * p_se_down)

			likelihood[tissue][se] = tuple([lik_up, lik_down])

			rel_entrp = rel_entrp_up + rel_entrp_down

			if se not in relative_entropy:
				relative_entropy[se] = rel_entrp
			else:
				relative_entropy[se] += rel_entrp

mutual_information = []

for se, rel_entr in relative_entropy.items():
	mut_inf = total_entropy - rel_entr
	data = tuple([se, mut_inf])
	mutual_information.append(data)

mutual_information_sorted = sorted(mutual_information, key=lambda x: x[1], reverse=True)
print(mutual_information_sorted)

