# complete code
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# load the dataset, split into input (X) and output (y) variables
dataset = np.loadtxt('pima-indians-diabetes.csv', delimiter=',')
X = dataset[:, 0:8]
y = dataset[:, 8]

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)

# define the model
model = nn.Sequential(
    nn.Linear(8, 12),
    nn.ReLU(),
    nn.Linear(12, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid()
)
print(model)

# train the model
loss_fn = nn.BCELoss()  # binary cross entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

n_epochs = 100
batch_size = 10

for epoch in range(n_epochs):
    for i in range(0, len(X), batch_size):
        Xbatch = X[i:i + batch_size]
        y_pred = model(Xbatch)
        ybatch = y[i:i + batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Finished epoch {epoch}, latest loss {loss}')

# compute accuracy (no_grad is optional)
with torch.no_grad():
    y_pred = model(X)
accuracy = (y_pred.round() == y).float().mean()
print(f"Accuracy {accuracy}")



# use the model
print("predictions")
print(model(X))     # see if it can predict correctly using the original input






# the follow along:

# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim
#
# # load the dataset, split into input (X) and output (y) variables
# dataset = np.loadtxt('pima-indians-diabetes.csv', delimiter=',')
# X = dataset[:,0:8]
# y = dataset[:,8]
#
# X = torch.tensor(X, dtype=torch.float32)
# y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)
#
#
# # defining model 8 > 12 > 12 > 8 > 1 (output therefore classifier)
# # model = nn.Sequential(
# #     nn.Linear(8, 12),
# #     nn.ReLU(),        # activation treshold function combinding the layers ( "rectified linear unit activation function" here)
# #     nn.Linear(12, 8),
# #     nn.ReLU(),
# #     nn.Linear(8, 1),
# #     nn.Sigmoid())
#
# # aparently better, classinherit from nn (pycharm nerual net.) (and can print steps in between)
# class PimaClassifier(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.hidden1 = nn.Linear(8, 12)
#         self.act1 = nn.ReLU()
#         self.hidden2 = nn.Linear(12, 8)
#         self.act2 = nn.ReLU()
#         self.output = nn.Linear(8, 1)
#         self.act_output = nn.Sigmoid()
#
#     def forward(self, x):
#         x = self.act1(self.hidden1(x))
#         x = self.act2(self.hidden2(x))
#         x = self.act_output(self.output(x))
#         return x
#
#
# model = PimaClassifier()
#
#
#
# loss_fn = nn.BCELoss()  # binary cross entropy
# optimizer = optim.Adam(model.parameters(), lr=0.001)
#
#
#
# n_epochs = 100
# batch_size = 10
#
# for epoch in range(n_epochs):
#     for i in range(0, len(X), batch_size):
#         Xbatch = X[i:i + batch_size]
#         y_pred = model(Xbatch)
#         ybatch = y[i:i + batch_size]
#         loss = loss_fn(y_pred, ybatch)
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#     print(f'Finished epoch {epoch}, latest loss {loss}')
#
#
#
# # evaluate the model
# # compute accuracy (no_grad is optional)
# with torch.no_grad():
#     y_pred = model(X)
#
# accuracy = (y_pred.round() == y).float().mean()
# print(f"Accuracy {accuracy}")
#
#
