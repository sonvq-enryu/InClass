import torch
from utils import intersection_over_union

class CustomLoss(torch.nn.Module):
    """
    YOLOv1 Loss.
    """
    def __init__(self, S=7, B=2, C=20):
        super(CustomLoss, self).__init__()

        self.mse = torch.nn.MSELoss(reduction="sum")

        """
        S is number of of grid cell, default value is 7.
        B is number bounding box per grid cell, default is 2.
        C is number of class of object. default value is 20 (number class of PASCAL VOC 2007/2012)
        """
        self.S = S
        self.B = B
        self.C = C

        self.lambda_noobj = 0.5
        self.lambda_coord = 5

    def forward(self, predicts, targets):
        """
        predicts from backbone model is (batch_size, S * S (B * 5 + C))
        """
        predicts = predicts.reshape(-1, self.S, self.S, self.B * 5 + self.C)

        iou_box1 = intersection_over_union(predicts[..., 21:25], targets[..., 21:25])
        iou_box2 = intersection_over_union(predicts[..., 26:30], targets[..., 21:25])

        ious = torch.cat([iou_box1.unsqueeze(0), iou_box2.unsqueeze(0)], dim=0)
        bestbox = torch.argmax(ious, dim=0)
        exists_box = targets[..., 20:21] # using not redundant shape, this is confidence score of target
        
        """
        Localization loss
        """
        box_predicts = exists_box * (
            bestbox * predicts[..., 26:30] + (1 - bestbox) * predicts[..., 21:25]
        )

        box_targets = exists_box * targets[..., 21:25]

        box_predicts = torch.sign(box_predicts[..., 2:4]) * torch.sqrt(
            torch.abs(box_predicts[..., 2:4])
        )
        box_targets = torch.sqrt(box_targets[..., 2:4])

        box_loss = self.mse(
            torch.flatten(box_targets, end_dim=-2),
            torch.flatten(box_predicts, end_dim=-2)
        )
        """
        Confidence loss
        """
        obj_conf_predicts = bestbox * predicts[..., 25:26] + (1 - bestbox) * predicts[..., 20:21]

        obj_conf_loss = self.mse(
            torch.flatten(targets[..., 20:21], start_dim=1),
            torch.flatten(exists_box * obj_conf_predicts, start_dim=1)
        )

        noobj_conf_predicts = bestbox * predicts[..., 25:26] + (1 - bestbox) * predicts[..., 20:21]

        noobj_conf_loss = self.mse(
            torch.flatten((1 - exists_box) * targets[..., 20:21]),
            torch.flatten((1- exists_box) * noobj_conf_predicts)
        )

        """
        Classification loss
        """
        clf_loss = self.mse(
            torch.flatten(exists_box * targets[..., :20], end_dim=-2),
            torch.flatten(exists_box * predicts[..., :20], end_dim=-2)
        )

        loss = (
            self.lambda_coord * box_loss + 
            obj_conf_loss + 
            self.lambda_noobj * noobj_conf_loss +
            clf_loss
        )

        return loss

def test():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    x = torch.randn((32, 7, 7, 30))
    y = torch.abs(torch.randn((32, 7, 7, 30)))

    crit = CustomLoss()
    loss = crit(x, y)
    print(loss.item())

test()