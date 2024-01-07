import torch
from PIL import Image

from misc import colorize


class DepthEstimationModel:
    def __init__(self) -> None:
        self.device = self._get_device()
        self.model = self._initialize_model(
            model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"
        ).to(self.device)

    def _get_device(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _initialize_model(self, model_repo="isl-org/ZoeDepth", model_name="ZoeD_N"):
        torch.hub.help("intel-isl/MiDaS", "DPT_BEiT_L_384", force_reload=True)
        model = torch.hub.load(
            model_repo, model_name, pretrained=True, skip_validation=True
        )
        model.eval()
        print("Model initialized successfully!")
        return model

    def save_colorized_depth(self, depth_numpy, output_path):
        colored = colorize(depth_numpy)
        Image.fromarray(colored).save(output_path)
        print("Colorized image saved successfully!")

    def calculate_depthmap(self, image_path, output_path):
        image = Image.open(image_path).convert("RGB")
        print("Image read successfully!")
        depth_numpy = self.model.infer_pil(image)
        self.save_colorized_depth(depth_numpy, output_path)
        return f"Image saved successfully at {output_path}"
