import os


def rename_images(folder_path):
    # 获取文件夹中的所有文件名
    files = os.listdir(folder_path)

    # 筛选出图像文件（根据扩展名）
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))]

    # 对文件进行排序（按名称）
    image_files.sort()

    # 遍历每个文件并重命名
    for i, file_name in enumerate(image_files):
        # 构建新文件名（递增数列，6位数字，不足前面补0）
        new_name = f"{i:06d}" + os.path.splitext(file_name)[1]

        # 构建完整路径
        old_file = os.path.join(folder_path, file_name)
        new_file = os.path.join(folder_path, new_name)

        # 重命名文件
        os.rename(old_file, new_file)
        print(f"Renamed: {old_file} -> {new_file}")


# 使用示例：将 'path/to/your/folder' 替换为你的文件夹路径
folder_path = 'R'
rename_images(folder_path)
