# 批量查询安全组(Security Group)所属的CloudFormation堆栈

要批量查询某个安全组(Security Group)被哪个CloudFormation堆栈管理，可以使用以下方法：

## 方法1：使用AWS CLI批量查询

### 1. 首先获取安全组ID
```bash
# 获取特定安全组ID（如果已知名称）
SG_ID=$(aws ec2 describe-security-groups --group-names "您的安全组名称" --query "SecurityGroups[0].GroupId" --output text)

# 或者列出所有安全组
aws ec2 describe-security-groups --query "SecurityGroups[*].[GroupId,GroupName]" --output table
```

### 2. 通过资源标签查询所属堆栈
```bash
# 查询安全组的CloudFormation标签
aws ec2 describe-security-groups \
  --group-ids $SG_ID \
  --query "SecurityGroups[0].Tags[?Key=='aws:cloudformation:stack-name'].Value" \
  --output text
```

### 3. 批量查询所有安全组及其所属堆栈
```bash
#!/bin/bash

# 获取所有安全组及其CloudFormation堆栈信息
aws ec2 describe-security-groups \
  --query "SecurityGroups[*].[GroupId, GroupName, Tags[?Key=='aws:cloudformation:stack-name'].Value | [0]]" \
  --output table

# 或者导出到CSV文件
aws ec2 describe-security-groups \
  --query "SecurityGroups[*].[GroupId, GroupName, Tags[?Key=='aws:cloudformation:stack-name'].Value | [0]]" \
  --output text | awk '{print $1","$2","$3}' > sg-stack-mapping.csv
```

## 方法2：使用AWS Resource Groups Tagging API

```bash
# 查询特定安全组所属堆栈
aws resourcegroupstaggingapi get-resources \
  --resource-type-filters "ec2:security-group" \
  --query "ResourceTagMappingList[?ResourceARN.contains('security-group/$SG_ID')].Tags[?Key=='aws:cloudformation:stack-name'].Value" \
  --output text

# 批量查询所有安全组与堆栈的关联
aws resourcegroupstaggingapi get-resources \
  --resource-type-filters "ec2:security-group" \
  --query "ResourceTagMappingList[*].[ResourceARN, Tags[?Key=='aws:cloudformation:stack-name'].Value | [0]]" \
  --output table
```

## 方法3：使用AWS Config高级查询（如果已启用Config）

```bash
# 使用AWS Config SQL查询
aws configservice select-resource-config \
  --expression "SELECT resourceId, resourceName, tags.aws:cloudformation:stack-name WHERE resourceType = 'AWS::EC2::SecurityGroup'"
```

## 方法4：检查CloudFormation堆栈资源

```bash
# 列出所有堆栈
STACKS=$(aws cloudformation describe-stacks --query "Stacks[*].StackName" --output text)

# 检查每个堆栈是否包含该安全组
for stack in $STACKS; do
  if aws cloudformation list-stack-resources --stack-name $stack \
    --query "StackResourceSummaries[?PhysicalResourceId=='$SG_ID'].LogicalResourceId" \
    --output text | grep -q .; then
    echo "安全组 $SG_ID 属于堆栈: $stack"
  fi
done
```

## 注意事项

1. 如果安全组是手动创建的，可能不属于任何CloudFormation堆栈
2. 某些情况下安全组可能被多个堆栈引用（不常见但可能发生）
3. 跨区域查询时，确保CLI配置了正确的region参数
4. 对于大量资源，建议增加CLI的分页参数`--page-size`和`--max-items`

## 推荐方案

对于生产环境，建议使用方法2(Resource Groups Tagging API)，因为它：
- 查询效率最高
- 可以一次性获取所有资源的标签信息
- 支持批量查询多种资源类型

示例输出格式：
```
------------------------------------------------------------------
|                          DescribeSecurityGroups                          |
+---------------------------+---------------------+------------------------+
|  sg-1234567890abcdef0     |  my-security-group  |  my-cloudformation-stack |
|  sg-0987654321abcdef0     |  default            |  None                   |
------------------------------------------------------------------
```
