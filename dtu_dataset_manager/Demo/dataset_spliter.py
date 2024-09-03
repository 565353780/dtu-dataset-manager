from dtu_dataset_manager.Module.dataset_spliter import DatasetSpliter

def demo():
    dataset_root_folder_path = "/home/chli/chLi/Dataset/DTU/"
    save_image_root_folder_path = "/home/chli/chLi/Dataset/DTU/split_images/"
    overwrite = False

    dataset_spliter = DatasetSpliter(dataset_root_folder_path)

    valid_scene_id_list = dataset_spliter.getValidSceneIdList()
    print('valid_scene_id_list:')
    print(valid_scene_id_list)

    dataset_spliter.autoSplitScenes(save_image_root_folder_path, overwrite)

    return True
