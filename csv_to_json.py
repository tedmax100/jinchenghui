#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import json
import re

def extract_building_floor(description):
    """从说明中提取门牌号和楼层"""
    # 匹配格式如: 500-2F., 502-10F., 500-14F.1, B2-67, 510. 等
    match = re.match(r'^(\d+)-(\d+)F?', description)
    if match:
        building = match.group(1)
        floor = int(match.group(2))
        return building, floor

    # 匹配 B2-67, 510. 这种车位格式
    match = re.match(r'^B\d+-\d+,\s*(\d+)', description)
    if match:
        building = match.group(1)
        return building, 0

    # 其他格式返回空
    return "", 0

def csv_to_json(csv_path, output_path):
    results = []

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader):
            card_no = row['卡號'].strip()
            description = row['使用者說明'].strip()
            password = 0  # 固定为0
            card_type = row['卡片類型'].strip()
            use_floor = row['使用樓層'].strip()
            access_group = row['通行群組'].strip()
            parking_group = row['車位群組'].strip()
            parking_status = row['停車狀態'].strip()

            # 提取门牌号和楼层
            building, floor = extract_building_floor(description)

            # 生成 primaryKey
            if building and floor > 0:
                primary_key = f"{building}-{floor:02d}"
            elif building:
                primary_key = building
            else:
                primary_key = ""

            record = {
                "index": idx,
                "cardNo": card_no,
                "description": description,
                "password": password,
                "cardType": card_type,
                "useFloor": use_floor,
                "accessGroup": access_group,
                "parkingGroup": parking_group,
                "parkingStatus": parking_status,
                "building": building,
                "floor": floor,
                "primaryKey": primary_key,
                "parkingSpots": []
            }
            results.append(record)

    # 输出 JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"转换完成！共 {len(results)} 笔资料")
    print(f"输出文件: {output_path}")
    return results

if __name__ == '__main__':
    csv_to_json('20260307.csv', 'rawData.json')
