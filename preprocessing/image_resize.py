from PIL import Image
import os

# 원본 이미지 파일 경로
root_path = "D:/인도보행 영상/Surface_processed/images"
# root_path = "D:/인도보행 영상/train/images_test"

# 저장할 이미지 파일 경로
output_image_path = "D:/인도보행 영상/Surface_processed/images_resized"

for image_name in os.listdir(root_path):
    print(image_name)
    # 이미지 열기
    original_image_path = os.path.join(root_path,image_name)
    image = Image.open(original_image_path)

    # 이미지 크기 조절 (해상도 변경)
    resized_image = image.resize((1024, 576))
    if image_name.endswith('.png'):
        new_image_path = os.path.join(output_image_path, image_name.replace('.png', '.jpg'))
        rgb_image = resized_image.convert('RGB')
        rgb_image.save(new_image_path, 'JPEG') # JPEG 포맷으로 저장하면서 용량 낮추기
    else:
        new_image_path = os.path.join(output_image_path,image_name)
        resized_image.save(new_image_path)