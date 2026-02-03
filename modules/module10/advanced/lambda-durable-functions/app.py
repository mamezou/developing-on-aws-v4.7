"""
Lambda Durable Functions - 注文処理ワークフロー

Step Functions を使わずに、コードファーストでマルチステップワークフローを構築します。
"""

import random
from aws_durable_execution_sdk_python import (
    DurableContext,
    StepContext,
    durable_execution,
    durable_step,
)
from aws_durable_execution_sdk_python.config import (
    Duration,
    StepConfig,
    CallbackConfig,
)
from aws_durable_execution_sdk_python.retries import (
    RetryStrategyConfig,
    create_retry_strategy,
)


@durable_step
def validate_order(step_context: StepContext, order_id: str, items: list) -> dict:
    """注文データを検証"""
    step_context.logger.info(f"Validating order: {order_id}")
    
    # 注文内容の検証
    total = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    
    return {
        "order_id": order_id,
        "total": total,
        "status": "validated"
    }


@durable_step
def check_inventory(step_context: StepContext, items: list) -> dict:
    """在庫確認"""
    step_context.logger.info(f"Checking inventory for {len(items)} items")
    
    # デモ用: 常に在庫あり
    return {
        "available": True,
        "reserved": True
    }


@durable_step
def send_for_approval(step_context: StepContext, callback_id: str, order_id: str, total: int) -> dict:
    """承認リクエストを送信"""
    step_context.logger.info(f"Sending order {order_id} (total: {total}) for approval")
    step_context.logger.info(f"Callback ID: {callback_id}")
    
    # 本番環境: callback_id を外部承認システムに送信
    # 外部システムは SendDurableExecutionCallbackSuccess/Failure API を呼び出す
    
    return {
        "order_id": order_id,
        "callback_id": callback_id,
        "status": "sent_for_approval"
    }


@durable_step
def process_payment(step_context: StepContext, order_id: str, total: int) -> dict:
    """支払い処理（リトライロジック付き）"""
    step_context.logger.info(f"Processing payment for order: {order_id}, amount: {total}")
    
    # デモ用: 40% の確率で失敗（リトライを確認）
    if random.random() > 0.6:
        step_context.logger.info("Payment processing failed, will retry")
        raise Exception("Payment gateway timeout")
    
    import uuid
    return {
        "order_id": order_id,
        "payment_id": f"pay_{uuid.uuid4().hex[:8]}",
        "amount": total,
        "status": "charged"
    }


@durable_step
def send_notification(step_context: StepContext, order_id: str, payment_id: str) -> dict:
    """完了通知の送信"""
    step_context.logger.info(f"Order {order_id} completed. Payment: {payment_id}")
    return {"notified": True}


@durable_execution
def lambda_handler(event: dict, context: DurableContext) -> dict:
    """注文処理ワークフローのメインハンドラー"""
    try:
        import uuid
        order_id = event.get("order_id", str(uuid.uuid4()))
        customer_id = event.get("customer_id", "unknown")
        items = event.get("items", [])
        
        context.logger.info(f"Processing order: {order_id} for customer: {customer_id}")
        
        # Step 1: 注文検証
        validated = context.step(validate_order(order_id, items))
        if validated["status"] != "validated":
            raise Exception("Validation failed")
        context.logger.info(f"Order validated: {validated}")
        
        # Step 2: 在庫確認
        inventory = context.step(check_inventory(items))
        if not inventory["available"]:
            return {
                "status": "failed",
                "reason": "out_of_stock",
                "order_id": order_id
            }
        context.logger.info(f"Inventory checked: {inventory}")
        
        # Step 3: コールバック作成（承認待ち）
        callback = context.create_callback(
            name="awaiting-approval",
            config=CallbackConfig(timeout=Duration.from_minutes(5))
        )
        context.logger.info(f"Created callback with id: {callback.callback_id}")
        
        # Step 4: 承認リクエスト送信
        approval_request = context.step(
            send_for_approval(callback.callback_id, order_id, validated["total"])
        )
        context.logger.info(f"Approval request sent: {approval_request}")
        
        # Step 5: コールバック結果を待機（Lambda は終了、料金なし）
        context.logger.info("Waiting for approval callback...")
        approval_result = callback.result()
        context.logger.info(f"Approval received: {approval_result}")
        
        if not approval_result.get("approved"):
            return {
                "status": "rejected",
                "order_id": order_id
            }
        
        # Step 6: カスタムリトライ戦略で支払い処理
        retry_config = RetryStrategyConfig(max_attempts=3, backoff_rate=2.0)
        payment = context.step(
            process_payment(order_id, validated["total"]),
            config=StepConfig(retry_strategy=create_retry_strategy(retry_config)),
        )
        context.logger.info(f"Payment processed: {payment}")
        
        # Step 7: 完了通知
        context.step(send_notification(order_id, payment["payment_id"]))
        
        return {
            "status": "completed",
            "order_id": order_id,
            "payment_id": payment["payment_id"],
            "amount": payment["amount"]
        }
        
    except Exception as error:
        context.logger.error(f"Error processing order: {error}")
        raise error
