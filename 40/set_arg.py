根据需求，我们需要实现通过命令行参数指定构建定义ID的功能。以下是分步骤的改造方案：

---

### 1. 修改命令行参数解析 (`runner.py`)
```python
# 在run命令解析器中新增参数
run_parser.add_argument('--definition-id', help='指定构建定义ID', type=int)
run_parser.add_argument('--definition-name', help='指定构建定义名称(模糊匹配)')
```

---

### 2. 增强 `find_any_build_definition` 函数 (`utils.py`)
```python
def find_build_definition(context, definition_id=None, definition_name=None):
    """支持多种方式查找构建定义"""
    logger.debug('查找构建定义: id=%s, name=%s', definition_id, definition_name)
    
    # 缓存检查（优先匹配参数）
    if hasattr(context.runner_cache, 'build_definition'):
        cached = context.runner_cache.build_definition
        if (definition_id and cached.id == definition_id) or \
           (definition_name and definition_name.lower() in cached.name.lower()):
            return cached

    # 获取定义列表
    with http_logging.temporarily_disabled():
        project = find_any_project(context)
        build_client = context.connection.clients.get_build_client()
        definitions = build_client.get_definitions(project.id)

    # 精确ID匹配
    if definition_id:
        for d in definitions:
            if d.id == definition_id:
                context.runner_cache.build_definition = d
                return d
        raise AccountStateError(f'未找到ID为 {definition_id} 的构建定义')

    # 名称模糊匹配
    if definition_name:
        lower_name = definition_name.lower()
        matched = [d for d in definitions if lower_name in d.name.lower()]
        if matched:
            context.runner_cache.build_definition = matched[0]
            return matched[0]
        raise AccountStateError(f'未找到名称包含 "{definition_name}" 的构建定义')

    # 默认返回第一个
    if definitions:
        context.runner_cache.build_definition = definitions[0]
        return definitions[0]
        
    raise AccountStateError(f'项目 "{project.name}" 中没有构建定义')
```

---

### 3. 改造 `queue_build` 示例函数 (`samples/build.py`)
```python
@resource('build')
def queue_build(context, definition_id=None, definition_name=None):
    """支持参数化构建"""
    definition = find_build_definition(
        context,
        definition_id=getattr(context, 'definition_id', None),
        definition_name=getattr(context, 'definition_name', None)
    )
    
    build_client = context.connection.clients.get_build_client()
    response = build_client.queue_build(
        build={'definition': {'id': definition.id}},
        project=definition.project.id
    )
    
    emit(f"已触发构建: [ID:{response.id}] {definition.name}")
    emit(f"构建URL: {response.url}")
    return response
```

---

### 4. 修改 `run_cmd` 处理器 (`runner.py`)
```python
def run_cmd(args, config):
    # ...原有代码...
    
    # 将参数注入context
    context.definition_id = args.definition_id
    context.definition_name = args.definition_name
    
    main(**args_dict, auth_token=auth_token)
```

---

### 5. 使用示例

#### 通过ID构建：
```bash
python runner.py run build build --definition-id 123
```

#### 通过名称模糊匹配构建：
```bash
python runner.py run build build --definition-name "CI"
```

#### 输出示例：
```
已触发构建: [ID:789] CI-Pipeline
构建URL: https://dev.azure.com/org/project/_build/results?buildId=789
```

---

### 6. 改造后架构变化

```mermaid
graph LR
    CLI[命令行参数] --> Parser[参数解析器]
    Parser --> Context[注入context]
    Context --> Finder[增强的find_build_definition]
    Finder --> Queue[queue_build执行]
```

---

### 关键修改点总结

1. **向后兼容**：
   - 不指定参数时保持原有行为
   - 所有修改都是增量式添加

2. **灵活的查找方式**：
   - 同时支持ID精确匹配和名称模糊匹配
   - 清晰的错误反馈

3. **上下文传递**：
   - 通过`context`对象跨函数传递参数
   - 保持函数签名简洁

4. **可观测性**：
   - 增强的日志输出
   - 用户友好的结果展示

建议在实际修改前，先在测试环境中验证参数传递链路是否畅通，特别是检查`context`对象在不同函数间的参数传递是否正确。











要增加 `revision` 参数支持构建特定版本的流水线定义，需要进行以下修改：

---

### 1. 修改命令行参数解析 (`runner.py`)
```python
# 在run命令解析器中新增revision参数
run_parser.add_argument('--revision', help='指定构建定义版本号', type=int)
```

---

### 2. 增强构建定义查找函数 (`utils.py`)
```python
def find_build_definition(context, definition_id=None, definition_name=None, revision=None):
    """支持版本号查询的构建定义查找"""
    logger.debug('查找构建定义: id=%s, name=%s, revision=%s', 
                definition_id, definition_name, revision)
    
    # 获取基础定义
    definition = _find_base_definition(context, definition_id, definition_name)
    
    # 需要特定版本时
    if revision is not None:
        build_client = context.connection.clients.get_build_client()
        version_def = build_client.get_definition_revision(
            project=definition.project.id,
            definition_id=definition.id,
            revision=revision
        )
        version_def.project = definition.project  # 保持项目关联
        return version_def
        
    return definition

def _find_base_definition(context, definition_id, definition_name):
    """原始查找逻辑抽离"""
    # ...保留之前实现的查找逻辑...
```

---

### 3. 修改构建触发函数 (`samples/build.py`)
```python
@resource('build')
def queue_build(context):
    definition = find_build_definition(
        context,
        definition_id=getattr(context, 'definition_id', None),
        definition_name=getattr(context, 'definition_name', None),
        revision=getattr(context, 'revision', None)
    )
    
    build_params = {
        'definition': {
            'id': definition.id,
            'revision': definition.revision  # 显式传递版本号
        }
    }
    
    build_client = context.connection.clients.get_build_client()
    response = build_client.queue_build(
        build=build_params,
        project=definition.project.id
    )
    
    emit(f"已触发构建 [定义版本 {definition.revision}]: {response.id}")
    return response
```

---

### 4. 参数传递 (`runner.py`)
```python
def run_cmd(args, config):
    # ...原有代码...
    context.revision = args.revision  # 注入revision参数
```

---

### 5. 使用示例

#### 触发特定版本构建：
```bash
python runner.py run build build --definition-id 123 --revision 5
```

#### 输出示例：
```
已触发构建 [定义版本 5]: 789
构建详情: https://dev.azure.com/org/project/_build/results?buildId=789
```

---

### 关键修改点说明

1. **版本控制参数**：
   - 新增 `--revision` 可选参数
   - 通过 `get_definition_revision` API 获取历史版本

2. **构建请求结构**：
   ```json
   {
     "definition": {
       "id": 123,
       "revision": 5  // 新增版本号字段
     }
   }
   ```

3. **数据完整性**：
   - 从历史版本恢复的定义对象手动关联project信息
   - 日志中明确显示使用的版本号

4. **API文档参考**：
   - [获取定义版本](https://docs.microsoft.com/en-us/rest/api/azure/devops/build/definitions/get%20definition%20revision)
   - [排队构建参数](https://docs.microsoft.com/en-us/rest/api/azure/devops/build/builds/queue)

---

### 异常处理建议

在 `find_build_definition` 中添加版本校验：
```python
if revision is not None:
    if revision < 1:
        raise ValueError("版本号必须大于0")
    try:
        version_def = build_client.get_definition_revision(...)
    except Exception as e:
        raise AccountStateError(f"获取版本 {revision} 失败: {str(e)}")
```

---

### 改造后架构变化

```mermaid
sequenceDiagram
    participant CLI as 命令行
    participant Runner as Runner.py
    participant Utils as utils.py
    participant Build as build.py
    participant API as Azure API
    
    CLI->>Runner: run build build --revision 5
    Runner->>Utils: find_build_definition(revision=5)
    Utils->>API: get_definition_revision(123,5)
    API-->>Utils: 返回版本5定义
    Utils->>Build: 返回定义对象
    Build->>API: queue_build(含revision)
    API-->>Build: 返回构建结果
    Build->>CLI: 输出构建信息
```

这种修改保持了向后兼容性，同时增加了精确版本控制能力，特别适合需要回滚到历史稳定版本的场景。












以下是简化版改造方案：

---

### 1. 修改命令行参数（`runner.py`）
```python
run_parser.add_argument('--rev', type=int, help='指定构建定义版本号')
```

### 2. 修改查找函数（`utils.py`）
```python
def find_build_definition(context, rev=None):
    definition = _original_find_definition(context)  # 原有查找逻辑
    
    if rev:
        client = context.connection.clients.get_build_client()
        definition = client.get_definition_revision(
            project=definition.project.id,
            definition_id=definition.id,
            revision=rev
        )
    return definition
```

### 3. 修改构建函数（`samples/build.py`）
```python
@resource('build')
def queue_build(context):
    definition = find_build_definition(context, rev=getattr(context, 'rev', None))
    
    response = context.connection.clients.get_build_client().queue_build(
        build={
            'definition': {
                'id': definition.id,
                **({'revision': definition.revision} if hasattr(definition, 'revision') else {})
            }
        },
        project=definition.project.id
    )
    emit(f"Triggered build (Rev: {getattr(definition, 'revision', 'latest')}) ID: {response.id}")
    return response
```

### 4. 参数注入（`runner.py`）
```python
context.rev = args.rev  # 单字母参数更简洁
```

### 使用示例
```bash
# 触发最新版本
python runner.py run build build  

# 触发特定版本
python runner.py run build build --rev 2
```

### 关键点
1. 参数简化为 `--rev`
2. 自动兼容无版本号场景
3. 构建请求动态包含版本号
4. 输出显示使用的版本

这样修改只需改动3处代码，保持原有功能同时增加版本控制能力。







以下是极简改造方案（保持 `--revision` 完整参数名，仅简化实现）：

### 1. 只改关键文件 (`runner.py` 和 `samples/build.py`)

```python
# runner.py 修改
run_parser.add_argument('--revision', '-r', type=int, help='定义版本号')  # 添加-r简写

# samples/build.py 修改
@resource('build')
def queue_build(context):
    client = context.connection.clients.get_build_client()
    definition = find_any_build_definition(context)
    
    # 获取版本（核心修改点）
    rev = getattr(context, 'revision', None)
    build_def = {
        'id': definition.id,
        **({'revision': rev} if rev else {})  # 动态添加版本字段
    }
    
    response = client.queue_build(
        build={'definition': build_def},
        project=definition.project.id
    )
    emit(f"Triggered build (v{rev or 'latest'}): {response.url}")
    return response
```

### 2. 使用示例
```bash
# 完整参数
python runner.py run build build --revision 2

# 简写参数
python runner.py run build build -r 2  
```

### 特点
1. **最小改动**：仅需修改2个文件，不碰查找逻辑
2. **自动兼容**：无`-r`时使用最新版本
3. **清晰输出**：显示实际使用的版本号
4. **完整保留**：仍支持`--revision`完整参数名

其他文件（如`utils.py`）无需修改，保持原查找逻辑即可。这是最简洁的向后兼容方案。














在 Azure DevOps Python Runner 系统中，可以通过以下几种方式在函数间传递对象（如 `definitions` 对象）：

---

### **方法 1：使用 `context.runner_cache` (推荐)**
这是现有框架的标准方式，最适合在示例函数间传递数据。

#### 修改 `get_definitions()` 函数
```python
@resource('definition')
def get_definitions(context):
    project = find_any_project(context)
    build_client = context.connection.clients.get_build_client()
    definitions = build_client.get_definitions(project.id)
    
    # 存储到上下文缓存
    context.runner_cache.build_definitions = definitions
    return definitions
```

#### 在 `queue_build()` 中获取
```python
@resource('build')
def queue_build(context):
    # 从缓存获取definitions
    definitions = getattr(context.runner_cache, 'build_definitions', None)
    
    if not definitions:
        definitions = get_definitions(context)  # 重新获取
        
    # 使用definitions对象...
    selected_def = definitions[0]  # 示例：选择第一个定义
```

---

### **方法 2：通过返回值传递**
适用于直接调用的场景。

#### 链式调用示例
```python
def workflow(context):
    # 先获取definitions
    definitions = get_definitions(context)
    
    # 再传递给build函数
    result = queue_build_with_definitions(context, definitions)
```

---

### **方法 3：增强 `find_any_build_definition()`**
改造现有查找函数使其支持从缓存获取。

#### 修改后的查找函数
```python
def find_any_build_definition(context, use_cache=True):
    if use_cache and hasattr(context.runner_cache, 'build_definitions'):
        return context.runner_cache.build_definitions[0]  # 返回缓存中的第一个
    
    # 原始获取逻辑...
```

---

### **方法 4：参数注入（适合自定义场景）**
通过修改 `context` 对象动态添加属性。

#### 在调用前注入
```python
# 在run_cmd或调用函数中
context.requested_definition_id = 123  # 自定义参数

# 在queue_build中读取
def queue_build(context):
    target_id = getattr(context, 'requested_definition_id', None)
```

---

### **最佳实践建议**
1. **优先使用 `context.runner_cache`**  
   现有框架已为此设计，保持代码一致性。

2. **缓存有效期**  
   添加时间戳判断缓存是否过期：
   ```python
   if not hasattr(context.runner_cache, '_defs_expire') or \
      context.runner_cache._defs_expire < time.time():
       refresh_definitions(context)
   ```

3. **异常处理**  
   缓存不存在时的回退方案：
   ```python
   try:
       return context.runner_cache.build_definitions
   except AttributeError:
       return fetch_definitions(context)
   ```

4. **类型提示（Python 3.9+）**  
   明确缓存对象类型：
   ```python
   from typing import List
   from azure.devops.v7_1.build.models import BuildDefinition

   context.runner_cache.build_definitions: List[BuildDefinition] = definitions
   ```

---

### **完整调用链示例**
```mermaid
sequenceDiagram
    participant User
    participant Runner
    participant BuildSamples
    
    User->>Runner: run build build --use-cache
    Runner->>BuildSamples: get_definitions(context)
    BuildSamples->>Runner: 存储到context.runner_cache
    Runner->>BuildSamples: queue_build(context)
    BuildSamples->>Runner: 从cache读取definitions
    Runner->>User: 输出构建结果
```

---

### **各方法对比**

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| `context.runner_cache` | 框架原生支持 | 需处理缓存失效 | 大多数情况 |
| 返回值传递 | 直接明确 | 需修改调用链 | 简单工作流 |
| 增强查找函数 | 逻辑集中 | 需改造现有函数 | 需要智能查找时 |
| 参数注入 | 高度灵活 | 破坏封装性 | 特殊定制需求 |

选择方法 1（`runner_cache`）最能保持现有代码风格，同时满足对象传递需求。
