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





















# 获取完整构建定义和流水线内容的Python代码

如果您需要获取构建定义的完整JSON内容或整个流水线配置，以下是增强版的代码实现：

## 1. 获取完整构建定义JSON

```python
import json
from typing import Dict, Optional
from samples import resource
from utils import emit

@resource('definition')
def get_full_definition(context, definition_id: int, save_path: Optional[str] = None) -> Dict:
    """
    获取构建定义的完整JSON内容
    
    Args:
        context: 上下文对象
        definition_id: 构建定义ID
        save_path: 保存JSON文件的路径(可选)
    
    Returns:
        完整的构建定义JSON内容
    """
    build_client = context.connection.clients.get_build_client()
    
    # 获取完整定义(包括所有属性和配置)
    full_definition = build_client.get_definition(
        definition_id=definition_id,
        include_all_properties=True
    )
    
    # 转换为完整字典
    definition_dict = full_definition.as_dict()
    
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(definition_dict, f, indent=2, ensure_ascii=False)
            emit(f"完整构建定义已保存到: {save_path}")
        except Exception as e:
            emit(f"保存文件失败: {str(e)}", level='error')
            raise
    
    return definition_dict
```

## 2. 获取完整流水线配置

```python
@resource('pipeline')
def get_full_pipeline_config(context, definition_id: int, save_path: Optional[str] = None) -> Dict:
    """
    获取完整的流水线配置(包括所有阶段、任务和变量)
    
    Args:
        context: 上下文对象
        definition_id: 构建定义ID
        save_path: 保存JSON文件的路径(可选)
    
    Returns:
        完整的流水线配置
    """
    build_client = context.connection.clients.get_build_client()
    
    # 获取完整定义
    full_definition = build_client.get_definition(
        definition_id=definition_id,
        include_all_properties=True,
        include_configuration=True
    )
    
    # 获取流水线配置
    config = build_client.get_build_configuration(
        definition_id=definition_id,
        revision=full_definition.revision
    )
    
    # 组合结果
    pipeline_data = {
        'definition': full_definition.as_dict(),
        'configuration': config.as_dict(),
        'yaml': getattr(full_definition, 'yaml', None)  # 如果是YAML流水线
    }
    
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(pipeline_data, f, indent=2, ensure_ascii=False)
            emit(f"完整流水线配置已保存到: {save_path}")
        except Exception as e:
            emit(f"保存文件失败: {str(e)}", level='error')
            raise
    
    return pipeline_data
```

## 3. 使用示例

```python
# 获取特定构建定义的完整JSON
definition_id = 123  # 替换为实际定义ID
full_definition = get_full_definition(context, definition_id, "full_definition.json")

# 获取完整流水线配置(包括阶段、任务等)
pipeline_config = get_full_pipeline_config(context, definition_id, "pipeline_config.json")

# 打印YAML配置(如果可用)
if pipeline_config.get('yaml'):
    print("YAML配置:")
    print(pipeline_config['yaml'])
else:
    print("JSON配置:")
    print(json.dumps(pipeline_config['configuration'], indent=2))
```

## 关键点说明

1. **`as_dict()` 方法**:
   - 将Azure DevOps对象转换为完整字典
   - 包含所有属性和嵌套结构

2. **`include_all_properties=True`**:
   - 确保返回所有属性，而不仅仅是摘要

3. **`include_configuration=True`**:
   - 获取流水线配置细节(阶段、任务等)

4. **YAML流水线支持**:
   - 检查并返回YAML配置(如果是YAML定义的流水线)

5. **错误处理**:
   - 文件保存错误处理
   - 清晰的用户反馈

## 高级用法

如果您需要更细粒度的控制，可以添加以下功能：

```python
@resource('pipeline')
def export_pipeline_with_resources(context, definition_id: int) -> Dict:
    """
    导出流水线及其相关资源(变量组、服务连接等)
    """
    build_client = context.connection.clients.get_build_client()
    extension_client = context.connection.clients.get_extension_client()
    
    # 获取定义
    definition = build_client.get_definition(definition_id, include_all_properties=True)
    
    # 获取变量组
    variable_groups = []
    for vg_id in definition.variable_groups or []:
        variable_groups.append(
            extension_client.get_variable_group(vg_id)
    
    # 获取服务连接
    service_connections = []
    for sc_id in definition.service_connections or []:
        service_connections.append(
            extension_client.get_service_endpoint(sc_id))
    
    return {
        'definition': definition.as_dict(),
        'variable_groups': [vg.as_dict() for vg in variable_groups],
        'service_connections': [sc.as_dict() for sc in service_connections],
        'repositories': definition.repository.as_dict() if definition.repository else None
    }
```

这个版本提供了获取构建定义和流水线完整内容的能力，包括所有配置细节和可选的文件保存功能。






# 获取 Release 流水线完整信息的 Python 代码

以下是获取 Azure DevOps Release 流水线完整信息的 Python 实现，包括发布定义、阶段、任务和关联的构建工件等完整 JSON 输出：

```python
import json
from typing import Dict, List, Optional
from samples import resource
from utils import emit

@resource('release')
def get_full_release_definition(context, definition_id: int, save_path: Optional[str] = None) -> Dict:
    """
    获取 Release 流水线的完整定义
    
    Args:
        context: 上下文对象
        definition_id: Release 定义ID
        save_path: 保存JSON文件的路径(可选)
    
    Returns:
        完整的 Release 定义JSON内容
    """
    release_client = context.connection.clients.get_release_client()
    
    # 获取完整 Release 定义
    release_definition = release_client.get_release_definition(
        definition_id=definition_id,
        property_filters='*'  # 获取所有属性
    )
    
    # 转换为完整字典
    release_dict = release_definition.as_dict()
    
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(release_dict, f, indent=2, ensure_ascii=False)
            emit(f"完整 Release 定义已保存到: {save_path}")
        except Exception as e:
            emit(f"保存文件失败: {str(e)}", level='error')
            raise
    
    return release_dict

@resource('release')
def get_release_pipeline_details(context, definition_id: int) -> Dict:
    """
    获取 Release 流水线完整详细信息(包括阶段、任务、变量和触发器)
    
    Args:
        context: 上下文对象
        definition_id: Release 定义ID
    
    Returns:
        包含所有详细信息的字典
    """
    release_client = context.connection.clients.get_release_client()
    
    # 1. 获取基本定义
    release_def = release_client.get_release_definition(definition_id, property_filters='*')
    
    # 2. 获取所有环境(阶段)
    environments = []
    for env in release_def.environments:
        env_details = release_client.get_environment(
            project=release_def.project.id,
            definition_id=definition_id,
            environment_id=env.id
        )
        environments.append(env_details.as_dict())
    
    # 3. 获取变量
    variables = release_def.variables.as_dict() if release_def.variables else {}
    
    # 4. 获取触发器
    triggers = []
    if hasattr(release_def, 'triggers'):
        for trigger in release_def.triggers:
            triggers.append(trigger.as_dict())
    
    # 5. 获取工件(构建)定义
    artifacts = []
    if hasattr(release_def, 'artifacts'):
        for artifact in release_def.artifacts:
            artifact_detail = release_client.get_artifact(
                project=release_def.project.id,
                release_id=None,  # 获取定义级别的工件
                artifact_type=artifact.type,
                artifact_name=artifact.alias
            )
            artifacts.append(artifact_detail.as_dict())
    
    return {
        'definition': release_def.as_dict(),
        'environments': environments,
        'variables': variables,
        'triggers': triggers,
        'artifacts': artifacts,
        'revision': release_def.revision,
        'created_by': release_def.created_by.as_dict() if hasattr(release_def.created_by, 'as_dict') else str(release_def.created_by),
        'modified_by': release_def.modified_by.as_dict() if hasattr(release_def.modified_by, 'as_dict') else str(release_def.modified_by)
    }

@resource('release')
def export_release_pipeline(context, definition_id: int, save_path: Optional[str] = None) -> Dict:
    """
    导出完整的 Release 流水线配置
    
    Args:
        context: 上下文对象
        definition_id: Release 定义ID
        save_path: 保存JSON文件的路径(可选)
    
    Returns:
        完整 Release 流水线配置
    """
    full_details = get_release_pipeline_details(context, definition_id)
    
    if save_path:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(full_details, f, indent=2, ensure_ascii=False)
            emit(f"完整 Release 流水线配置已保存到: {save_path}")
        except Exception as e:
            emit(f"保存文件失败: {str(e)}", level='error')
            raise
    
    return full_details

# 使用示例
if __name__ == "__main__":
    # 假设有一个context对象
    context = get_context()  # 需要实现
    
    # 获取 Release 定义ID列表
    release_client = context.connection.clients.get_release_client()
    release_definitions = release_client.get_release_definitions(project="YourProjectName")
    
    if release_definitions:
        # 获取第一个 Release 定义的完整信息
        definition_id = release_definitions[0].id
        full_release = export_release_pipeline(context, definition_id, "release_pipeline.json")
        
        # 打印摘要信息
        print(f"Release 名称: {full_release['definition']['name']}")
        print(f"阶段数量: {len(full_release['environments'])}")
        print(f"变量数量: {len(full_release['variables'])}")
        print(f"工件数量: {len(full_release['artifacts'])}")
```

## 功能说明

1. **`get_full_release_definition`**:
   - 获取 Release 定义的基本完整 JSON
   - 包含所有属性和配置

2. **`get_release_pipeline_details`**:
   - 获取 Release 流水线的完整详细信息
   - 包括阶段(环境)、任务、变量、触发器和工件

3. **`export_release_pipeline`**:
   - 导出完整 Release 流水线配置
   - 可选保存为 JSON 文件

## 输出内容结构

返回的 JSON 包含以下主要部分：

```json
{
  "definition": {
    "id": 1,
    "name": "Production Release",
    "path": "\\",
    "revision": 5,
    "createdOn": "2023-01-01T00:00:00Z",
    "modifiedOn": "2023-01-10T00:00:00Z"
  },
  "environments": [
    {
      "id": 1,
      "name": "Dev",
      "tasks": [...],
      "conditions": [...],
      "variables": {...}
    },
    {
      "id": 2,
      "name": "Production",
      "approvals": [...],
      "tasks": [...]
    }
  ],
  "variables": {
    "configUrl": {
      "value": "https://config.example.com",
      "isSecret": false
    }
  },
  "triggers": [...],
  "artifacts": [
    {
      "alias": "_Build",
      "type": "Build",
      "definitionReference": {
        "definition": {
          "id": "123",
          "name": "Build Pipeline"
        }
      }
    }
  ]
}
```

## 高级用法

如果需要更详细的控制，可以添加以下功能：

```python
@resource('release')
def get_environment_tasks(context, definition_id: int, environment_id: int) -> List[Dict]:
    """
    获取特定环境的所有任务
    """
    release_client = context.connection.clients.get_release_client()
    
    tasks = release_client.get_environment_tasks(
        project=context.project.name,
        definition_id=definition_id,
        environment_id=environment_id
    )
    
    return [task.as_dict() for task in tasks]

@resource('release')
def get_release_artifacts(context, release_id: int) -> List[Dict]:
    """
    获取特定发布版本的工件详情
    """
    release_client = context.connection.clients.get_release_client()
    
    artifacts = release_client.get_release_artifacts(
        project=context.project.name,
        release_id=release_id
    )
    
    return [artifact.as_dict() for artifact in artifacts]
```

这段代码提供了获取 Azure DevOps Release 流水线完整信息的能力，可以根据需要进一步扩展或修改。




20

# 在 Azure DevOps 中更新 Release 定义的方法

要将修改后的 JSON 更新回 Azure DevOps 的 Release 定义，您需要遵循以下步骤：

## 1. 准备更新代码

```python
import json
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# 1. 设置连接
organization_url = 'https://dev.azure.com/your-organization'
personal_access_token = 'your-pat-token'  # 需要有Release管理权限
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# 2. 获取Release客户端
release_client = connection.clients.get_release_client()

def update_release_definition(project_name, release_definition_json):
    """
    更新Release定义
    
    Args:
        project_name: 项目名称
        release_definition_json: 修改后的Release定义JSON
    """
    try:
        # 3. 确保保留必要的元数据
        if 'id' not in release_definition_json:
            raise ValueError("Release定义必须包含id字段")
        
        # 4. 更新Release定义
        updated_definition = release_client.update_release_definition(
            release_definition=release_definition_json,
            project=project_name
        )
        
        print(f"成功更新Release定义: {updated_definition.name} (ID: {updated_definition.id})")
        return updated_definition
    except Exception as e:
        print(f"更新失败: {str(e)}")
        raise
```

## 2. 完整工作流程

```python
# 1. 从文件读取修改后的定义
with open('modified_release_definition.json', 'r') as f:
    modified_definition = json.load(f)

# 2. 更新定义
update_release_definition(
    project_name="Your Project Name",
    release_definition_json=modified_definition
)
```

## 3. 关键注意事项

1. **必须保留的字段**：
   - `id`: Release定义ID
   - `revision`: 当前版本号（用于冲突检测）

2. **建议更新前检查**：
   ```python
   # 获取当前最新版本
   current_def = release_client.get_release_definition(
       project="Your Project Name",
       definition_id=modified_definition['id']
   )
   
   # 确保revision匹配
   if modified_definition.get('revision') != current_def.revision:
       print("警告：本地版本与服务器版本不一致，可能已被他人修改")
       # 可以选择合并变更或强制更新
       modified_definition['revision'] = current_def.revision
   ```

3. **部分更新方法**：
   ```python
   # 如果只想更新特定部分（如变量）
   def update_release_variables(project_name, definition_id, new_variables):
       current_def = release_client.get_release_definition(project_name, definition_id)
       current_def.variables = new_variables
       return release_client.update_release_definition(current_def, project_name)
   ```

## 4. 错误处理建议

1. **版本冲突**：
   - 如果收到 `409 Conflict` 错误，说明有人已修改过定义
   - 解决方案：重新获取最新版本，重新应用您的修改

2. **权限问题**：
   - 确保PAT有足够的权限（Release管理员）

3. **验证变更**：
   ```python
   # 更新后验证
   updated_def = release_client.get_release_definition(
       project="Your Project Name",
       definition_id=modified_definition['id']
   )
   print(f"当前版本号: {updated_def.revision}")
   ```

## 5. 完整示例脚本

```python
import json
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

def get_authenticated_client():
    """创建认证客户端"""
    org_url = 'https://dev.azure.com/your-organization'
    pat = 'your-pat-token'
    return Connection(base_url=org_url, creds=BasicAuthentication('', pat)).get_release_client()

def load_and_validate_definition(file_path):
    """加载并验证定义文件"""
    with open(file_path, 'r') as f:
        definition = json.load(f)
    
    if 'id' not in definition:
        raise ValueError("Definition must contain 'id' field")
    return definition

def update_definition_with_retry(client, project, definition, max_retries=3):
    """带重试机制的更新"""
    for attempt in range(max_retries):
        try:
            # 获取当前版本
            current = client.get_release_definition(project, definition['id'])
            definition['revision'] = current.revision
            
            # 尝试更新
            return client.update_release_definition(definition, project)
        
        except Exception as e:
            if '409' in str(e) and attempt < max_retries - 1:
                print(f"版本冲突，重试 {attempt + 1}/{max_retries}")
                continue
            raise

if __name__ == "__main__":
    try:
        client = get_authenticated_client()
        modified_def = load_and_validate_definition('modified_release.json')
        
        result = update_definition_with_retry(
            client=client,
            project="Your Project",
            definition=modified_def
        )
        
        print(f"成功更新定义: {result.name} (Rev. {result.revision})")
    
    except Exception as e:
        print(f"更新失败: {str(e)}")
```

## 6. 最佳实践建议

1. **备份原始定义**：更新前总是保留原始定义的备份
2. **小步更新**：尽量只修改必要的部分，而不是整个定义
3. **测试环境**：先在测试项目/定义上验证您的更新逻辑
4. **变更日志**：记录您所做的修改，便于追踪

通过以上方法，您可以安全地将修改后的 JSON 定义更新回 Azure DevOps。
