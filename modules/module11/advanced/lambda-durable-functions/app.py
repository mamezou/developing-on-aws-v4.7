"""
Lambda Durable Functions デモ: 注文処理ワークフロー

Step Functions を使わずに、コードファーストでマルチステップワークフローを構築します。
公式 SDK: aws_durable_execution_sdk_python
"""
from aws_durable_execution_sdk_python import (
    DurableContext,
    durable_execution,
    durable_step,
)
from aws_durable_execution_sdk_python.config import Duration


@durable_step
def validate_order(step_context, order_id: str) -> dict:
    """注文データを検証"""
    step_context.logger.info(f"Validating order {order_id}")
    return {"order_id": order_id, "status": "validated"}


@durable_step
def process_payment(step_context, order_id: str, amount: float) -> dict:
    """支払い処理"""
    step_context.logger.info(f"Processing payment for order {order_id}: {amount}")
    return {"order_id": order_id, "status": "paid", "amount": amount}


@durable_step
def confirm_order(step_context, order_id: str) -> dict:
    """注文確定"""
    step_context.logger.info(f"Confirming order {order_id}")
    return {"order_id": order_id, "status": "confirmed"}


@durable_execution
def handler(event: dict, context: DurableContext) -> dict:
    """
    注文処理ワークフロー
    
    - @durable_step: 各ステップでチェックポイント作成
    - context.wait(): 待機中は Lambda 終了（料金ゼロ）
    - 障害時は最後のチェックポイントから再開
    """
    order_id = event.get("order_id", "unknown")
    items = event.get("items", [])
    total = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
    
    # Step 1: 注文検証
    validation_result = context.step(validate_order(order_id))
    context.logger.info(f"Validation complete: {validation_result}")
    
    # Step 2: 支払い処理
    payment_result = context.step(process_payment(order_id, total))
    context.logger.info(f"Payment complete: {payment_result}")
    
    # 外部確認を待機（10秒）- この間 Lambda は終了、料金なし
    context.wait(Duration.from_seconds(10))
    
    # Step 3: 注文確定
    confirmation_result = context.step(confirm_order(order_id))
    context.logger.info(f"Order confirmed: {confirmation_result}")
    
    return {
        "order_id": order_id,
        "status": "completed",
        "total": total,
        "steps": [validation_result, payment_result, confirmation_result]
    }
