import torch

class Yolov2Loss(torch.nn.Module):
    def __init__(self, priors, S=13, B=5, C=20):
        super.__init__()

        self.mse = torch.nn.MSELoss(reduction="sum")
        self.S = S
        self.B = B
        self.C = C
        self.priors = priors

        self.lambda_coord = 5
        self.lambda_noobj = 0.5

    def forward(self, predicts, targets):
        """
        Calculate YOLO loss
        Params:
            predicts: tensor with shape (batch_size, S, S, B, 5 + C)
            targets : tensor with shape (batch_size, S, S, B, 5 + C)
        """
        predicts = self.post_process_preds(predicts)
        
         

    def post_process_preds(self, preds):
        preds[..., :2] = torch.sigmoid(preds[..., :2] + 1e-6)
        priors_wh = torch.reshape(self.priors, (1, 1, 1, self.B, 2))
        preds[..., 2:4] = priors_wh * torch.exp(preds[..., 2:4])
        preds[..., 4:5] = torch.sigmoid(preds[..., 4:5] + 1e-6)
        preds[..., 5:] = torch.softmax(preds[..., 5:], dim=-1)
        return preds
