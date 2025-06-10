以下是将上述 CloudFront 配置转换为 CloudFormation 模板的完整代码，包括 S3 存储桶和相关策略的创建：

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudFront distribution for CMS and Core websites with CORS support'

Parameters:
  CmsDomainName:
    Type: String
    Description: 'Domain name for CMS website (e.g. cms.example.com)'
  CoreDomainName:
    Type: String
    Description: 'Domain name for Core website (e.g. core.example.com)'
  CertificateArn:
    Type: String
    Description: 'ARN of the ACM certificate covering both domains'

Resources:
  # S3 Buckets
  CmsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'cms-bucket-${AWS::AccountId}-${AWS::Region}'
      AccessControl: Private
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders: ['*']
            AllowedMethods: ['GET', 'HEAD']
            AllowedOrigins: [!Ref CoreDomainName]
            MaxAge: 3600
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  CoreBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'core-bucket-${AWS::AccountId}-${AWS::Region}'
      AccessControl: Private
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders: ['*']
            AllowedMethods: ['GET', 'HEAD', 'POST', 'PUT', 'DELETE']
            AllowedOrigins: [!Ref CmsDomainName]
            MaxAge: 3600
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # S3 Bucket Policies
  CmsBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref CmsBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              CanonicalUser: !GetAtt CmsOriginAccessIdentity.S3CanonicalUserId
            Action: 's3:GetObject'
            Resource: !Sub '${CmsBucket.Arn}/*'
          - Effect: Allow
            Principal:
              CanonicalUser: !GetAtt CmsOriginAccessIdentity.S3CanonicalUserId
            Action: 's3:ListBucket'
            Resource: !Sub '${CmsBucket.Arn}'

  CoreBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref CoreBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              CanonicalUser: !GetAtt CoreOriginAccessIdentity.S3CanonicalUserId
            Action: 's3:GetObject'
            Resource: !Sub '${CoreBucket.Arn}/*'
          - Effect: Allow
            Principal:
              CanonicalUser: !GetAtt CoreOriginAccessIdentity.S3CanonicalUserId
            Action: 's3:ListBucket'
            Resource: !Sub '${CoreBucket.Arn}'

  # Origin Access Identities
  CmsOriginAccessIdentity:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: 'OAI for CMS website'

  CoreOriginAccessIdentity:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: 'OAI for Core website'

  # Response Headers Policies
  CmsResponseHeadersPolicy:
    Type: AWS::CloudFront::ResponseHeadersPolicy
    Properties:
      ResponseHeadersPolicyConfig:
        Name: 'CMS-CORS-Policy'
        CorsConfig:
          AccessControlAllowOrigins:
            Items: [!Ref CoreDomainName]
            Quantity: 1
          AccessControlAllowHeaders:
            Items: ['Content-Type']
            Quantity: 1
          AccessControlAllowMethods:
            Items: ['GET', 'HEAD', 'OPTIONS']
            Quantity: 3
          AccessControlAllowCredentials: false
          AccessControlMaxAgeSec: 3600
          OriginOverride: true

  CoreResponseHeadersPolicy:
    Type: AWS::CloudFront::ResponseHeadersPolicy
    Properties:
      ResponseHeadersPolicyConfig:
        Name: 'Core-CORS-Policy'
        CorsConfig:
          AccessControlAllowOrigins:
            Items: [!Ref CmsDomainName]
            Quantity: 1
          AccessControlAllowHeaders:
            Items: ['Content-Type', 'Authorization']
            Quantity: 2
          AccessControlAllowMethods:
            Items: ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'DELETE']
            Quantity: 6
          AccessControlAllowCredentials: true
          AccessControlMaxAgeSec: 3600
          OriginOverride: true

  # CloudFront Distributions
  CmsDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Enabled: true
        Comment: 'Distribution for CMS website'
        Aliases: [!Ref CmsDomainName]
        PriceClass: PriceClass_100
        HttpVersion: http2
        DefaultCacheBehavior:
          TargetOriginId: 'S3-CMS-Origin'
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            Items:
              - GET
              - HEAD
              - OPTIONS
            CachedMethods:
              Items:
                - GET
                - HEAD
              Quantity: 2
            Quantity: 3
          CachePolicyId: '658327ea-f89d-4fab-a63d-7e88639e58f6' # Managed-CachingOptimized
          OriginRequestPolicyId: '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf' # Managed-CORS-S3Origin
          ResponseHeadersPolicyId: !Ref CmsResponseHeadersPolicy
          Compress: true
        Origins:
          - Id: 'S3-CMS-Origin'
            DomainName: !GetAtt CmsBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: !Sub 'origin-access-identity/cloudfront/${CmsOriginAccessIdentity}'
        ViewerCertificate:
          AcmCertificateArn: !Ref CertificateArn
          SslSupportMethod: sni-only
          MinimumProtocolVersion: TLSv1.2_2021

  CoreDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Enabled: true
        Comment: 'Distribution for Core website'
        Aliases: [!Ref CoreDomainName]
        PriceClass: PriceClass_100
        HttpVersion: http2
        DefaultCacheBehavior:
          TargetOriginId: 'S3-Core-Origin'
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            Items:
              - GET
              - HEAD
              - OPTIONS
              - POST
              - PUT
              - DELETE
            CachedMethods:
              Items:
                - GET
                - HEAD
              Quantity: 2
            Quantity: 6
          CachePolicyId: '658327ea-f89d-4fab-a63d-7e88639e58f6' # Managed-CachingOptimized
          OriginRequestPolicyId: '88a5eaf4-2fd4-4709-b370-b4c650ea3fcf' # Managed-CORS-S3Origin
          ResponseHeadersPolicyId: !Ref CoreResponseHeadersPolicy
          Compress: true
        Origins:
          - Id: 'S3-Core-Origin'
            DomainName: !GetAtt CoreBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: !Sub 'origin-access-identity/cloudfront/${CoreOriginAccessIdentity}'
        ViewerCertificate:
          AcmCertificateArn: !Ref CertificateArn
          SslSupportMethod: sni-only
          MinimumProtocolVersion: TLSv1.2_2021

Outputs:
  CmsDistributionDomainName:
    Description: 'Domain name of the CMS CloudFront distribution'
    Value: !GetAtt CmsDistribution.DomainName
  CoreDistributionDomainName:
    Description: 'Domain name of the Core CloudFront distribution'
    Value: !GetAtt CoreDistribution.DomainName
  CmsBucketName:
    Description: 'Name of the CMS S3 bucket'
    Value: !Ref CmsBucket
  CoreBucketName:
    Description: 'Name of the Core S3 bucket'
    Value: !Ref CoreBucket
```

## 模板说明

1. **S3 存储桶配置**：
   - 为 CMS 和 Core 分别创建私有 S3 存储桶
   - 配置了 CORS 规则允许跨域访问
   - 启用了默认加密和公共访问阻止

2. **S3 存储桶策略**：
   - 仅允许对应的 CloudFront OAI 访问存储桶内容
   - 限制为仅必要的 GetObject 和 ListBucket 权限

3. **Origin Access Identities (OAI)**：
   - 为每个分布创建独立的 OAI，用于安全访问 S3

4. **响应头策略**：
   - 为每个网站创建自定义 CORS 响应头策略
   - 配置适当的 Access-Control-Allow-* 头

5. **CloudFront 分布**：
   - 每个网站有自己的分布，使用不同的域名
   - 配置了优化的缓存策略和 CORS 源请求策略
   - 启用了 HTTPS 重定向和压缩
   - 使用 ACM 证书进行 SSL/TLS 加密

6. **输出**：
   - 输出分布域名和 S3 存储桶名称供参考

## 部署说明

1. 在部署前，确保您已经：
   - 在 ACM 中创建了包含两个域名的证书
   - 将两个域名指向 CloudFront 分布

2. 部署参数：
   - `CmsDomainName`: CMS 网站域名 (如 cms.example.com)
   - `CoreDomainName`: Core 网站域名 (如 core.example.com)
   - `CertificateArn`: ACM 证书 ARN

3. 部署后，您需要：
   - 将网站内容上传到对应的 S3 存储桶
   - 配置 DNS 记录指向 CloudFront 分布

此模板实现了第一个方案（两个独立分布），解决了跨域问题同时保持了安全性和性能优化。
