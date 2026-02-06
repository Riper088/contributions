# Educational Tutorial: Training an AI to Play Chrome Dinosaur Game with Reinforcement Learning

# Learning Objective:
# This tutorial teaches the fundamental concepts of Reinforcement Learning (RL)
# by training a simple AI agent to play the Google Chrome Dinosaur game.
# We will focus on the core idea of an agent interacting with an environment,
# receiving rewards, and learning a policy to maximize those rewards.
# This example uses a simplified approach to keep it beginner-friendly.

# --- Prerequisites ---
# You'll need to have Python installed.
# You'll also need a way to interact with the Chrome Dinosaur game.
# For simplicity, this code *simulates* the game's environment and interactions.
# In a real-world scenario, you'd use libraries like Selenium or PyAutoGUI
# to control the browser and capture game state.

# --- Core Concepts Explained ---
# Reinforcement Learning (RL):
# Imagine teaching a dog a trick. You give it a treat (reward) when it does something right.
# Over time, the dog learns which actions lead to treats. RL works similarly.
# - Agent: The AI we are training (our "dinosaur").
# - Environment: The game world (the Chrome Dinosaur game).
# - State: The current situation in the environment (e.g., dinosaur's position, obstacle positions, speed).
# - Action: What the agent can do (e.g., jump, duck, do nothing).
# - Reward: A signal from the environment indicating how good or bad an action was.
#   - Positive reward: For surviving, for moving forward.
#   - Negative reward: For hitting an obstacle.
# - Policy: The agent's strategy for choosing actions based on the current state.
#   Our goal is to learn an optimal policy.

# --- Simplified Environment Simulation ---
# We'll create a basic class to represent the game environment.
# This avoids the complexity of actual browser interaction for educational purposes.
import random

class DinoGameEnvironment:
    def __init__(self):
        # Game state variables
        self.dino_y = 0  # Dinosaur's vertical position (0 = ground, >0 = jumping)
        self.obstacles = [] # List of obstacles: (distance_from_dino, height)
        self.score = 0
        self.game_over = False
        self.game_speed = 1 # How fast obstacles approach

    def reset(self):
        # Resets the game to its initial state
        self.dino_y = 0
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.game_speed = 1
        return self._get_state() # Return the initial state

    def _get_state(self):
        # Represents the current state of the game.
        # For simplicity, we'll use a few key features.
        # In a real game, this would be pixel data or more detailed game info.
        closest_obstacle_dist = float('inf')
        closest_obstacle_height = 0
        if self.obstacles:
            closest_obstacle_dist = min(self.obstacles, key=lambda obs: obs[0])[0]
            closest_obstacle_height = min(self.obstacles, key=lambda obs: obs[0])[1]

        # Return a simplified state: (dino_y, closest_obstacle_dist, closest_obstacle_height)
        # A real agent might need more features or raw pixel data.
        return (self.dino_y, closest_obstacle_dist, closest_obstacle_height)

    def step(self, action):
        # Takes an action and returns the next state, reward, and whether the game is over.
        # Actions: 0 = Do nothing, 1 = Jump, 2 = Duck (we'll simplify and only consider jump/nothing for now)
        # Let's redefine actions for simplicity: 0 = Nothing, 1 = Jump

        reward = 0 # Default reward

        if self.game_over:
            return self._get_state(), 0, True # No action if game over

        # Simulate obstacle movement and spawning
        self.score += 1
        if random.random() < 0.05 * self.game_speed: # Probability of spawning an obstacle
            self.obstacles.append([300, random.choice([20, 40])]) # (initial_distance, height)

        # Move obstacles towards the dino
        for i in range(len(self.obstacles)):
            self.obstacles[i][0] -= self.game_speed
        self.obstacles = [obs for obs in self.obstacles if obs[0] > -20] # Remove obstacles that passed

        # Process dinosaur actions
        if action == 1 and self.dino_y == 0: # If action is Jump and dino is on ground
            self.dino_y = 60 # Simulate jumping up
            reward += 1 # Small reward for a successful action
        elif self.dino_y > 0: # If dino is in the air
            self.dino_y -= 15 # Simulate coming down
            if self.dino_y < 0:
                self.dino_y = 0 # Ensure dino lands on the ground
            reward += 0.1 # Small reward for continuing to jump (if needed)

        # Check for collisions
        for obs_dist, obs_height in self.obstacles:
            if -10 < obs_dist < 10 and self.dino_y < obs_height: # Collision detected
                self.game_over = True
                reward = -100 # Large negative reward for crashing
                break # No need to check other obstacles

        # Reward for surviving each step
        if not self.game_over:
            reward += 0.5

        # Increase game speed gradually
        if self.score % 100 == 0:
            self.game_speed += 0.1

        return self._get_state(), reward, self.game_over

# --- Simple Reinforcement Learning Agent ---
# We'll use a very basic Q-learning-like approach.
# Q-learning is a popular RL algorithm that learns an action-value function (Q-function).
# The Q-function estimates the expected future reward of taking a specific action in a specific state.
# Q(state, action) = Reward + DiscountFactor * MaxQ(next_state, all_actions)

class SimpleDinoAgent:
    def __init__(self, num_actions=2): # 0: Nothing, 1: Jump
        self.num_actions = num_actions
        # We'll use a dictionary to store Q-values.
        # Keys will be (state, action) tuples.
        # For a real game, states would be more complex, possibly requiring a neural network.
        self.q_table = {}
        self.learning_rate = 0.1 # How much we update Q-values based on new info
        self.discount_factor = 0.99 # How much we value future rewards

    def get_q_value(self, state, action):
        # Safely retrieve Q-value, defaulting to 0 if not seen before.
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, epsilon=0.1):
        # Epsilon-greedy action selection:
        # With probability epsilon, explore (choose a random action).
        # With probability 1-epsilon, exploit (choose the best known action).
        if random.random() < epsilon:
            # Explore: Choose a random action
            return random.randrange(self.num_actions)
        else:
            # Exploit: Choose the action with the highest Q-value for the current state
            q_values = [self.get_q_value(state, a) for a in range(self.num_actions)]
            max_q = max(q_values)
            # If multiple actions have the same max Q-value, pick one randomly.
            best_actions = [a for a, q in enumerate(q_values) if q == max_q]
            return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        # Update the Q-value for the (state, action) pair.
        current_q = self.get_q_value(state, action)

        # Find the maximum Q-value for the next state across all possible actions.
        next_q_values = [self.get_q_value(next_state, a) for a in range(self.num_actions)]
        max_next_q = max(next_q_values) if next_q_values else 0.0 # Handle cases with no next_state Q-values

        # The core Q-learning update rule:
        # New Q = Current Q + LearningRate * (Reward + DiscountFactor * MaxNextQ - Current Q)
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)

        # Store the updated Q-value in the Q-table.
        self.q_table[(state, action)] = new_q

# --- Training Loop ---
def train_agent(episodes=1000):
    env = DinoGameEnvironment()
    agent = SimpleDinoAgent()
    total_rewards = []

    print("Starting training...")
    for episode in range(episodes):
        state = env.reset()
        done = False
        episode_reward = 0

        while not done:
            # Agent chooses an action based on the current state (with exploration).
            action = agent.choose_action(state, epsilon=0.1) # Epsilon slowly decreases in real agents.

            # Environment simulates the action and returns the next state, reward, and game status.
            next_state, reward, done = env.step(action)

            # Agent learns from the experience: updates its Q-values.
            agent.learn(state, action, reward, next_state)

            # Update current state and accumulate reward.
            state = next_state
            episode_reward += reward

        total_rewards.append(episode_reward)

        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{episodes}, Score: {env.score}, Total Reward: {episode_reward:.2f}")

    print("Training finished.")
    return total_rewards

# --- Example Usage ---
if __name__ == "__main__":
    # Train the agent for a number of episodes.
    # For this simple simulation, 1000 episodes is a good starting point.
    # For a real game, this would take much longer and require more sophisticated state representation.
    training_rewards = train_agent(episodes=1000)

    # Now let's see the trained agent play!
    print("\n--- Testing Trained Agent ---")
    env = DinoGameEnvironment()
    agent = SimpleDinoAgent() # Load the learned Q-table (in this case, it's in the global agent object)
    # In a real scenario, you would save and load the q_table.

    # For demonstration, let's directly use the trained agent's Q-table by re-initializing it
    # with the same q_table from the training session (this is a simplification).
    # A better approach is to save/load the q_table from agent.q_table.

    # Re-create agent and assume it has learned the Q-values
    trained_agent = SimpleDinoAgent()
    trained_agent.q_table = agent.q_table # This is a hack for this example.
                                         # In practice, you'd serialize and deserialize.

    state = env.reset()
    done = False
    score = 0
    print("Agent playing (no learning during this phase, only exploitation):")
    while not done:
        # Agent chooses the BEST action based on learned Q-values (no exploration).
        # We set epsilon to 0 for pure exploitation.
        action = trained_agent.choose_action(state, epsilon=0.0)
        next_state, reward, done = env.step(action)

        state = next_state
        score += 1 # Score increases each step the game is not over

        # Optional: Print game state for visualization (can slow down simulation)
        # print(f"State: {state}, Action: {action}, Reward: {reward}, Score: {score}")

    print(f"\nAgent finished with Score: {score}")
    print(f"Final game speed: {env.game_speed:.2f}")
    print(f"Number of Q-table entries: {len(trained_agent.q_table)}")

    # Visualizing rewards over episodes can show learning progress.
    # You could use matplotlib for plotting.
    # import matplotlib.pyplot as plt
    # plt.plot(training_rewards)
    # plt.xlabel("Episode")
    # plt.ylabel("Total Reward")
    # plt.title("Agent's Reward Over Time")
    # plt.show()