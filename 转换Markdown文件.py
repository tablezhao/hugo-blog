#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

# 设置目录路径
source_dir = os.path.join(os.path.dirname(__file__), 'ghost-markdown')
target_dir = os.path.join(os.path.dirname(__file__), 'content', 'blog')

# 创建目标目录
os.makedirs(target_dir, exist_ok=True)

print("开始批量转换Ghost Markdown文件到Hugo格式...")
print()

# 获取所有Markdown文件
md_files = [f for f in os.listdir(source_dir) if f.endswith('.md')]

success_count = 0
failure_count = 0

for md_file in md_files:
    try:
        print(f"处理: {md_file}")
        
        # 从文件名提取文章名（去除日期部分）
        file_name = os.path.splitext(md_file)[0]
        article_name = ""
        
        # 移除文件名中的日期前缀 (yyyy-mm-dd-)
        if re.match(r'^\d{4}-\d{2}-\d{2}-', file_name):
            article_name = file_name[11:]  # 移除前11个字符 (yyyy-mm-dd-)
        else:
            article_name = file_name
        
        # 生成输出文件名
        output_file = os.path.join(target_dir, f"{article_name}.md")
        
        # 读取原文件内容
        source_file_path = os.path.join(source_dir, md_file)
        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
        
        # 提取Ghost元数据
        ghost_metadata = {}
        in_metadata = False
        
        for line in content:
            line = line.strip()
            if line == '---':
                in_metadata = not in_metadata
                continue
            if in_metadata:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    ghost_metadata[key] = value
        
        # 提取所需字段
        title = ghost_metadata.get('title', article_name).strip('"')
        
        # 处理日期
        date_str = "2023-01-01T00:00:00+08:00"
        if 'date_published' in ghost_metadata:
            # 解析ISO格式日期
            try:
                iso_date = ghost_metadata['date_published'].strip('"')
                # 转换为datetime对象
                dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
                # 转换为Hugo需要的格式 (UTC+8)
                date_str = dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")
            except:
                print(f"  警告: 日期格式解析错误，使用默认日期")
        
        # 处理标签
        tags = []
        if 'tags' in ghost_metadata:
            tags_str = ghost_metadata['tags'].strip('"')
            # 分割标签（支持空格分隔）
            tags = [tag.strip() for tag in tags_str.split() if tag.strip()]
        
        # 写入Hugo格式的新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            # 1. 写入前置元数据
            f.write("---\n")
            f.write(f"title: \"{title}\"\n")
            f.write(f"date: {date_str}\n")
            f.write(f"tags: {tags}\n")
            f.write("featured: true\n")
            f.write("---\n\n")
            f.write("<!--more-->\n\n")
            
            # 2. 写入文章内容（跳过Ghost元数据）
            skip_metadata = True
            for line in content:
                line = line.rstrip('\n')
                if line == '---':
                    skip_metadata = not skip_metadata
                    continue
                if not skip_metadata:
                    # 跳过Ghost特定的元数据行
                    if line.strip().startswith(("title:", "slug:", "date_published:", "date_updated:", "tags:")):
                        continue
                else:
                    # 只写入文章内容部分
                    f.write(f"{line}\n")
        
        print(f"  成功: 已创建 {article_name}.md")
        success_count += 1
        
    except Exception as e:
        print(f"  错误: {str(e)}")
        failure_count += 1

print()
print(f"转换完成！")
print(f"成功转换: {success_count} 个文件")
print(f"转换失败: {failure_count} 个文件")
input("按 Enter 键退出...")
