import os, shutil
from sklearn.model_selection import train_test_split
import re

# train, test, val로 나눌 전체 이미지 리스트
# 1. 그리고 8:1:1로 나누기
# 2. 이미지 리스트를 train, test, valid 나눠서 저장

# 폴더 경로 설정
images_dir = "D:/인도보행 영상/Surface_processed/images_resized"
labels_dir = "D:/인도보행 영상/Surface_processed/labels"

train_img_dir = "D:/인도보행 영상/Surface_processed/train/images"
train_labels_dir = "D:/인도보행 영상/Surface_processed/train/labels"

test_img_dir = "D:/인도보행 영상/Surface_processed/test/images"
test_labels_dir = "D:/인도보행 영상/Surface_processed/test/labels"

val_img_dir = "D:/인도보행 영상/Surface_processed/valid/images"
val_labels_dir = "D:/인도보행 영상/Surface_processed/valid/labels"

# csv 불러와서 list로 변환
file_path = "D:/인도보행 영상/Surface_processed/image_list.txt"
# data = list()
with open(file_path, 'r', encoding='utf-8') as file:
    data = [line.strip() for line in file]

# train, test, val로 나누는 과정
train_img_list, test_img_list = train_test_split(data, test_size=0.2, random_state=777)
print(len(train_img_list), len(test_img_list))
      
test_img_list, val_img_list = train_test_split(test_img_list, test_size=0.5, random_state=777)
print(len(test_img_list), len(val_img_list))

# 각 train,test,val에 속하는 리스트들을 순회하며 각 해당폴더로 이미지와 label txt 파일 복사 실행
for img in train_img_list:
    print(img)
    origin_img_path = os.path.join(images_dir,img)
    origin_text_path = os.path.join(labels_dir, re.sub(r'\.(jpg|png)$', '.txt', img))
    shutil.copy2(origin_img_path, train_img_dir)
    shutil.copy2(origin_text_path, train_labels_dir)

for img in test_img_list:
    print(img)
    origin_img_path = os.path.join(images_dir,img)
    origin_text_path = os.path.join(labels_dir, re.sub(r'\.(jpg|png)$', '.txt', img))
    shutil.copy2(origin_img_path, test_img_dir)
    shutil.copy2(origin_text_path, test_labels_dir)

for img in val_img_list:
    print(img)
    origin_img_path = os.path.join(images_dir,img)
    origin_text_path = os.path.join(labels_dir, re.sub(r'\.(jpg|png)$', '.txt', img))
    shutil.copy2(origin_img_path, val_img_dir)
    shutil.copy2(origin_text_path, val_labels_dir)