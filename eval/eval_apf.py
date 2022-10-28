import gym, gym_depth_planning
import numpy as np

from gym_depth_planning.apf.potential_field_continuous import ApfAgent
from gym_depth_planning.utils.obstacle_randomizer import ObstacleRandomizer
from stable_baselines3.common.vec_env import DummyVecEnv

agent = ApfAgent()
env = gym.make("depth_planner-v0", no_dynamics=True)
env = DummyVecEnv([lambda: env])
obs = env.reset()

env_configurations = ['route0', 'route1', 'route2',  'route3', 'route4', 'route5']
randomizer = ObstacleRandomizer(env.envs[0].env.model_name)
env_conf = env_configurations[5]
randomizer.reload_environment('./environments/' + env_conf + '.npy')

episode_times = np.zeros((4, 6, 10))
finish_passed = np.zeros((4, 6, 10))
final_position = np.zeros((4, 6, 10))
safety_cost = np.zeros((4, 6, 10))

env.envs[0].env.start_x = -10
env.envs[0].env.forward_direction = True
env.envs[0].env.target_y_list = [0]

model_num = 0

for route_count, env_conf in enumerate(env_configurations):

    episode_finish_count = 0
    for episode_count in range(10):
        print("episode: ", episode_count)

        obs = env.envs[0].env.reset()
        randomizer.reload_environment('./environments/' + env_conf + '.npy')
        safety_cost_list = []
        for i in range(5002):  # breaks at the end of the episode
            action = agent.compute_action(obs)
            obs, rewards, dones, info = env.envs[0].env.step(action)
            if info["closer_object"] < 1.5:
                safety_cost_list.append(1 / info["closer_object"])
            if dones:
                finish_passed[model_num, route_count, episode_count] = info['finish_passed']
                final_position[model_num, route_count, episode_count] = info['current_position'].x
                episode_finish_count += info['finish_passed']
                if safety_cost_list == []:
                    safety_cost_list = [0]
                safety_cost[model_num, route_count, episode_count] = np.mean(safety_cost_list)
                print("finish_passed:", info['finish_passed'])
                break
    # np.save("safetycost", safety_cost)
    # np.save("final_pose-apf", final_position)
    # np.save("finish_passed-apf", finish_passed)

