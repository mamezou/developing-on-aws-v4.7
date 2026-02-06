import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import * as crypto from 'crypto';

export interface StudentEnvironmentStackProps extends cdk.StackProps {
  studentCount: number;
  instanceType: string;
}

export class StudentEnvironmentStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: StudentEnvironmentStackProps) {
    super(scope, id, props);

    const accountId = cdk.Stack.of(this).account;
    const region = cdk.Stack.of(this).region;

    // ===========================================
    // Phase 1: Permissions Boundary
    // ===========================================
    const permissionsBoundary = new iam.ManagedPolicy(this, 'StudentPermissionsBoundary', {
      managedPolicyName: 'StudentPermissionsBoundary',
      description: 'Permissions boundary for student IAM users and roles',
      statements: [
        // S3: 自分のプレフィックスのみ
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['s3:*'],
          resources: [
            'arn:aws:s3:::*instructor*',
            'arn:aws:s3:::*student*',
            'arn:aws:s3:::*instructor*/*',
            'arn:aws:s3:::*student*/*',
            // SAM managed bucket
            'arn:aws:s3:::aws-sam-cli-managed-default-*',
            'arn:aws:s3:::aws-sam-cli-managed-default-*/*',
          ],
        }),
        // S3: バケット一覧は許可（デモで必要）
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['s3:ListAllMyBuckets', 's3:GetBucketLocation'],
          resources: ['*'],
        }),
        // DynamoDB: 自分のプレフィックスのみ
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['dynamodb:*'],
          resources: [
            `arn:aws:dynamodb:${region}:${accountId}:table/*instructor*`,
            `arn:aws:dynamodb:${region}:${accountId}:table/*student*`,
            `arn:aws:dynamodb:${region}:${accountId}:table/*instructor*/index/*`,
            `arn:aws:dynamodb:${region}:${accountId}:table/*student*/index/*`,
          ],
        }),
        // DynamoDB: テーブル一覧は許可
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['dynamodb:ListTables', 'dynamodb:DescribeLimits'],
          resources: ['*'],
        }),
        // Lambda: 自分のプレフィックスのみ
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['lambda:*'],
          resources: [
            `arn:aws:lambda:${region}:${accountId}:function:*instructor*`,
            `arn:aws:lambda:${region}:${accountId}:function:*student*`,
            `arn:aws:lambda:${region}:${accountId}:layer:*`,
          ],
        }),
        // Lambda: 一覧は許可
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['lambda:ListFunctions', 'lambda:ListLayers', 'lambda:GetAccountSettings'],
          resources: ['*'],
        }),
        // API Gateway: 全て許可（リソースベースの制限が難しい）
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['apigateway:*'],
          resources: ['*'],
        }),
        // Step Functions: 自分のプレフィックスのみ
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['states:*'],
          resources: [
            `arn:aws:states:${region}:${accountId}:stateMachine:*instructor*`,
            `arn:aws:states:${region}:${accountId}:stateMachine:*student*`,
            `arn:aws:states:${region}:${accountId}:execution:*instructor*:*`,
            `arn:aws:states:${region}:${accountId}:execution:*student*:*`,
          ],
        }),
        // Step Functions: 一覧は許可
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['states:ListStateMachines'],
          resources: ['*'],
        }),
        // Cognito: 全て許可（Module 12 で必要）
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['cognito-idp:*', 'cognito-identity:*'],
          resources: ['*'],
        }),
        // CloudWatch Logs & Metrics
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['logs:*', 'cloudwatch:*'],
          resources: ['*'],
        }),
        // X-Ray
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['xray:*'],
          resources: ['*'],
        }),
        // CloudFormation: 自分のプレフィックスのみ（SAM 用）
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['cloudformation:*'],
          resources: [
            `arn:aws:cloudformation:${region}:${accountId}:stack/*instructor*/*`,
            `arn:aws:cloudformation:${region}:${accountId}:stack/*student*/*`,
            `arn:aws:cloudformation:${region}:${accountId}:stack/aws-sam-cli-managed-default/*`,
          ],
        }),
        // CloudFormation: 一覧・変換は許可
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: [
            'cloudformation:ListStacks',
            'cloudformation:GetTemplateSummary',
            'cloudformation:ValidateTemplate',
            'cloudformation:CreateChangeSet',
          ],
          resources: ['*'],
        }),
        // IAM: ロール作成（Permissions Boundary 必須）
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: [
            'iam:CreateRole',
            'iam:DeleteRole',
            'iam:AttachRolePolicy',
            'iam:DetachRolePolicy',
            'iam:PutRolePolicy',
            'iam:DeleteRolePolicy',
            'iam:GetRole',
            'iam:GetRolePolicy',
            'iam:ListRolePolicies',
            'iam:ListAttachedRolePolicies',
            'iam:TagRole',
            'iam:UntagRole',
            'iam:UpdateAssumeRolePolicy',
          ],
          resources: [
            `arn:aws:iam::${accountId}:role/*instructor*`,
            `arn:aws:iam::${accountId}:role/*student*`,
          ],
        }),
        // IAM: PassRole
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['iam:PassRole'],
          resources: [
            `arn:aws:iam::${accountId}:role/*instructor*`,
            `arn:aws:iam::${accountId}:role/*student*`,
          ],
        }),
        // IAM: 一覧・読み取りは許可
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: [
            'iam:ListRoles',
            'iam:ListPolicies',
            'iam:GetPolicy',
            'iam:GetPolicyVersion',
            'iam:CreateServiceLinkedRole',
          ],
          resources: ['*'],
        }),
        // STS
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: ['sts:GetCallerIdentity'],
          resources: ['*'],
        }),
        // EC2: Waiter デモ用（制限付き）
        new iam.PolicyStatement({
          effect: iam.Effect.ALLOW,
          actions: [
            'ec2:RunInstances',
            'ec2:DescribeInstances',
            'ec2:TerminateInstances',
            'ec2:CreateTags',
            'ec2:DescribeImages',
            'ec2:DescribeSecurityGroups',
            'ec2:DescribeSubnets',
            'ec2:DescribeVpcs',
          ],
          resources: ['*'],
        }),
      ],
    });

    // ===========================================
    // 専用 VPC を作成
    // ===========================================
    const vpc = new ec2.Vpc(this, 'TrainingVpc', {
      vpcName: 'developing-on-aws-training',
      maxAzs: 2,
      natGateways: 0,  // コスト削減のため NAT Gateway なし
      subnetConfiguration: [
        {
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
      ],
    });

    // Security Group
    const securityGroup = new ec2.SecurityGroup(this, 'StudentSG', {
      vpc,
      description: 'Security group for student Code Server instances',
      allowAllOutbound: true,
    });

    // Code Server 用ポート (8443)
    securityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(8443),
      'Allow Code Server access'
    );

    // SSH (デバッグ用)
    securityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(22),
      'Allow SSH access'
    );

    // ===========================================
    // IAM Role for EC2 (training labs)
    // ===========================================
    const labRole = new iam.Role(this, 'TrainingLabRole', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'),
      ],
      permissionsBoundary: permissionsBoundary,
    });

    // EC2 ロールに Permissions Boundary 内の権限を付与
    labRole.addToPolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        // S3
        's3:*',
        // DynamoDB
        'dynamodb:*',
        // Lambda
        'lambda:*',
        // EC2 (for Waiter demo)
        'ec2:RunInstances',
        'ec2:DescribeInstances',
        'ec2:TerminateInstances',
        'ec2:CreateTags',
        'ec2:DescribeImages',
        'ec2:DescribeSecurityGroups',
        'ec2:DescribeSubnets',
        'ec2:DescribeVpcs',
        // CloudWatch Logs & Metrics
        'logs:*',
        'cloudwatch:*',
        // IAM (for Lambda role creation in demos and SAM)
        'iam:CreateRole',
        'iam:DeleteRole',
        'iam:AttachRolePolicy',
        'iam:DetachRolePolicy',
        'iam:PutRolePolicy',
        'iam:DeleteRolePolicy',
        'iam:PassRole',
        'iam:GetRole',
        'iam:GetRolePolicy',
        'iam:ListRoles',
        'iam:ListRolePolicies',
        'iam:ListAttachedRolePolicies',
        'iam:ListPolicies',
        'iam:GetPolicy',
        'iam:GetPolicyVersion',
        'iam:TagRole',
        'iam:UntagRole',
        'iam:CreateServiceLinkedRole',
        'iam:UpdateAssumeRolePolicy',
        // Step Functions
        'states:*',
        // STS (for config.py)
        'sts:GetCallerIdentity',
        // API Gateway
        'apigateway:*',
        // X-Ray
        'xray:*',
        // Cognito (Module 12)
        'cognito-idp:*',
        'cognito-identity:*',
        // CloudFormation (for SAM deploy)
        'cloudformation:*',
      ],
      resources: ['*'],
    }));

    // Amazon Linux 2023 AMI
    const ami = ec2.MachineImage.latestAmazonLinux2023({
      cpuType: ec2.AmazonLinuxCpuType.X86_64,
    });

    // Create instances for each student
    const students = ['instructor', ...Array.from({ length: props.studentCount }, (_, i) => `student-${i + 1}`)];

    // ===========================================
    // マネジメントコンソールログイン URL
    // ===========================================
    new cdk.CfnOutput(this, 'ConsoleLoginURL', {
      value: `https://${accountId}.signin.aws.amazon.com/console`,
      description: 'AWS Management Console login URL',
    });

    for (const studentId of students) {
      // Generate random passwords
      const codeServerPassword = crypto.randomBytes(8).toString('hex');
      const consolePassword = crypto.randomBytes(12).toString('hex') + 'Aa1!'; // 複雑性要件を満たす

      // ===========================================
      // Phase 2: IAM ユーザー作成（マネコン用）
      // ===========================================
      const iamUserName = studentId.replace('-', ''); // student-1 -> student1
      const iamUser = new iam.User(this, `User-${studentId}`, {
        userName: iamUserName,
        password: cdk.SecretValue.unsafePlainText(consolePassword),
        passwordResetRequired: false,
        permissionsBoundary: permissionsBoundary,
      });

      // IAM ユーザーに権限を付与（Permissions Boundary 内で動作）
      iamUser.addToPolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          // S3
          's3:*',
          // DynamoDB
          'dynamodb:*',
          // Lambda
          'lambda:*',
          // CloudWatch Logs & Metrics
          'logs:*',
          'cloudwatch:*',
          // Step Functions
          'states:*',
          // API Gateway
          'apigateway:*',
          // X-Ray
          'xray:*',
          // Cognito
          'cognito-idp:*',
          'cognito-identity:*',
          // CloudFormation
          'cloudformation:*',
          // IAM (読み取り中心)
          'iam:GetRole',
          'iam:GetRolePolicy',
          'iam:ListRoles',
          'iam:ListRolePolicies',
          'iam:ListAttachedRolePolicies',
          'iam:ListPolicies',
          'iam:GetPolicy',
          'iam:GetPolicyVersion',
          // STS
          'sts:GetCallerIdentity',
        ],
        resources: ['*'],
      }));

      // User Data script - using raw script to avoid cloud-init issues
      const userData = ec2.UserData.forLinux();
      userData.addCommands(
        '#!/bin/bash',
        '# Disable strict mode that cloud-init enables',
        'set +u',
        'set +e',
        '',
        '# Logging',
        'exec > >(tee /var/log/user-data.log) 2>&1',
        'echo "Starting user data script at $(date)"',
        '',
        '# Set HOME explicitly',
        'export HOME=/root',
        '',
        '# System update',
        'echo "Updating system..."',
        'dnf update -y',
        '',
        '# Install Python and tools',
        'echo "Installing Python and tools..."',
        'dnf install -y python3 python3-pip git',
        'pip3 install boto3',
        '',
        '# Install AWS CLI v2',
        'echo "Installing AWS CLI v2..."',
        'curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"',
        'unzip -q awscliv2.zip',
        './aws/install',
        'rm -rf aws awscliv2.zip',
        '',
        '# Set environment variables',
        `echo 'export STUDENT_ID=${studentId}' >> /etc/profile.d/student.sh`,
        `echo 'export AWS_DEFAULT_REGION=ap-northeast-1' >> /etc/profile.d/student.sh`,
        'chmod +x /etc/profile.d/student.sh',
        '',
        '# Install Code Server',
        'echo "Installing Code Server..."',
        'HOME=/root curl -fsSL https://code-server.dev/install.sh | HOME=/root sh',
        '',
        '# Configure Code Server',
        'echo "Configuring Code Server..."',
        'mkdir -p /home/ec2-user/.config/code-server',
        `cat > /home/ec2-user/.config/code-server/config.yaml << CODESERVEREOF`,
        'bind-addr: 0.0.0.0:8443',
        'auth: password',
        `password: ${codeServerPassword}`,
        'cert: false',
        'CODESERVEREOF',
        '',
        '# Clone training repository',
        'echo "Cloning training repository..."',
        'git clone https://github.com/mamezou/developing-on-aws-v4.7.git /home/ec2-user/developing-on-aws-v4.7 || echo "Repository clone failed or already exists"',
        '',
        '# Configure git safe.directory for ec2-user',
        'sudo -u ec2-user git config --global --add safe.directory /home/ec2-user/developing-on-aws-v4.7',
        '',
        '# Set ec2-user home directory to the project',
        'usermod -d /home/ec2-user/developing-on-aws-v4.7 ec2-user',
        '',
        '# Set ownership',
        'chown -R ec2-user:ec2-user /home/ec2-user',
        '',
        '# Install Python extension for Code Server',
        'echo "Installing VS Code extensions..."',
        'sudo -u ec2-user HOME=/home/ec2-user code-server --install-extension ms-python.python || echo "Extension install failed"',
        '',
        '# Create systemd service',
        'echo "Creating systemd service..."',
        `cat > /etc/systemd/system/code-server.service << SERVICEEOF`,
        '[Unit]',
        'Description=Code Server',
        'After=network.target',
        '',
        '[Service]',
        'Type=simple',
        'User=ec2-user',
        'WorkingDirectory=/home/ec2-user/developing-on-aws-v4.7',
        `Environment=STUDENT_ID=${studentId}`,
        'Environment=AWS_DEFAULT_REGION=ap-northeast-1',
        'Environment=HOME=/home/ec2-user/developing-on-aws-v4.7',
        'ExecStart=/usr/bin/code-server --config /home/ec2-user/.config/code-server/config.yaml /home/ec2-user/developing-on-aws-v4.7',
        'Restart=always',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
        'SERVICEEOF',
        '',
        '# Start Code Server',
        'echo "Starting Code Server..."',
        'systemctl daemon-reload',
        'systemctl enable code-server',
        'systemctl start code-server',
        '',
        'echo "User data script completed successfully at $(date)"',
      );

      // EC2 Instance
      const instance = new ec2.Instance(this, `Instance-${studentId}`, {
        vpc,
        instanceType: new ec2.InstanceType(props.instanceType),
        machineImage: ami,
        securityGroup,
        role: labRole,
        userData,
        vpcSubnets: {
          subnetType: ec2.SubnetType.PUBLIC,
        },
      });

      // Outputs - Code Server
      new cdk.CfnOutput(this, `${studentId}-CodeServerURL`, {
        value: `http://${instance.instancePublicDnsName}:8443`,
        description: `Code Server URL for ${studentId}`,
      });

      new cdk.CfnOutput(this, `${studentId}-CodeServerPassword`, {
        value: codeServerPassword,
        description: `Code Server password for ${studentId}`,
      });

      // Outputs - Management Console
      new cdk.CfnOutput(this, `${studentId}-ConsoleUser`, {
        value: iamUserName,
        description: `Console username for ${studentId}`,
      });

      new cdk.CfnOutput(this, `${studentId}-ConsolePassword`, {
        value: consolePassword,
        description: `Console password for ${studentId}`,
      });
    }
  }
}
