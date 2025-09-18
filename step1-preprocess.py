import json


def ts_to_json(ts_file_path, jsonl_file_path, name, question):
    """
    将TS文件转换为JSON格式并保存到文件。

    :param ts_file_path: TS文件的路径
    :param json_file_path: 输出JSON文件的路径
    :param name: 外部输入的名字
    :param question: 外部输入的问题
    """
    with open(ts_file_path, 'r') as file, open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
        idx = 251
        for line in file:
            if ':' in line:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    data_parts = parts[0].split(',')
                    label = parts[1]

                    try:
                        time_series = [float(x) for x in data_parts]
                        formatted_time_series = [f"{x:.4f}" for x in time_series]
                        entry = {
                            "id": idx,
                            "task": name,
                            "question": question,
                            "label": label,
                            "timeseries": formatted_time_series,
                            "timeseries2": ", ".join(formatted_time_series)
                        }
                        jsonl_file.write(json.dumps(entry, ensure_ascii=False) + '\n')
                        idx += 1
                    except ValueError:
                        print(f"Error processing line: {line}")
                        continue

                else:
                    print(f"Incorrect format in line: {line}")
            else:
                continue
        print(f"Finished processing line: {idx}")


ts_file_path = 'CTU/Computers_TEST.ts'
jsonl_file_path = 'CTU/CTU_test.jsonl'
name_input = 'CTU'
question_input = 'You are analyzing a time series signal derived from electricity usage patterns in UK households, recorded as part of the government-sponsored study "Powering the Nation". The signal represents energy consumption sampled every 2 minutes over a 24-hour period, resulting in a series length of 720. The plot shows a segment of the household’s daily electricity usage pattern. \nYour task is to classify the household’s device usage pattern into one of the following two classes: \n- label 1(Desktop): The energy consumption pattern suggests the use of a desktop computer. \n- label 2(Laptop): The energy consumption pattern suggests the use of a laptop computer. \nPlease choose the label(1/2) that best matches the full signal.'

ts_to_json(ts_file_path, jsonl_file_path, name_input, question_input)
