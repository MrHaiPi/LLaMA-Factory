#!/bin/bash
set -e  # 任何命令失败（非零退出码）立即退出脚本

# train
yaml_path=/home/xiarui/nas/projects/LLaMA-Factory/examples/train_lora/photo_intern_vl3_lora_sft1.yaml
data_backup_dir=/home/xiarui/nas/projects/AIPhoto/Dataset/final_train

llamafactory-cli train $yaml_path

python sh/backup_train_data.py \
--yaml_path $yaml_path \
--data_backup_dir $data_backup_dir



# # train
# yaml_path=/home/xiarui/projects/LLaMA-Factory/examples/train_full/photo_smolvlm_full_sft.yaml
# data_backup_dir=/home/xiarui/projects/AIPhoto/Dataset/final_train

# llamafactory-cli train $yaml_path

# python /home/xiarui/projects/LLaMA-Factory/sh/backup_train_data.py \
# --yaml_path $yaml_path \
# --data_backup_dir $data_backup_dir

