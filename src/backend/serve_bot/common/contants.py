from enum import Enum


class Intent(Enum):
    """意图枚举类"""
    ORDER_INQUIRY = "order_inquiry"  # 订单查询：用户想查询订单状态、查看下单记录等
    LOGISTICS_TRACKING = "logistics_tracking"  # 物流跟踪：用户想查询包裹物流进度、快递信息等
    AFTER_SALE = "after_sale"  # 售后申请：用户想申请退货、退款、维修等
    COMPLAINT_FEEDBACK = "complaint_feedback"  # 投诉与反馈：用户想进行投诉、建议或其他服务意见
    PAYMENT_INVOICE = "payment_invoice"  # 支付与发票：用户咨询支付方式、发票申请或报销事宜
    FAQ = "faq"  # FAQ常见问题：用户询问常见流程、政策、规则类问题，例如运费规则、优惠券使用、会员积分等
    OUT_OF_SCOPE = "out_of_scope"  # 业务外或无关：用户提出与电商客服完全无关的问题，或无法匹配在上述意图中的任何一类
    UNCLEAR = "unclear"  # 不确定：用户意图不明确，需要进一步澄清
