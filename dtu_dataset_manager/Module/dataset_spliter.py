import os

class DatasetSpliter(object):
    def __init__(self, dataset_root_folder_path: str) -> None:
        self.dataset_root_folder_path = dataset_root_folder_path
        return

    def reset(self) -> bool:
        return True

    def loadScene(self, scene_id: int) -> bool:
        return True

    def splitScene(self, scene_id: int) -> bool:
        return True
