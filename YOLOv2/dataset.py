import os
import torch
import pandas as pd
from PIL import Image

class VOCDataset(torch.utils.data.Dataset):
    def __init__(self, csv_file, img_dir, label_dir, S=13, B=5, C=20, transform=None):

        self.annotations = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.S = S
        self.B = B
        self.C = C
        self.transform = transform
    
    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        label_path = os.path.join(self.label_dir, self.annotations.iloc[index, 1])
        boxes = []

        with open(label_path, mode='r') as f:
            for line in f.readlines():
                box_class, x, y, w, h = [
                    float(x) for x in line.replace('\n', '').split(' ')
                ]
                boxes.append([int(box_class), x, y, w, h])

        img_path = os.path.join(self.img_dir, self.annotations.iloc[index, 0])
        image = Image.open(img_path)
        boxes = torch.tensor(boxes)

        if self.transform:
            image, boxes = self.transform(image, boxes)

        target = torch.zeros((self.S, self.S, self.B, 4 + 1 + self.C))
        for box in boxes:
            box_class, x, y, w, h = box.tolist()
            # calculate location on grid
            # row, col
            row, col = int(self.S  * y), int(self.S * x)
            # calculate x, y relative to 
            center_x, center_y = self.S * x - col, self.S * y - row

            w, h = (w * self.S, h * self.S)

            target[row, col, :, :4] = torch.tensor(self.B * [[center_x, center_y, w, h]])
            target[row, col, :, 4] = torch.tensor(self.B * [1.])
            target[row, col, :, 5+box_class] = torch.tensor(self.B * [1.])

        return image, target

dataset = VOCDataset('./pascal_voc/test.csv', img_dir='./pascal_voc/images', label_dir='./pascal_voc/labels')
