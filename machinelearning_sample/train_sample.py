import os
import torch
from torch import nn, optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader

data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
])

data_dir = "./dataset_sample/train"
dataset = datasets.ImageFolder(data_dir, transform=data_transforms)

dataset.samples = [s for s in dataset.samples if os.path.exists(s[0])]

dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# モデル構築（ResNet18）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2) 
model = model.to(device)

#ファインチューニング
model_path = "models/sample1_vs_sample2.pth"
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    print("既存モデルを読み込みました")
else:
    print("新しいモデルを作成します")

# 損失関数と最適化
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.00005) 

# 学習
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct = 0

    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        correct += torch.sum(preds == labels.data)

    accuracy = correct.double() / len(dataset)
    print(f"Epoch {epoch+1}, Loss: {running_loss:.4f}, Accuracy: {accuracy:.4f}")

os.makedirs("models", exist_ok=True)
torch.save(model.state_dict(), model_path)
print("モデルを保存しました")
