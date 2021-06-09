import torch.nn as nn
# Re-implement Yolov1 with Pytorch
# Refer from: https://www.youtube.com/watch?v=n9_XyCGr-MI


# Model architect from original paper:
cfg = [
    # Tuple: (kernel_size, out_channel, stride, padding), List represents list tuples and number repeats convolutional operation
    (7, 64, 2, 3),
    "M",
    (3, 192, 1, 1),
    "M",
    (1, 128, 1, 0),
    (3, 256, 1, 1),
    (1, 256, 1, 0),
    (3, 512, 1, 1),
    "M",
    [(1, 256, 1, 0), (3, 512, 1, 1), 4],
    (1, 512, 1, 0),
    (3, 1024, 1, 1),
    "M",
    [(1, 512, 1, 0), (3, 1024, 1, 1), 2],
    (3, 1024, 1, 1),
    (3, 1024, 2, 1),
    (3, 1024, 1, 1),
    (3, 1024, 1, 1),
]

class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super().__init__()

        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batch_norm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(0.1)
    def forward(self, x):
        out = self.conv(x)
        out = self.batch_norm(out)
        return self.leakyrelu(out)

class YOLOv1(nn.Module):
    def __init__(self, in_channels=3, **kwargs):
        super().__init__()

        self.cfg = cfg
        self.in_channels = in_channels
        self.darknet = self._make_layers(self.cfg)
        self.fcs = self._make_fcs(**kwargs)

    def forward(self, x):
        out = self.darknet(x)
        return self.fcs(out)

    def _make_layers(self, cfg):
        layers = []
        in_channels = self.in_channels

        for x in cfg:
            if isinstance(x, tuple):
                layers += [
                    ConvBlock(in_channels, x[1], kernel_size=x[0], stride=x[2], padding=x[3])
                ]
                in_channels = x[1]
    
            elif isinstance(x, list):
                conv1 = x[0]
                conv2 = x[1]
                repeats = x[2]

                for _ in range(repeats):
                    layers += [
                        ConvBlock(in_channels, conv1[1], kernel_size=conv1[0], stride=conv1[2]),
                        ConvBlock(conv1[1], conv2[1], kernel_size=conv2[0], stride=conv2[2], padding=conv2[3])
                    ]
                    in_channels = conv2[1]
            elif x == "M":
                layers += [nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))]
        
        return nn.Sequential(*layers)

    def _make_fcs(self, split_size, num_boxes, num_classes):
        S, B, C = split_size, num_boxes, num_classes

        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * S * S, 496),
            nn.Linear(496, S * S * (C + B * 5)),
        )
