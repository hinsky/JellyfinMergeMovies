#! /usr/bin/env python3

import sqlite3
import requests

# 设置变量
api_key = ""
url = ""
db = ""

# 连接数据库
conn = sqlite3.connect(db)
cursor = conn.cursor()

# 查询数据库
cursor.execute("""
    SELECT DISTINCT
        SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb='),
            CASE
                WHEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb=')), '|') > 0
                THEN INSTR(SUBSTR(ProviderIds, INSTR(ProviderIds, 'Tmdb=') + LENGTH('Tmdb=')), '|') - 1
                ELSE LENGTH(ProviderIds)
            END) AS ExtractedProviderValue,
        PresentationUniqueKey,
        Name
    FROM
        TypedBaseItems
    WHERE
        type = 'MediaBrowser.Controller.Entities.Movies.Movie'
        AND IsVirtualItem = '0'
        AND ProviderIds LIKE '%Tmdb=%'
    ORDER BY
        ExtractedProviderValue
""")
video_data = cursor.fetchall()

# 关闭数据库连接
conn.close()

# 遍历数组VideoData，删除唯一的ProviderIds行数据
unique_provider_ids = set([data[0] for data in video_data])
for provider_id in unique_provider_ids:
    if sum(1 for data in video_data if data[0] == provider_id) == 1:
        video_data = [data for data in video_data if data[0] != provider_id]

# 找出重复的ProviderIds行数据并执行合并操作
for provider_id in unique_provider_ids:
    if sum(1 for data in video_data if data[0] == provider_id) > 1:
        # 组合PresentationUniqueKey和name值
        ids = ",".join([data[1] for data in video_data if data[0] == provider_id])
        names = ",".join([data[2] for data in video_data if data[0] == provider_id])
        # 构建curl post请求
        merge_url = f"{url}/Videos/MergeVersions?api_key={api_key}&ids={ids}"
        # 发送请求
        #print(merge_url)
        response = requests.post(merge_url)
        # 输出执行结果
        if response.status_code == 204:
            print(f"Merged versions count: {len(ids.split(','))} {names}")
        else:
            print(f"Error occurred while merging versions: {ids} {names}")
            continue
