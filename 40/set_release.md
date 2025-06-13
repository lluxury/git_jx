import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from samples import resource
from utils import emit, find_any_project, find_any_build_definition

logger = logging.getLogger(__name__)

@resource('definition')
def get_definitions(context, save_to_file: Optional[str] = None) -> List[Dict]:
    """
    获取构建定义并可选保存为JSON文件
    
    Args:
        context: 上下文对象
        save_to_file: 保存JSON的文件路径(可选)
    
    Returns:
        构建定义列表
    """
    project = find_any_project(context)
    emit(f"正在获取项目 '{project.name}' 的构建定义...")
    
    build_client = context.connection.clients.get_build_client()
    definitions = build_client.get_definitions(project.id)
    
    # 转换为可序列化的字典格式
    definitions_data = []
    for definition in definitions:
        definition_dict = {
            'id': definition.id,
            'name': definition.name,
            'revision': definition.revision,
            'project': {
                'id': definition.project.id,
                'name': definition.project.name
            },
            # 可以根据需要添加更多字段
            'created_date': definition.created_date.isoformat() if definition.created_date else None,
            'path': definition.path
        }
        definitions_data.append(definition_dict)
        emit(f"{definition.id}: {definition.name} (rev. {definition.revision})")
    
    if save_to_file:
        try:
            with open(save_to_file, 'w', encoding='utf-8') as f:
                json.dump(definitions_data, f, indent=2, ensure_ascii=False)
            emit(f"构建定义已保存到: {save_to_file}")
        except Exception as e:
            logger.error(f"保存构建定义到文件失败: {str(e)}")
            raise
    
    return definitions_data

@resource('definition')
def update_definition_from_file(context, definition_id: int, json_file: str) -> Dict:
    """
    从JSON文件更新构建定义
    
    Args:
        context: 上下文对象
        definition_id: 要更新的定义ID
        json_file: 包含更新内容的JSON文件路径
    
    Returns:
        更新后的构建定义
    """
    if not Path(json_file).exists():
        raise FileNotFoundError(f"JSON文件不存在: {json_file}")
    
    build_client = context.connection.clients.get_build_client()
    
    # 读取修改后的JSON内容
    with open(json_file, 'r', encoding='utf-8') as f:
        updated_definition = json.load(f)
    
    # 获取当前定义以保留必要字段
    current_definition = build_client.get_definition(definition_id)
    
    # 合并更新(保留系统管理的字段)
    updated_definition.update({
        'id': current_definition.id,
        'revision': current_definition.revision,
        'project': {
            'id': current_definition.project.id,
            'name': current_definition.project.name
        }
    })
    
    emit(f"正在更新构建定义 {definition_id}...")
    response = build_client.update_definition(
        definition=updated_definition,
        project=current_definition.project.id,
        definition_id=definition_id
    )
    
    emit(f"成功更新构建定义: {response.id} (rev. {response.revision})")
    return {
        'id': response.id,
        'name': response.name,
        'revision': response.revision,
        'url': response.url
    }

@resource('definition')
def edit_definition_interactive(context, definition_id: int) -> Dict:
    """
    交互式编辑构建定义
    
    Args:
        context: 上下文对象
        definition_id: 要编辑的定义ID
    
    Returns:
        更新后的构建定义
    """
    build_client = context.connection.clients.get_build_client()
    
    # 1. 获取当前定义
    definition = build_client.get_definition(definition_id)
    definition_json = json.dumps(definition.__dict__, indent=2, default=str)
    
    # 2. 创建临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', encoding='utf-8', delete=False) as tmp:
        tmp.write(definition_json)
        tmp_path = tmp.name
    
    # 3. 提示用户编辑
    emit(f"构建定义 {definition_id} 已导出到临时文件: {tmp_path}")
    emit("请使用文本编辑器修改该文件，保存后按回车键继续...")
    input("按回车键继续...")
    
    # 4. 读取修改后的内容并更新
    try:
        return update_definition_from_file(context, definition_id, tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

# 使用示例
if __name__ == "__main__":
    # 假设有一个context对象
    context = get_context()  # 需要实现
    
    # 1. 获取所有定义并保存到文件
    definitions = get_definitions(context, save_to_file="definitions.json")
    
    # 2. 用户可以手动编辑definitions.json文件
    
    # 3. 更新特定定义
    if definitions:
        definition_id = definitions[0]['id']
        update_definition_from_file(context, definition_id, "modified_definition.json")
        
        # 或者使用交互式编辑
        edit_definition_interactive(context, definition_id)
