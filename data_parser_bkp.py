import math
from pyexpat import features
import pandas as pd
import argparse

# Change this ID with the number of the scenario with best fitness



# Each scenario has two components: NPC_1 and NPC_2
def get_average_speed(data):
	speeds = []
	for i in range(len(data)):
		sum = 0.0
		for j in range(len(data[0])):
			sum = sum + data[i][j][0]
		speeds.append(sum/len(data[i]))
	return speeds

def get_number_of_lane_changes(data):
	lane_changes = []
	for i in range(len(data)):
		lc = 0
		for j in range(1, len(data[0])):
			if data[i][j][1] - data[i][j-1][1] != 0:
				lc += 1
		lane_changes.append(lc)
	return lane_changes

def get_ego_avg_speed(data):
	sum = 0.0
	for i in range(len(data)):
		sum = sum + math.sqrt(math.pow(data[i]['ego'].velocity.x, 2.0) + math.pow(data[i]['ego'].velocity.z, 2.0))
	return sum/len(data)

def get_npc_actual_speed(data, npc):
	sum = 0.0
	for i in range(len(data)):
		sum = sum + math.sqrt(math.pow(data[i][npc].velocity.x, 2.0) + math.pow(data[i][npc].velocity.z, 2.0))
	return sum/len(data)

def get_avg_distances(data):
	dist = []
	npcs = ['npc_0', 'npc_1']
	for npc in npcs:
		sum = 0.0
		for i in range(len(data)):
			sum = sum + math.sqrt(math.pow(data[i][npc].transform.position.x - data[i]['ego'].transform.position.x, 2.0) + math.pow(data[i][npc].transform.position.z - data[i]['ego'].transform.position.z, 2.0))
		dist.append(sum/len(data))
	return dist

if __name__ == '__main__':

	# Features dict to construct final csv document
	features_data = {
		'fitness': [],
		'fault': [],
		'npc1_avg_control_speed': [],
		'npc2_avg_control_speed': [],
		'npc1_number_lane_changes': [],
		'npc2_number_lane_changes': [],
		'ego_avg_speed': [],
		'npc1_avg_speed': [],
		'npc2_avg_speed': [],
		'avg_dist_ego_npc1': [],
		'avg_dist_ego_npc2': []
	}

	total_number_scenarios = 475

	for i in range(total_number_scenarios):
		scenario_file = "scenarios/scenario_" + str(i) + ".obj"
		results_file = "results/scenario_" + str(i) + ".obj"
		records_file = "records/scenario_" + str(i) + ".obj"

		# Get avg NPC speed and Number of lane changes
		scenario_data = pd.read_pickle(scenario_file)
		avg_control_speed = get_average_speed(scenario_data)
		lane_change = get_number_of_lane_changes(scenario_data)

		# Get fitness and fault from the results object
		results_data = pd.read_pickle(results_file)
	
		# Get average ego and npc average actual speed and average distance to npc

		record_data = pd.read_pickle(records_file)
		pos_data = record_data['frames']
		ego_avg_speed = get_ego_avg_speed(pos_data)
		npc1_avg_speed = get_npc_actual_speed(pos_data, 'npc_0')
		npc2_avg_speed = get_npc_actual_speed(pos_data, 'npc_1')
		avg_distances = get_avg_distances(pos_data)

		features_data['fitness'].append(results_data['fitness'])
		features_data['fault'].append(results_data['fault'][0])
		features_data['npc1_avg_control_speed'].append(avg_control_speed[0])
		features_data['npc2_avg_control_speed'].append(avg_control_speed[1])
		features_data['npc1_number_lane_changes'].append(lane_change[0])
		features_data['npc2_number_lane_changes'].append(lane_change[1])
		features_data['ego_avg_speed'].append(ego_avg_speed)
		features_data['npc1_avg_speed'].append(npc1_avg_speed)
		features_data['npc2_avg_speed'].append(npc2_avg_speed)
		features_data['avg_dist_ego_npc1'].append(avg_distances[0])
		features_data['avg_dist_ego_npc2'].append(avg_distances[1])

	features = pd.DataFrame.from_dict(features_data)
	features.to_csv("features.csv", index=False)
	




