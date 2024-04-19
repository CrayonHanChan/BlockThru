import os, shutil
import xml.etree.ElementTree as ET
import pandas as pd
import re

# names:
  # 0: person
  # 1: bicycle
  # 2: car
  # 3: motorcycle
  # 4: bus
  # 5: tree_trunk #argoverse에는 truck
  # 6: traffic_light
  # 7: stop # agroverse에는 stop_sign
  # 8: carrier
  # 9: cat
  # 10: dog
  # 11: movable_signage
  # 12: scooter
  # 13: stroller
  # 14: truck
  # 15: wheelchair
  # 16: barricade
  # 17: bench
  # 18: bollard
  # 19: chair
  # 20: fire_hydrant
  # 21: kiosk
  # 22: parking_meter
  # 23: pole
  # 24: potted_plant
  # 25: power_controller
  # 26: table
  # 27: traffic_light_controller
  # 28: traffic_sign

obstacles_dict = {'person':0,
                  'bicycle':1,
                  'car':2,
                  'motorcycle':3,
                  'bus':4,
                  'tree_trunk':5,
                  'traffic_light':6,
                  'stop':7,
                  'carrier':8,
                  'cat':9,
                  'dog':10,
                  'movable_signage':11,
                  'scooter':12,
                  'stroller':13,
                  'truck':14,
                  'wheelchair':15,
                  'barricade':16,
                  'bench':17,
                  'bollard':18,
                  'chair':19,
                  'fire_hydrant':20,
                  'kiosk':21,
                  'parking_meter':22,
                  'pole':23,
                  'potted_plant':24,
                  'power_controller':25,
                  'table':26,
                  'traffic_light_controller':27,
                  'traffic_sign':28}

# 폴더 경로 설정
base_directory = "D:/인도보행 영상/바운딩박스"
labels_dir = "D:/인도보행 영상/labels"
no_image_labels_dir = "D:/인도보행 영상/no_image_labels"
images_dir = "D:/인도보행 영상/images"

# 통계내는 데이터프레임 초기화
columns = ['img_name']+list(obstacles_dict.keys())
df_img = pd.DataFrame(columns=columns)
df_noimg = pd.DataFrame(columns=columns)

# base_directory 내의 모든 폴더를 순회
for folder_name in os.listdir(base_directory):
  folder_path = os.path.join(base_directory, folder_name)
  print(folder_name)
  if os.path.isdir(folder_path):
    for subfolder_name in os.listdir(folder_path):
      subfolder_path = os.path.join(folder_path,subfolder_name)
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
                      # 확인하고 있는 폴더에 image 파일의 유무를 확인 후 image 있을 시, 파일 복사 실행
                      checkimg_path = os.path.join(subfolder_path,image_name)
                      img_available = False
                      if os.path.isfile(checkimg_path):
                        img_available = True
                        shutil.copy2(checkimg_path, images_dir)
                      # image 파일이 없는 경우, labels txt를 모아두는 폴더 다르게 지정하고 각 데이터 프레임에 데이터추가
                      ## 데이터프레임의 새로운 행에 모든 값을 0으로 설정하고 추가하기
                      new_row = {col: 0 for col in df_img.columns}
                      new_row['img_name'] = image_name
                      if img_available == True:
                        text_file_path = os.path.join(labels_dir, re.sub(r'\.(jpg|png)$', '.txt', image_name))
                        # text_file_path = os.path.join(labels_dir, image_name.replace('.jpg', '.txt'))
                        df_img.loc[len(df_img)] = new_row
                      else:
                        text_file_path = os.path.join(no_image_labels_dir, re.sub(r'\.(jpg|png)$', '.txt', image_name))
                        df_noimg.loc[len(df_noimg)] = new_row

                      with open(text_file_path, 'w') as txt_file:
                          # <box> 태그 내부의 label과 points 추출
                          for box in image.findall('box'):
                              label = box.get('label')
                              xtl = float(box.get('xtl'))
                              ytl = float(box.get('ytl'))
                              xbr = float(box.get('xbr'))
                              ybr = float(box.get('ybr'))
                              w = xbr - xtl
                              h = ybr - ytl # 수정
                              norx = (xtl+w/2) / image_width
                              nory = (ytl+h/2) / image_height
                              norw = w/image_width
                              norh = h/image_height
                              # 혹 1보다 클 경우
                              norx = 1 if norx>1 else norx
                              nory = 1 if nory>1 else nory
                              norw = 1 if norw>1 else norw
                              norh = 1 if norh>1 else norh
                              # 혹 0보다 작을 경우
                              norx = 0.000001 if norx<0 else norx
                              nory = 0.000001 if nory<0 else nory
                              norw = 0.000001 if norw<0 else norw
                              norh = 0.000001 if norh<0 else norh
                              # 소수점 6자리까지
                              norx= "{:.6f}".format(float(norx))
                              nory= "{:.6f}".format(float(nory))
                              norw= "{:.6f}".format(float(norw))
                              norh= "{:.6f}".format(float(norh))
                              # label index
                              label_idx = obstacles_dict[label]
                              # need to write a txt file in the format of label_idx norx nory norw norh
                              txt_file.write(f"{label_idx} {norx} {nory} {norw} {norh}\n")
                              # dataframe에도 각 이미지의 label추가하기
                              if img_available == True:
                                df_img.loc[df_img.index[-1],label] +=1
                              else:
                                df_noimg.loc[df_noimg.index[-1],label] +=1

# 스크립트 완료 메시지 출력
print("모든 폴더를 처리했습니다.")
save_df_img = 'D:/인도보행 영상/df_img.csv'
save_df_noimg = 'D:/인도보행 영상/df_noimg.csv'
df_img.to_csv(save_df_img, index=False)
df_noimg.to_csv(save_df_noimg, index=False)