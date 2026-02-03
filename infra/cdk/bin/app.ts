#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { StudentEnvironmentStack } from '../lib/student-environment-stack';

const app = new cdk.App();

const studentCount = app.node.tryGetContext('studentCount') || 3;
const instanceType = app.node.tryGetContext('instanceType') || 't3.small';

new StudentEnvironmentStack(app, 'StudentEnvironmentStack', {
  studentCount: Number(studentCount),
  instanceType: instanceType,
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'ap-northeast-1',
  },
});
