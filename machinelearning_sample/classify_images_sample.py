import os
import torch
from torchvision import models, transforms
from PIL import Image
import shutil

INPUT_DIR = "./to_classify"
OUTPUT_DIR = "./output"
MODEL_PATH = "./models/sample1_vs_sample2.pth"

CLASSES = ["sample1", "sample2"]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# モデル読み込み
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

for class_name in CLASSES:
    os.makedirs(os.path.join(OUTPUT_DIR, class_name), exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        continue

    image_path = os.path.join(INPUT_DIR, filename)
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        pred_class = CLASSES[torch.argmax(output, 1).item()]

    dest_path = os.path.join(OUTPUT_DIR, pred_class, filename)
    shutil.copy2(image_path, dest_path)
    print(f"{filename} → {pred_class}")

print("✅ すべての画像を分類しました。")
