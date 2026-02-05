"""
Cognito オーソライザーで保護された API のバックエンド
"""
import json


def handler(event, context):
    # Cognito オーソライザーが検証済みのユーザー情報を取得
    claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'Access granted to protected resource',
            'user': {
                'sub': claims.get('sub'),
                'email': claims.get('email'),
                'username': claims.get('cognito:username')
            }
        })
    }
