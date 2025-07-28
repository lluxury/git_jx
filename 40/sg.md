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




    service.beta.kubernetes.io/aws-load-balancer-manage-backend-security-group-rules: "false"
        # 限制允许访问的客户端IP范围
    service.beta.kubernetes.io/aws-load-balancer-source-ranges: "203.0.113.0/24,198.51.100.0/24"



























在 AWS EKS 环境中，当使用 NLB (Network Load Balancer) 时，AWS 会自动配置安全组规则来管理 MTU 发现（Path MTU Discovery）。这条标记为 `kubernetes.io/rule/nlb/mtu` 的 ICMP 规则是 AWS 自动管理的，但您可以通过以下方式查看和修改其范围：

### 1. **查看现有规则**
首先查看 NLB 关联的安全组：
```bash
# 获取集群名称
CLUSTER_NAME=your-eks-cluster-name

# 查找自动创建的 NLB 安全组
aws ec2 describe-security-groups \
  --filters Name=tag-key,Values=elbv2.k8s.aws/cluster Name=tag-value,Values=$CLUSTER_NAME \
  --query "SecurityGroups[?contains(GroupName, 'k8s-traffic')]"
```

### 2. **理解默认规则**
自动创建的 ICMP 规则通常如下：
- **协议**: ICMP (类型 3 "Destination Unreachable", 代码 4 "Fragmentation Needed")
- **源范围**: 0.0.0.0/0 (默认允许所有 IP)
- **标记**: `kubernetes.io/rule/nlb/mtu`

### 3. **修改规则范围**
#### 方案 1：通过标签阻止自动管理
```bash
# 给安全组添加特殊标签阻止控制器修改
aws ec2 create-tags \
  --resources sg-0123456789abcdef \
  --tags Key=elbv2.k8s.aws/resource,Value=do-not-manage
```

#### 方案 2：手动修改规则（需定期维护）
```bash
# 删除自动规则
aws ec2 revoke-security-group-ingress \
  --group-id sg-0123456789abcdef \
  --protocol icmp \
  --port -1 \
  --cidr 0.0.0.0/0

# 添加自定义范围规则（例如仅允许VPC内）
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef \
  --ip-permissions \
    IpProtocol=icmp,FromPort=3,ToPort=4,\
    IpRanges=[{CidrIp=10.0.0.0/16,Description="Custom MTU discovery"}]
```

### 4. **通过 Kubernetes 配置（推荐）**
在 Service 注解中指定安全组：
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-security-groups: "sg-myexistinggroup"
    service.beta.kubernetes.io/aws-load-balancer-extra-security-groups: "sg-extragroup"
spec:
  type: LoadBalancer
```

### 5. **注意事项**
- 修改后需检查 NLB 的健康检查是否正常
- 在 `kube-system/aws-load-balancer-controller` 日志中会看到相关事件：
  ```bash
  kubectl logs -n kube-system deployment/aws-load-balancer-controller | grep security-group
  ```
- 完全禁用自动管理可能影响其他功能的正常工作

建议在测试环境验证后再应用到生产环境。如需严格限制范围，最佳实践是提前创建自定义安全组并通过 Service 注解指定。
    
