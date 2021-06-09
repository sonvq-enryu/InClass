import torch
import torch.nn as nn
from torch.nn.modules import padding

# Output shape is same with input shape, only channels increase.
class Conv2d(torch.nn.Module):
    def __init__(self, in_c, out_c, ksize, bn=False, leaky_relu=True, **kwargs):
        super().__init__()

        self.conv = nn.Conv2d(in_c, out_c, ksize, bias=False, **kwargs)
        self.norm = nn.BatchNorm2d(out_c) if bn else None
        self.leaky_relu = nn.LeakyReLU(0.2, inplace=True) if leaky_relu else None

    def forward(self, x):
        out = self.conv(x)
        if self.norm:
            out = self.norm(out)
        if self.leaky_relu:
            out = self.leaky_relu(out)
        return out

darknet_cfg = [
    (32, 3),
    'M', (64, 3),
    'M', (128, 3), (64, 1), (128, 3),
    'M', (256, 3), (128, 1), (256, 3),
    'M', (512, 3), (256, 1), (512, 3), (256, 1), (512, 3),
    'M', (1024, 3), (512, 1), (1024, 3), (512, 1), (1024, 3),
    (1024, 3), (1024, 3), (1024, 3) # 3 3x3 convolution layer and last layer is 1x1
]

class Darknet19(torch.nn.Module):
    def __init__(self, in_channels=3, S=13, B=5, C=20):
        super().__init__()

        self.S = S
        self.B = B
        self.C = C
        self.in_channels = in_channels
        self.darknet = self._make_layers(darknet_cfg)
    
    def forward(self, x):
        out = self.darknet(x)
        out = out.permute(0, 2, 3, 1)
        out = out.reshape(-1, self.S, self.S, self.B, (4 + 1 + self.C))
        return out

    def _make_layers(self, cfg):
        layers = []
        in_channels = self.in_channels

        for x in cfg:
            if isinstance(x, tuple):
                p = 0 if x[1] == 1 else 1 # kernel_size = 1 => padding = 0, else kernel_size = 3 then padding = 1
                layers += [Conv2d(in_channels, x[0], x[1], padding=p)]
                in_channels = x[0]
            else: # x is str
                layers += [nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))]
        
        layers += [Conv2d(in_channels, (4 + 1 + self.C) * self.B, 1, bn=False, padding=0)]
        return nn.Sequential(*layers)