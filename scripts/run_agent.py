import gymnasium as gym
from stable_baselines3 import PPO, SAC
from gym_pathfinding.envs.pathfinding_env import PathfindingEnv
from gym_pathfinding.envs.visualization import Renderer  # If you want to visualize the environment

model_name = "sac_pathfinding_2025-06-10_07-43-11_24_50"
# Load the trained model
model = SAC.load(f"/home/bake/Projects/Rest-to-Rest/models/{model_name}.zip")  # Make sure this path matches your saved model

# Create the environment
env = PathfindingEnv(
    number_of_obstacles=10, 
    bounds=[[0, 0], [100, 100]], 
    bounce_factor=1, 
    num_lidar_scans=24, 
    lidar_max_range=50,
    random_start_target=True,
    terminate_on_collision=False,
    obstacle_max_size=5,
    obstacle_min_size=1
)


# Initialize the renderer (if visualization is needed)
renderer = Renderer(env, record=True, video_path=f"/home/bake/Projects/Rest-to-Rest/Videos/inference_video_{model_name}.mp4")

# Reset the environment
obs, _ = env.reset()
done = False

while not done:
    # Get action from trained model
    action, _ = model.predict(obs)

    # Take a step in the environment
    obs, reward, done, truncated, info = env.step(action)

    # Render the environment
    renderer.render(env.agent, env.obstacle_manager, env.target_position)

# Save the video and close the renderer
renderer.save_video()
print("Inference completed!")
