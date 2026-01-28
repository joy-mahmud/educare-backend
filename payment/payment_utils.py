from payment.models import PaymentSlip
from .constants import ANNUAL_FEES
def generate_memo_number(year):
    last_slip = (
        PaymentSlip.objects
        .filter(year=year)
        .order_by("-id")
        .first()
    )

    next_number = 1
    if last_slip:
        next_number = int(last_slip.memo_number.split("-")[-1]) + 1

    return f"EDU-{year}-SLP-{str(next_number).zfill(5)}"

def merge_payment_breakdowns(payments):
    merged = {
        "application_fee": 0,
        "admission_fee": 0,
        "registration_fee": 0,
        "tuition_fee": {
            "amount": 0,
            "months": []
        },
        "exam_fee": {
            "first_semester": 0,
            "second_semester": 0
        }
    }

    for payment in payments:
        data = payment.payment_breakdown or {}

        merged["application_fee"] += data.get("application_fee", 0)
        merged["admission_fee"] += data.get("admission_fee", 0)
        merged["registration_fee"] += data.get("registration_fee", 0)

        tuition = data.get("tuition_fee", {})
        merged["tuition_fee"]["amount"] += tuition.get("amount", 0)
        merged["tuition_fee"]["months"].extend(tuition.get("months", []))

        exam = data.get("exam_fee", {})
        merged["exam_fee"]["first_semester"] += exam.get("first_semester", 0)
        merged["exam_fee"]["second_semester"] += exam.get("second_semester", 0)

    merged["tuition_fee"]["months"] = sorted(
        set(merged["tuition_fee"]["months"])
    )
    return merged

# def calculate_total_payable(breakdown):
#     total = 0

#     if breakdown["application_fee"] > 0:
#         total += ANNUAL_FEES["application_fee"]

#     if breakdown["admission_fee"] > 0:
#         total += ANNUAL_FEES["admission_fee"]

#     if breakdown["registration_fee"] > 0:
#         total += ANNUAL_FEES["registration_fee"]

#     total += len(breakdown["tuition_fee"]["months"]) * ANNUAL_FEES["monthly_tuition"]

#     if breakdown["exam_fee"]["first_semester"] > 0:
#         total += ANNUAL_FEES["exam_fee"]["first_semester"]

#     if breakdown["exam_fee"]["second_semester"] > 0:
#         total += ANNUAL_FEES["exam_fee"]["second_semester"]

#     return total

def extract_paid_fees(breakdown):
    response = {}
    # One-time fees
    response["application_fee_paid"] = (
        breakdown["application_fee"]
        if breakdown["application_fee"] > 0 else 0
    )

    response["admission_fee_paid"] = (
        breakdown["admission_fee"]
        if breakdown["admission_fee"] > 0 else 0
    )

    response["registration_fee_paid"] = (
        breakdown["registration_fee"]
        if breakdown["registration_fee"] > 0 else 0
    )

    # Exam fees
    response["exam_fee_paid"] = {
        "first_semester": breakdown["exam_fee"]["first_semester"],
        "second_semester": breakdown["exam_fee"]["second_semester"]
    }

    # Tuition fees
    response["tuition_fee_paid"] = {
        "months": breakdown["tuition_fee"]["months"],
        "total_amount": breakdown["tuition_fee"]["amount"]
    }

    return response