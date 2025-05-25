import os
import yaml

def analyze_imports_in_directory(directory_path):
    # 用一个集合来存储所有文件的导入语句，确保去重
    all_imports = set()

    # 遍历目录下的所有文件
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):  # 只处理.py文件
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                # 获取文件的导入语句，并将其添加到集合中
                all_imports.update(analyze_imports(file_path))
    
    # 处理带有"."的导入语句，输出层级结构
    processed_imports = process_imports(all_imports)
    
    # 打印为 YAML 格式输出
    print(yaml.dump(processed_imports, default_flow_style=False, allow_unicode=True))

def analyze_imports(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 存储拆分后的导入语句
    imports = set()  # 使用set来去重
    
    for line in lines:
        # 清除行首尾空格
        line = line.strip()

        # 如果是import语句
        if line.startswith("import "):
            # 处理多包导入的情况，如：import os, sys
            parts = line.split("import")[1].strip().split(",")
            for part in parts:
                # 处理as情况，丢弃别名
                part = part.split(" as ")[0].strip()
                imports.add(f"{part}")
        
        # 如果是from语句
        elif line.startswith("from "):
            # 处理from语句，将其转换为import形式
            if "import" in line:
                base_package = line.split("import")[0].strip()[5:]  # 获取from后的包名
                modules = line.split("import")[1].strip().split(",")  # 获取模块列表
                for module in modules:
                    # 处理as情况，丢弃别名
                    module = module.split(" as ")[0].strip()
                    # 转换为 package.module 形式
                    imports.add(f"{base_package}.{module}")
            else:
                imports.add(line)
    
    return imports

def process_imports(imports):
    """
    对带有点号（`.`）的导入语句进行处理，输出层级结构。
    """
    processed = {}
    for imp in imports:
        if "." in imp:
            levels = imp.split(".")
            current = processed
            for level in levels:
                if level not in current:
                    current[level] = {}
                current = current[level]
        else:
            processed[imp] = {}
    return processed

# 输入你需要分析的目录路径
directory_path = "/Users/yann/python_workspace/Mastering-Machine-Learning-with-scikit-learn-Second-Edition-master/"
analyze_imports_in_directory(directory_path)
