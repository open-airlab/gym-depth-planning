from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.callbacks import CheckpointCallback
import gym, gym_depth_planning
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import rc
import rospy
import pickle
from gym_depth_planning.utils.obstacle_randomizer import ObstacleRandomizer


env = gym.make("depth_planner-v0", no_dynamics=True)

env = DummyVecEnv([lambda: env])
randomizer = ObstacleRandomizer(env.envs[0].env.model_name)

model_dirs = ["../train/trained_models/scdp_rl_model_100000_steps.zip", "../train/trained_models/cdp_rl_model_100000_steps.zip", "../train/trained_models/ddp_rl_model_100000_steps.zip"]

env_configurations = ['route0', 'route1', 'route2',  'route3', 'route4', 'route5']

episode_times = np.zeros((4, 6, 10))
finish_passed = np.zeros((4, 6, 10))
final_position = np.zeros((4, 6, 10))
safety_cost = np.zeros((4, 6, 10))

env.envs[0].env.start_x = -10
env.envs[0].env.forward_direction = True
env.envs[0].env.target_y_list = [0]

for model_num, model_dir in enumerate(model_dirs):
    model = PPO.load(model_dir)
    if model_num < 2:
        env = gym.make("depth_planner-v0", no_dynamics=True)
        env = DummyVecEnv([lambda: env])
    else:
        env = gym.make("depth_planner-v0", no_dynamics=True, discrete_actions=True)
        env = DummyVecEnv([lambda: env])
    env.envs[0].env.start_x = -10
    env.envs[0].env.forward_direction = True
    env.envs[0].env.target_y_list = [0]
    for route_count, env_conf in enumerate(env_configurations):
        episode_finish_count = 0
        for episode_count in range(10):
            print("episode: ", episode_count)

            obs = env.envs[0].env.reset()
            randomizer.reload_environment('./environments/' + env_conf + '.npy')
            # start_time = clock
            episode_safety_cost = 0
            safety_cost_list = []
            length_list = []
            for i in range(5002):  # breaks at the end of the episode
                action, _states = model.predict(obs, deterministic=True)
                # print(action)
                obs, rewards, dones, info = env.envs[0].env.step(action)
                if info["closer_object"] < 1.5:
                    safety_cost_list.append(1/info["closer_object"])
                length_list.append(info["closer_object"])
                if dones:
                    finish_passed[model_num, route_count, episode_count] = info['finish_passed']
                    final_position[model_num, route_count, episode_count] = info['current_position'].x
                    episode_finish_count += info['finish_passed']
                    if safety_cost_list == []:
                        safety_cost_list = [0]
                    safety_cost[model_num, route_count, episode_count] = np.mean(safety_cost_list)
                    print("finish_passed:", info['finish_passed'])
                    break
        # np.save("safety_cost", safety_cost)
        # np.save("final_pose", final_position)
        # np.save("finish_passed", finish_passed)


