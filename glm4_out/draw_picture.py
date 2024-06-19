import os
import json
from run_vega import vega_lite_svg
from tqdm import tqdm

vis_type = "heatmap"

# 设置文件夹路径
folder_path = fr'C:\Users\admin\PycharmProjects\create_data\gemini_out\{vis_type}\json'

# 获取文件夹中的所有文件
files = os.listdir(folder_path)

# 遍历所有文件
for file in tqdm(files):

    # 构建完整文件路径
    file_path = os.path.join(folder_path, file)

    # 打开并读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as f:
        f = f.read()
        print(type(f))
        file_name, file_extension = os.path.splitext(file)
        vega_lite = json.loads(f)
        url = f"https://raw.githubusercontent.com/gzu-zxc/visual_coda/main/json/{file}"
        vega_lite['data']['url'] = url
        # try:
        #     vega_lite['mark']['type'] = "heatmap"
        # except:
        #     vega_lite['mark'] = "heatmap"
        if 'tooltip' in vega_lite['mark']:
            del vega_lite['mark']['tooltip']

        vega_lite_svg(vega_lite,file_name,vis_type)
        print(file_name)