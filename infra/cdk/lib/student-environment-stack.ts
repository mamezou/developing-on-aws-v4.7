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

    // 専用 VPC を作成
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

    // IAM Role for training labs
    const labRole = new iam.Role(this, 'TrainingLabRole', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'),
      ],
    });

    // Training lab permissions
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
        // CloudWatch Logs
        'logs:*',
        // IAM (PassRole for Lambda)
        'iam:PassRole',
        'iam:GetRole',
        // Step Functions
        'states:*',
        // STS (for config.py)
        'sts:GetCallerIdentity',
        // API Gateway
        'apigateway:*',
        // X-Ray
        'xray:*',
      ],
      resources: ['*'],
    }));

    // Amazon Linux 2023 AMI
    const ami = ec2.MachineImage.latestAmazonLinux2023({
      cpuType: ec2.AmazonLinuxCpuType.X86_64,
    });

    // Create instances for each student
    const students = ['instructor', ...Array.from({ length: props.studentCount }, (_, i) => `student-${i + 1}`)];

    for (const studentId of students) {
      // Generate random password
      const password = crypto.randomBytes(8).toString('hex');

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
        `password: ${password}`,
        'cert: false',
        'CODESERVEREOF',
        '',
        '# Clone training repository',
        'echo "Cloning training repository..."',
        'git clone https://github.com/mamezou/developing-on-aws-v4.7.git /home/ec2-user/developing-on-aws-v4.7 || echo "Repository clone failed or already exists"',
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
        `Environment=STUDENT_ID=${studentId}`,
        'Environment=AWS_DEFAULT_REGION=ap-northeast-1',
        'Environment=HOME=/home/ec2-user',
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

      // Outputs
      new cdk.CfnOutput(this, `${studentId}-URL`, {
        value: `http://${instance.instancePublicDnsName}:8443`,
        description: `Code Server URL for ${studentId}`,
      });

      new cdk.CfnOutput(this, `${studentId}-Password`, {
        value: password,
        description: `Password for ${studentId}`,
      });
    }
  }
}
