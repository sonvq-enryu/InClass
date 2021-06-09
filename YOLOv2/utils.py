import torch
import torch
from torch import Tensor

# Original implementation from https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
def _upcast(t: Tensor) -> Tensor:
    # Protects from numerical overflows in multiplications by upcasting to the equivalent higher type
    if t.is_floating_point():
        return t if t.dtype in (torch.float32, torch.float64) else t.float()
    else:
        return t if t.dtype in (torch.int32, torch.int64) else t.int()

def box_area(boxes: Tensor) -> Tensor:
    """
    Computes the area of a set of bounding boxes, which are specified by their
    (x1, y1, x2, y2) coordinates.
    Args:
        boxes (Tensor[N, 4]): boxes for which the area will be computed. They
            are expected to be in (x1, y1, x2, y2) format with
            ``0 <= x1 < x2`` and ``0 <= y1 < y2``.
    Returns:
        Tensor[N]: the area for each box
    """
    boxes = _upcast(boxes)
    return (boxes[..., 2:3] - boxes[..., 0:1]) * (boxes[..., 3:4] - boxes[..., 1:2])


def box_iou(box1, box2):
    """
    Calculate Intersection over Union (IoU)
    box format in (x1, x2, y1, y2) with 0 <= x1 < x2 and 0 <= y1 < y2
    Params:
        box1: tensor with shape (n, 4)
        box2: tensor with shape (1, 4)
    Return:
        tensor with shape (batch_size, priors_size, 1)
        represent IoU score between box1 and box2 pairwise
    """
    lt = torch.maximum(box1[..., :2], box2[..., :2])
    rb = torch.minimum(box1[..., 2:4], box2[..., 2:4])

    wh = _upcast(rb - lt).clamp(min=0)
    inter = wh[..., 0:1] * wh[..., 1:2]

    box1_area = box_area(box1)
    box2_area = box_area(box2)

    return inter / (box1_area + box2_area - inter)

a = torch.rand((8, 13, 13, 5, 4))
b = torch.rand((8, 13, 13, 1, 4))
ious = box_iou(a, b)
max_iou = torch.max(ious, dim=3, keepdim=True)[0]
print(max_iou.shape)
best_box_index = torch.unsqueeze(torch.eq(ious, max_iou).float(), dim=-1)
print(best_box_index)