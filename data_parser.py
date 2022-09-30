import math
from pyexpat import features
import pandas as pd
import argparse
import numpy as np

# Change this ID with the number of the scenario with best fitness



# Each scenario has two components: NPC_1 and NPC_2
def get_average_speed(data):
	array = np.ndarray([len(data[0]), 1])
	speeds = []
	for i in range(len(data)):
		# sum = 0.0
		for j in range(len(data[0])):
			array[j] = data[i][j][0]
		speeds.append(array.mean())
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

def get_actor_data_speed(data, actor):
	sum = np.ndarray([len(data),1])
	stats = []
	for i in range(len(data)):
		sum[i] = math.sqrt(math.pow(data[i][actor].velocity.x, 2.0) + math.pow(data[i][actor].velocity.z, 2.0))
	stats.append(sum.mean())
	stats.append(sum.min())
	stats.append(sum.max())
	stats.append(np.std(sum))
	return stats

def get_avg_distances(data):
	dist = [[],[]]
	npcs = ['npc_0', 'npc_1']
	x = 0
	for npc in npcs:
		sum = np.ndarray(len(data))
		for i in range(len(data)):
			sum[i] = math.sqrt(math.pow(data[i][npc].transform.position.x - data[i]['ego'].transform.position.x, 2.0) + math.pow(data[i][npc].transform.position.z - data[i]['ego'].transform.position.z, 2.0))
		dist[x].append(sum.mean())
		dist[x].append(sum.min())
		dist[x].append(sum.max())
		dist[x].append(np.std(sum))
		x += 1
	return dist

def get_min_max_std_control_speed(data):
	array = np.ndarray([len(data[0]), 1])
	speeds = []
	for i in range(len(data)):
		# sum = 0.0
		for j in range(len(data[0])):
			array[j] = data[i][j][0]
		speeds.append([array.min(), array.max(), np.std(array)])
	return speeds

def get_accel_data(data, actor):
	sum = np.ndarray([len(data), 1])
	stats = []
	for i in range(len(data)):
		if i == 0:
			sum[i] = 0.0
		else:
			# accel_x = (data[i][actor].velocity.x - data[i-1][actor].velocity.x)/0.1
			# accel_z = (data[i][actor].velocity.z - data[i-1][actor].velocity.z)/0.1
			# sum[i] = math.sqrt(math.pow(accel_x, 2.0) + math.pow(accel_z, 2.0))
			v_f = math.sqrt(math.pow(data[i][actor].velocity.x, 2.0) + math.pow(data[i][actor].velocity.z, 2.0))
			v_o = math.sqrt(math.pow(data[i-1][actor].velocity.x, 2.0) + math.pow(data[i-1][actor].velocity.z, 2.0))
			sum[i] = (v_f-v_o)/0.1
	stats.append(sum.mean())
	stats.append(sum.min())
	stats.append(sum.max())
	stats.append(np.std(sum))

	return stats


if __name__ == '__main__':

	# Features dict to construct final csv document
	features_data = {
		'fitness': [],
		'fault': [],
		'npc1_avg_control_speed': [],
		'npc1_min_control_speed': [],
		'npc1_max_control_speed': [],
		'npc1_std_control_speed': [],
		'npc2_avg_control_speed': [],
		'npc2_min_control_speed': [],
		'npc2_max_control_speed': [],
		'npc2_std_control_speed': [],
		'npc1_number_lane_changes': [],
		'npc2_number_lane_changes': [],
		'ego_avg_speed': [],
		'ego_min_speed': [],
		'ego_max_speed': [],
		'ego_std_speed': [],
		'npc1_avg_speed': [],
		'npc1_min_speed': [],
		'npc1_max_speed': [],
		'npc1_std_speed': [],
		'npc2_avg_speed': [],
		'npc2_min_speed': [],
		'npc2_max_speed': [],
		'npc2_std_speed': [],
		'avg_dist_ego_npc1': [],
		'min_dist_ego_npc1': [],
		'max_dist_ego_npc1': [],
		'std_dist_ego_npc1': [],
		'avg_dist_ego_npc2': [],
		'min_dist_ego_npc2': [],
		'max_dist_ego_npc2': [],
		'std_dist_ego_npc2': [],
		'ego_avg_accel': [],
		'ego_min_accel': [],
		'ego_max_accel': [],
		'ego_std_accel': [],
		'npc1_avg_accel': [],
		'npc1_min_accel': [],
		'npc1_max_accel': [],
		'npc1_std_accel': [],
		'npc2_avg_accel': [],
		'npc2_min_accel': [],
		'npc2_max_accel': [],
		'npc2_std_accel': []
	}

	total_number_scenarios = 404

	for i in range(total_number_scenarios):
		scenario_file = "scenarios/scenario_" + str(i) + ".obj"
		results_file = "results/scenario_" + str(i) + ".obj"
		records_file = "records/scenario_" + str(i) + ".obj"

		# Get avg NPC speed and Number of lane changes
		scenario_data = pd.read_pickle(scenario_file)
		avg_control_speed = get_average_speed(scenario_data)
		lane_change = get_number_of_lane_changes(scenario_data)
		minmax_npcs = get_min_max_std_control_speed(scenario_data)

		# Get fitness and fault from the results object
		results_data = pd.read_pickle(results_file)
	
		# Get average ego and npc average actual speed and average distance to npc

		record_data = pd.read_pickle(records_file)
		pos_data = record_data['frames']
		ego_data_speed = get_actor_data_speed(pos_data, 'ego')
		npc1_data_speed = get_actor_data_speed(pos_data, 'npc_0')
		npc2_data_speed = get_actor_data_speed(pos_data, 'npc_1')
		avg_distances = get_avg_distances(pos_data)
		ego_data_accel = get_accel_data(pos_data, 'ego')
		npc1_data_accel = get_accel_data(pos_data, 'npc_0')
		npc2_data_accel = get_accel_data(pos_data, 'npc_1')

		features_data['fitness'].append(results_data['fitness'])
		features_data['fault'].append(results_data['fault'][0])
		features_data['npc1_avg_control_speed'].append(avg_control_speed[0])
		features_data['npc1_min_control_speed'].append(minmax_npcs[0][0])
		features_data['npc1_max_control_speed'].append(minmax_npcs[0][1])
		features_data['npc1_std_control_speed'].append(minmax_npcs[0][2])
		features_data['npc2_avg_control_speed'].append(avg_control_speed[1])
		features_data['npc2_min_control_speed'].append(minmax_npcs[1][0])
		features_data['npc2_max_control_speed'].append(minmax_npcs[1][1])
		features_data['npc2_std_control_speed'].append(minmax_npcs[1][2])
		features_data['npc1_number_lane_changes'].append(lane_change[0])
		features_data['npc2_number_lane_changes'].append(lane_change[1])
		features_data['ego_avg_speed'].append(ego_data_speed[0])
		features_data['ego_min_speed'].append(ego_data_speed[1])
		features_data['ego_max_speed'].append(ego_data_speed[2])
		features_data['ego_std_speed'].append(ego_data_speed[3])
		features_data['npc1_avg_speed'].append(npc1_data_speed[0])
		features_data['npc1_min_speed'].append(npc1_data_speed[1])
		features_data['npc1_max_speed'].append(npc1_data_speed[2])
		features_data['npc1_std_speed'].append(npc1_data_speed[3])
		features_data['npc2_avg_speed'].append(npc2_data_speed[0])
		features_data['npc2_min_speed'].append(npc2_data_speed[1])
		features_data['npc2_max_speed'].append(npc2_data_speed[2])
		features_data['npc2_std_speed'].append(npc2_data_speed[3])
		features_data['avg_dist_ego_npc1'].append(avg_distances[0][0])
		features_data['min_dist_ego_npc1'].append(avg_distances[0][1])
		features_data['max_dist_ego_npc1'].append(avg_distances[0][2])
		features_data['std_dist_ego_npc1'].append(avg_distances[0][3])
		features_data['avg_dist_ego_npc2'].append(avg_distances[1][0])
		features_data['min_dist_ego_npc2'].append(avg_distances[1][1])
		features_data['max_dist_ego_npc2'].append(avg_distances[1][2])
		features_data['std_dist_ego_npc2'].append(avg_distances[1][3])
		features_data['ego_avg_accel'].append(ego_data_accel[0])
		features_data['ego_min_accel'].append(ego_data_accel[1])
		features_data['ego_max_accel'].append(ego_data_accel[2])
		features_data['ego_std_accel'].append(ego_data_accel[3])
		features_data['npc1_avg_accel'].append(npc1_data_accel[0])
		features_data['npc1_min_accel'].append(npc1_data_accel[1])
		features_data['npc1_max_accel'].append(npc1_data_accel[2])
		features_data['npc1_std_accel'].append(npc1_data_accel[3])
		features_data['npc2_avg_accel'].append(npc2_data_accel[0])
		features_data['npc2_min_accel'].append(npc2_data_accel[1])
		features_data['npc2_max_accel'].append(npc2_data_accel[2])
		features_data['npc2_std_accel'].append(npc2_data_accel[3])


	features = pd.DataFrame.from_dict(features_data)
	features.to_csv("features.csv", index=False)
	




