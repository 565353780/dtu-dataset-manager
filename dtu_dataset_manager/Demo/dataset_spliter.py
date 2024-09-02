from dtu_dataset_manager.Module.dataset_spliter import DatasetSpliter

def demo():
    dataset_root_folder_path = "/home/chli/chLi/Dataset/DTU/"
    scene_id = 24

    dataset_spliter = DatasetSpliter(dataset_root_folder_path)
    dataset_spliter.splitScene(scene_id)
    return True
