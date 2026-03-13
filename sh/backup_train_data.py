import yaml
import os
import shutil
import json
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="从 YAML 配置中读取 dataset 并拷贝 jsonl 文件到备份目录")
    parser.add_argument("--yaml_path", required=True, help="YAML 配置文件路径")
    parser.add_argument("--data_backup_dir", required=True, help="数据备份的根目录路径")
        
    args = parser.parse_args()

    # 配置路径
    yaml_path = args.yaml_path
    # yaml_path = "/home/xiarui/projects/LLaMA-Factory/examples/train_lora/photo_qwen3vl_lora_sft.yaml"
    data_backup_dir = args.data_backup_dir
    # data_backup_dir = "/home/xiarui/projects/AIPhoto/Dataset/final_train"

    # 读取 YAML 文件
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 提取字段
    dataset_dir = config.get('dataset_dir')
    dataset_str = config.get('dataset')
    output_dir = config.get('output_dir')

    # 拷贝训练配置
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy2(yaml_path, os.path.join(output_dir, os.path.basename(yaml_path)))

    if not all([dataset_dir, dataset_str, output_dir]):
        raise ValueError("YAML 文件中缺少 dataset_dir、dataset 或 output_dir 字段")

    # 解析 dataset 字符串（格式为 "str,str,str"）
    dataset_files = [f.strip() + ".json" for f in dataset_str.split(',')]
    dataset_files.append("dataset_info.json") # 单独加一个文件

    # 构建目标目录
    target_dir = os.path.join(data_backup_dir, output_dir)
    os.makedirs(target_dir, exist_ok=True)

    # 拷贝每个 jsonl 文件
    for file_name in dataset_files:

        src_path = os.path.join(dataset_dir, file_name)
        dst_path = os.path.join(target_dir, file_name)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"已拷贝: {src_path} -> {dst_path}")
        else:
            print(f"错误: 源文件不存在 {src_path}")
        
        # info文件没有图片要拷贝
        if file_name == "dataset_info.json":
            continue
        
        # 拷贝图片
        # 读取有哪些文件夹
        image_dir_dic = {}
        with open(src_path, "r") as f:
            js = json.load(f)
            for item in js:
                for image_path in item["images"]:
                    image_dir = image_path.split("/")[0]
                    image_dir_dic[image_dir] = 1
        # 把文件夹下的所有文件或文件夹都拷贝到target_dir
        for dir_name in image_dir_dic:
            src_dir_path = os.path.join(dataset_dir, dir_name)
            dst_dir_path = os.path.join(target_dir, dir_name)
            os.makedirs(dst_dir_path, exist_ok=True)
            shutil.copytree(src_dir_path, dst_dir_path, dirs_exist_ok=True)
        

    print("文件拷贝完成。")


if __name__ == "__main__":
    main()