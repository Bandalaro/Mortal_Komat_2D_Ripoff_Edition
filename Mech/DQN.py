import numpy as np
from collections import deque
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam


class PPOAgent:
    def __init__(self, state_size, action_size, gamma=0.95, epsilon=0.2, learning_rate=0.001, memory_size=2000,
                 entropy_loss_coef=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.memory = deque(maxlen=memory_size)
        self.actor_model = self._build_actor()
        self.critic_model = self._build_critic()

    def _build_actor(self):
        state_input = Input(shape=(self.state_size,))
        x = Dense(24, activation='relu')(state_input)
        x = Dense(24, activation='relu')(x)
        action_output = Dense(self.action_size, activation='softmax')(x)
        model = Model(inputs=state_input, outputs=action_output)
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss=self._ppo_loss)
        return model

    def _build_critic(self):
        state_input = Input(shape=(self.state_size,))
        x = Dense(24, activation='relu')(state_input)
        x = Dense(24, activation='relu')(x)
        value_output = Dense(1, activation='linear')(x)
        model = Model(inputs=state_input, outputs=value_output)
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def _ppo_loss(self, y_true, y_pred):
        advantages, old_prediction = y_true[:, :1], y_true[:, 1:]
        prob = y_pred
        ratio = tf.exp(tf.math.log(prob + 1e-10) - tf.math.log(old_prediction + 1e-10))
        clipped_ratio = tf.clip_by_value(ratio, 1 - self.epsilon, 1 + self.epsilon)
        loss = -tf.reduce_mean(tf.minimum(ratio * advantages, clipped_ratio * advantages))
        entropy_loss = -self.entropy_loss_coef * tf.reduce_mean(prob * tf.math.log(prob + 1e-10))
        return loss + entropy_loss

    def get_action(self, state):
        state = state.reshape(1, -1)
        policy = self.actor_model.predict(state, verbose=0)[0]
        action = np.random.choice(self.action_size, p=policy)
        return action, policy

    def train(self, states, actions, rewards, next_states, dones):
        states = states.reshape(-1, self.state_size)
        next_states = next_states.reshape(-1, self.state_size)
        advantages = np.zeros_like(rewards)
        target_values = np.zeros_like(rewards)

        for i in range(len(rewards)):
            if dones[i]:
                target_values[i] = rewards[i]
            else:
                next_state_value = self.critic_model.predict(next_states[i].reshape(1, -1))[0]
                target_values[i] = rewards[i] + self.gamma * next_state_value
            current_state_value = self.critic_model.predict(states[i].reshape(1, -1))[0]
            advantages[i] = target_values[i] - current_state_value

        actions_onehot = np.zeros((len(actions), self.action_size))
        actions_onehot[np.arange(len(actions)), actions] = 1

        y_true = np.hstack([advantages.reshape(-1, 1), actions_onehot])

        self.actor_model.fit(states, y_true, epochs=1, verbose=0)
        self.critic_model.fit(states, target_values, epochs=1, verbose=0)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        states = np.array([mb[0] for mb in minibatch])
        actions = np.array([mb[1] for mb in minibatch])
        rewards = np.array([mb[2] for mb in minibatch])
        next_states = np.array([mb[3] for mb in minibatch])
        dones = np.array([mb[4] for mb in minibatch])

        self.train(states, actions, rewards, next_states, dones)

    def load(self, name):
        self.actor_model.load_weights(name + '_actor.h5')
        self.critic_model.load_weights(name + '_critic.h5')

    def save(self, name):
        self.actor_model.save_weights(name + '_actor.h5')
        self.critic_model.save_weights(name + '_critic.h5')

    def get_valid_action(self, character, environment):
        """
        Ensure that the action taken by the PPO agent is valid based on character constraints.
        :param character: The character object controlled by the PPO agent.
        :param environment: The game environment to ensure valid actions.
        :return: A valid action.
        """
        state = np.array(character.position).reshape(1, -1)
        policy = self.actor_model.predict(state, verbose=0)[0]
        action = np.random.choice(self.action_size, p=policy)

        # Call the environment's method to ensure the character stays within bounds
        environment.constrain_character_position(character)

        return action
