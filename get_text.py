import json
import os
import traceback

def parse_result(json_data, output_file):
    # 判断 json_data 是文件路径还是 JSON 数据
    if isinstance(json_data, str) and os.path.isfile(json_data):
        with open(json_data, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif isinstance(json_data, (str, dict)):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
    else:
        raise ValueError("json_data 必须是有效的文件路径、JSON 字符串或字典。")

    results = []
    
    try:
        # 解析 orderResult 内部的 JSON 字符串
        order_result_data = data 

        for segment in json.loads(order_result_data["content"]['orderResult'])['lattice']:
            json_1best_data = json.loads(segment['json_1best'])
            # 调试
            # print(json_1best_data['st'])
            # {'sc': ' 0.000', 'pa': '0', 'rt': [{'ws': [{'cw': [{'w': '六', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 1, 'we': 12}, {'cw': [{'w': '七月份', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 13, 'we': 68}, {'cw': [{'w': '吧', 'wp': 's', 'wc': ' 0.000'}], 'wb': 69, 'we': 96}, {'cw': [{'w': '6月', 'og': '六月', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 97, 'we': 184}, {'cw': [{'w': '7月', 'og': '七月', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 185, 'we': 212}, {'cw': [{'w': '不', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 213, 'we': 224}, {'cw': [{'w': '记得', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 225, 'we': 240}, {'cw': [{'w': '了', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 241, 'we': 252}, {'cw': [{'w': '。', 'wp': 'p', 'wc': ' 0.000'}], 'wb': 252, 'we': 252}]}], 'bg': '440', 'rl': '1', 'ed': '3030'}

            start_time = None
            end_time = None
            speaker_id = 'Unknown'
            text = ''

            for key, value in json_1best_data['st'].items():  # 使用items()方法遍历键值对
                # print(key)
                # sc pa rt bg rl ed
                if key == 'bg':
                    start_time = int(value) / 1000
                elif key == 'ed':
                    end_time = int(value) / 1000
                elif key == 'rl':
                    speaker_id = value if value != 'None' else 'Unknown'  # 'rl'的值是说话人ID
                elif key == 'rt':
                    # print(value[0])
                    # {'ws': [{'cw': [{'w': '六', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 1, 'we': 12}, {'cw': [{'w': '七月份', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 13, 'we': 68}, {'cw': [{'w': '吧', 'wp': 's', 'wc': ' 0.000'}], 'wb': 69, 'we': 96}, {'cw': [{'w': '6月', 'og': '六月', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 97, 'we': 184}, {'cw': [{'w': '7月', 'og': '七月', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 185, 'we': 212}, {'cw': [{'w': '不', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 213, 'we': 224}, {'cw': [{'w': '记得', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 225, 'we': 240}, {'cw': [{'w': '了', 'wp': 'n', 'wc': ' 0.000'}], 'wb': 241, 'we': 252}, {'cw': [{'w': '。', 'wp': 'p', 'wc': ' 0.000'}], 'wb': 252, 'we': 252}]}
                    # for word in value[0]['ws']:
                    #     print(word)
                    text = "".join([word['cw'][0]['w'] for word in value[0]['ws']])
                
            # Format: [start_time - end_time] Speaker: text
            formatted_text = f"[{start_time:.2f} - {end_time:.2f}] Speaker {speaker_id}: {text}"
            results.append(formatted_text)

    except KeyError as e:
        print(f"JSON 数据结构不匹配，缺少键: {e}")
        traceback.print_exc()
        return
    except TypeError as e:
        print(f"数据类型错误: {e}")
        traceback.print_exc()
        return
    except json.JSONDecodeError as e:
        print(f"解析嵌套 JSON 时出错: {e}")
        traceback.print_exc()
        return

    # 创建输出文件目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))

    print(f"解析后的文本已写入 {output_file}")
    print(64*"=")
    return 1

# 使用示例
if __name__ == '__main__':
    parse_result("/home/youjiajun/result.json", "/home/youjiajun/result.txt")
