import torch
import torch.nn as nn
from stable_baselines3 import PPO

# Define your model architecture
class CustomPolicy(nn.Module):
    def __init__(self):
        super(CustomPolicy, self).__init__()
        self.fc1 = nn.Linear(8, 64)  # Adjust input size based on your observation space
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 5)   # Adjust output size based on your action space

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Load the model
model = CustomPolicy()
model.load_state_dict(torch.load(r'D:\Temp\policy.pth'))
model.eval()  # Set the model to evaluation mode
