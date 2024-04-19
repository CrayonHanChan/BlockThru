import os, shutil
import xml.etree.ElementTree as ET
import pandas as pd
import re

# names:
  # 0: braille_guiding_block
  # 1: roadway
  # 2: crosswalk


surface_dict = {'braille_guide_blocks':0,
                  'roadway':1,
                  'crosswalk':2}

surface_labels = ['braille_guide_blocks', 'roadway']

# 폴더 경로 설정
base_directory = "D:/인도보행 영상/Surface_1"
labels_dir = "D:/인도보행 영상/Surface_processed/labels"
images_dir = "D:/인도보행 영상/Surface_processed/images"

# 통계내는 데이터프레임 초기화
columns = ['img_name']+list(surface_dict.keys())
df_img = pd.DataFrame(columns=columns)

# base_directory 내의 모든 폴더를 순회
for subfolder_name in os.listdir(base_directory):
  subfolder_path = os.path.join(base_directory,subfolder_name)
  print(subfolder_name)
  if os.path.isdir(subfolder_path):
      # 폴더 내의 XML 파일 찾기
      for file_name in os.listdir(subfolder_path):
          if file_name.endswith('.xml'):
              xml_path = os.path.join(subfolder_path, file_name)
              # XML 파일 파싱
              tree = ET.parse(xml_path)
              root = tree.getroot()

              # <image> 태그 내부 탐색
              for image in root.findall('image'):
                image_name = image.get('name')
                image_width = float(image.get('width'))
                image_height = float(image.get('height'))
                print(image_name)
                text_file_path = os.path.join(labels_dir, re.sub(r'\.(jpg|png)$', '.txt', image_name))
                count_label = 0
                str_to_write = ""
                for polygon in image.findall('polygon'):
                    label = polygon.get('label')
                    # print(label)
                    if label in surface_labels:
                        if count_label == 0:
                            new_row = {col: 0 for col in df_img.columns}
                            new_row['img_name'] = image_name
                            df_img.loc[len(df_img)] = new_row
                        count_label += 1
                        if label =='roadway':
                            sublabel = polygon.find('attribute').text
                            if sublabel=='crosswalk':
                                label = sublabel
                        df_img.loc[df_img.index[-1],label] +=1
                        points = polygon.get('points')
                        points_split = points.split(';')
                        x_list = []
                        y_list = []
                        for p in points_split:
                            c_list = p.split(',')
                            x_list.append("{:.6f}".format(float(c_list[0])/image_width))
                            y_list.append("{:.6f}".format(float(c_list[1])/image_height))
                        
                        combined = [val for pair in zip(x_list, y_list) for val in pair]
                        label_idx = surface_dict[label]
                        combined_str = f"{label_idx} {' '.join(combined)}\n"
                        str_to_write += combined_str
                if count_label > 0:
                  with open(text_file_path, 'w') as txt_file:
                      txt_file.write(str_to_write)

                if os.path.isfile(text_file_path):
                    img_path = os.path.join(subfolder_path,image_name)
                    shutil.copy2(img_path, images_dir)
    
# 스크립트 완료 메시지 출력
print("모든 폴더를 처리했습니다.")
save_df_img = 'D:/인도보행 영상/Surface_processed/df_surfimg.csv'
df_img.to_csv(save_df_img, index=False)