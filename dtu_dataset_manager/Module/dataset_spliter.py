import os
from tqdm import tqdm
from shutil import copyfile

from dtu_dataset_manager.Method.path import removeFile

class DatasetSpliter(object):
    def __init__(self, dataset_root_folder_path: str) -> None:
        self.dataset_root_folder_path = dataset_root_folder_path

        if self.dataset_root_folder_path[-1] != "/":
            self.dataset_root_folder_path += "/"

        self.rectified_folder_path = self.dataset_root_folder_path + "Rectified/"

        self.valid_scene_id_list = []

        self.updateValidSceneIdList()
        return

    def reset(self) -> bool:
        return True

    def updateValidSceneIdList(self, force: bool = False) -> bool:
        if not force:
            if len(self.valid_scene_id_list) > 0:
                return True

        if not self.isValid():
            print('[ERROR][DatasetSpliter::updateValidSceneIdList]')
            print('\t isValid check failed!')
            return False

        scene_folder_name_list = os.listdir(self.rectified_folder_path)

        self.valid_scene_id_list = []

        for scene_folder_name in scene_folder_name_list:
            if scene_folder_name[:4] != 'scan':
                continue

            scene_id = int(scene_folder_name[4:])

            self.valid_scene_id_list.append(scene_id)

        self.valid_scene_id_list.sort()

        return True

    def isValid(self, output_info: bool = True) -> bool:
        if not os.path.exists(self.dataset_root_folder_path):
            if output_info:
                print('[ERROR][DatasetSpliter::isValid]')
                print('\t dataset not found!')
                print('\t dataset_root_folder_path :', self.dataset_root_folder_path)
            return False

        if not os.path.exists(self.rectified_folder_path):
            if output_info:
                print('[ERROR][DatasetSpliter::isValid]')
                print('\t rectified folder not found!')
                print('\t rectified_folder_path :', self.rectified_folder_path)
            return False

        return True

    def getValidSceneIdList(self) -> list:
        self.updateValidSceneIdList()
        return self.valid_scene_id_list

    def getSceneSplitTagList(self, scene_id: int) -> list:
        if not self.isValid():
            print('[ERROR][DatasetSpliter::getSceneSplitTagList]')
            print('\t isValid check failed!')
            return []

        if scene_id not in self.valid_scene_id_list:
            print('[ERROR][DatasetSpliter::getSceneSplitTagList]')
            print('\t scene_id not valid!')
            return []

        scene_folder_path = self.rectified_folder_path + "scan" + str(scene_id) + "/"

        scene_filename_list = os.listdir(scene_folder_path)

        scene_split_tag_list = []

        for scene_filename in scene_filename_list:
            if scene_filename[:5] != 'rect_':
                continue

            if scene_filename[-4:] != '.png':
                continue

            scene_info_list = scene_filename[5:-4].split('_')
            scene_split_tag = scene_info_list[1]
            if len(scene_info_list) > 2:
                for scene_info in scene_info_list[2:]:
                    scene_split_tag += '_' + scene_info

            if scene_split_tag not in scene_split_tag_list:
                scene_split_tag_list.append(scene_split_tag)

        return scene_split_tag_list

    def splitSceneWithTag(self, scene_id: int, split_tag: str, save_image_folder_path: str, overwrite: bool = False) -> bool:
        if not self.isValid():
            print('[ERROR][DatasetSpliter::splitSceneWithTag]')
            print('\t isValid check failed!')
            return False

        if scene_id not in self.valid_scene_id_list:
            print('[ERROR][DatasetSpliter::splitSceneWithTag]')
            print('\t scene_id not valid!')
            return False

        os.makedirs(save_image_folder_path, exist_ok=True)

        scene_folder_path = self.rectified_folder_path + "scan" + str(scene_id) + "/"

        scene_filename_list = os.listdir(scene_folder_path)

        full_tag = split_tag + '.png'

        print('[INFO][DatasetSpliter::splitSceneWithTag]')
        print('\t start split scene', scene_id, 'with tag', split_tag, '...')
        for scene_filename in tqdm(scene_filename_list):
            if full_tag not in scene_filename:
                continue

            save_image_file_path = save_image_folder_path + scene_filename

            if os.path.exists(save_image_file_path):
                if not overwrite:
                    continue

            removeFile(save_image_file_path)

            copyfile(scene_folder_path + scene_filename, save_image_file_path)

        return True

    def splitScene(self, scene_id: int, save_image_root_folder_path: str, overwrite: bool = False) -> bool:
        os.makedirs(save_image_root_folder_path, exist_ok=True)

        scene_split_tag_list = self.getSceneSplitTagList(scene_id)
        if len(scene_split_tag_list) == 0:
            print('[ERROR][DatasetSpliter::splitScene]')
            print('\t getSceneSplitTagList failed!')
            return False

        for scene_split_tag in scene_split_tag_list:
            save_image_folder_path = save_image_root_folder_path + str(scene_id) + '/' + scene_split_tag + '/input/'

            if not self.splitSceneWithTag(scene_id, scene_split_tag, save_image_folder_path, overwrite):
                print('[WARN][DatasetSpliter::splitScene]')
                print('\t splitSceneWithTag failed!')
                print('\t scene_id :', scene_id)
                print('\t scene_split_tag :', scene_split_tag)
                print('\t save_image_folder_path :', save_image_folder_path)
                continue

        return True

    def autoSplitScenes(self, save_image_root_folder_path: str, overwrite: bool = False) -> bool:
        for scene_id in self.valid_scene_id_list:
            if not self.splitScene(scene_id, save_image_root_folder_path, overwrite):
                print('[WARN][DatasetSpliter::autoSplitScenes]')
                print('\t splitScene failed!')
                print('\t scene_id :', scene_id)
        return True
