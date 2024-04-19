import os
import glob

# 폴더 경로 설정
folder_path = 'D:/kdt_231026/data/valid/labels'

# 폴더 내의 모든 .txt 파일 찾기
txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

# 각 파일에 대해 반복
for file_path in txt_files:
    print(file_path)
    with open(file_path, 'r') as file:
    # 파일 내용 읽기
        lines = file.readlines()
        print(lines)

    # 수정할 내용을 변경하는 과정 (객체 22번 삭제하고 22번 이후 객체 번호 하나씩 빼기)
    modified_lines = []
    for line in lines:
        temp = line.split(" ")
        print(temp)
        if int(temp[0]) == 22:
            continue
        elif int(temp[0]) > 22:
            temp[0] = str(int(temp[0]) -1)
            line_adjusted = " ".join(temp)
            modified_lines.append(line_adjusted)
        else:
            modified_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(modified_lines)