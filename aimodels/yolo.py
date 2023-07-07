import torch

class ModelLoader:
    def __init__(self, model_source='ultralytics/yolov5:v7.0', hub='github', weights=None, type='yolov5s'):
        self.model_source = model_source
        self.hub = hub
        self.weights = weights
        self.type = type

        if weights:
            self.model = self.load_finetuned()
        else:
            self.model = self.load_pretrained()

    def load_finetuned(self):
        model = torch.hub.load(self.model_source, 'custom', path=self.weights, verbose=False)
        return model

    def load_pretrained(self):
        model = torch.hub.load(self.model_source, self.type)
        return model