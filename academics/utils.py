# def calculate_final_gpa(results):
#     main_gp_sum = 0
#     main_subject_count = 0
#     elective_gp = 0
#     bonus_points = 0

#     for r in results:
#         # Convert GP to float for safety
#         current_gp = float(r.gpa)
        
#         if r.student_subject.role == "MAIN":
#             if current_gp == 0:
#                 return 0.00  # Fail rule: Any F in a MAIN subject = Total GPA 0
            
#             main_gp_sum += current_gp
#             main_subject_count += 1

#         elif r.student_subject.role == "ELECTIVE":
#             elective_gp = current_gp

#     # 1. Calculate Bonus Points (Points above 2.0)
#     if(elective_gp==5):
#         bonus_points+=3
#     elif(elective_gp==4):
#         bonus_points+=2
#     elif(elective_gp==3.5):
#         bonus_points+=1


#     # 2. Add bonus to the MAIN sum, then divide by the number of MAIN subjects
#     if main_subject_count == 0:
#         return 0.00
        
#     final_result = (main_gp_sum + bonus_points) / main_subject_count

#     # 3. Cap at 5.00 and round
#     final_gpa = min(5.00, final_result)
    
#     return round(final_gpa, 2)
from collections import defaultdict

def calculate_final_gpa(results):

    subject_groups = defaultdict(list)

    # Step 1: Group subjects
    for r in results:
        subject = r.student_subject.class_subject.subject
        final_subject = subject.parent_subject or subject
        subject_groups[final_subject].append(r)

    main_gp_sum = 0
    main_subject_count = 0
    elective_gp = 0
    bonus_points = 0

    # Step 2: Process each subject group

    for subject, group_results in subject_groups.items():

        role = group_results[0].student_subject.role

        # If subject has multiple parts → combine
        if len(group_results) > 1:
            total_marks = sum(float(r.marks_obtained) for r in group_results)
            avg_marks = total_marks / len(group_results)

            current_gp = marks_to_gpa(avg_marks)

        else:
            current_gp = float(group_results[0].gpa)

        # Step 3: Apply your original logic
        if role == "MAIN":

            if current_gp == 0:
                return 0.00

            main_gp_sum += current_gp
            main_subject_count += 1

        elif role == "ELECTIVE":
            elective_gp = current_gp

    # Step 4: Your existing bonus logic
    if elective_gp == 5:
        bonus_points += 3
    elif elective_gp == 4:
        bonus_points += 2
    elif elective_gp == 3.5:
        bonus_points += 1

    if main_subject_count == 0:
        return 0.00
    final_result = (main_gp_sum + bonus_points) / main_subject_count

    final_gpa = min(5.00, final_result)

    return round(final_gpa, 2)

def marks_to_gpa(marks):
    if marks >= 80:
        return 5.0
    elif marks >= 70:
        return 4.0
    elif marks >= 60:
        return 3.5
    elif marks >= 50:
        return 3.0
    elif marks >= 40:
        return 2.0
    elif marks >= 33:
        return 1.0
    else:
        return 0.0

def marks_to_grade(marks):
    if marks >= 80:
        return "A+"
    elif marks >= 70:
        return "A"
    elif marks >= 60:
        return "A-"
    elif marks >= 50:
        return "B"
    elif marks >= 40:
        return "C"
    elif marks >= 33:
        return "D"
    else:
        return "F"

def gpa_to_grade(gpa):
    if gpa >= 5.0:
        return "A+"
    elif gpa >= 4.0:
        return "A"
    elif gpa >= 3.5:
        return "A-"
    elif gpa >= 3.0:
        return "B"
    elif gpa >= 2.0:
        return "C"
    elif gpa >= 1.0:
        return "D"
    else:
        return "F"


def build_subjects_response(results):
    subject_groups = defaultdict(list)

    # Step 1: Group subjects (Bangla 1st + 2nd → Bangla)
    for r in results:
        subject = r.student_subject.class_subject.subject
        final_subject = subject.parent_subject or subject
        subject_groups[final_subject].append(r)
        

    processed_subjects = []
    print(subject_groups)
    # Step 2: Process each group
    for subject, items in subject_groups.items():

        role = items[0].student_subject.role
        class_subject_order = items[0].student_subject.class_subject.order
        is_optional = role == "ELECTIVE"

        # MULTI-PART SUBJECT (Bangla / English)
        if len(items) > 1:

            total_marks = sum(float(r.marks_obtained) for r in items)
            avg_marks = total_marks / len(items)

            combined_gpa = marks_to_gpa(avg_marks)
            combined_grade = marks_to_grade(avg_marks)

            parts = []

            for r in items:
                parts.append({
                    "subject_name": r.student_subject.class_subject.subject.name,
                    "full_marks": r.student_subject.class_subject.subject.full_marks,
                    "highest_marks": float(r.highest_marks),
                    "obtaining_marks": {
                        "cq": float(r.marks_cq) if r.marks_cq else None,
                        "mcq": float(r.marks_mcq) if r.marks_mcq else None,
                        "ca": None,
                        "prc": None,
                    },
                    "total_marks": float(r.marks_obtained)
                })

            processed_subjects.append({
                "subject_group_name": subject.name,
                "combined_letter_grade": combined_grade,
                "combined_grade_point": combined_gpa,
                "parts": parts,
                "is_optional": is_optional,
                "optional_tag": "Optional" if is_optional else None,
                "role": role,
                "order": class_subject_order
            })

        # SINGLE SUBJECT
        else:
            r = items[0]

            processed_subjects.append({
                "subject_name": subject.name,
                "full_marks": subject.full_marks,
                "highest_marks": float(r.highest_marks),
                "obtaining_marks": {
                    "cq": float(r.marks_cq) if r.marks_cq else None,
                    "mcq": float(r.marks_mcq) if r.marks_mcq else None,
                    "ca": None,
                    "prc": None,
                },
                "total_marks": float(r.marks_obtained),
                "letter_grade": r.grade,
                "grade_point": float(r.gpa) if r.gpa else None,
                "is_optional": is_optional,
                "optional_tag": "Optional" if is_optional else None,
                "role": role,
                "order": class_subject_order
            })

    # Step 3: Sort by order
    processed_subjects.sort(key=lambda x: x["order"] if x["order"] is not None else 999)

    # Step 4: Move elective subjects to last
    main_subjects = []
    elective_subjects = []

    for item in processed_subjects:
        if item["role"] == "ELECTIVE":
            elective_subjects.append(item)
        else:
            main_subjects.append(item)

    final_subjects = main_subjects + elective_subjects

    # Step 5: Remove helper fields
    for item in final_subjects:
        item.pop("order", None)
        item.pop("role", None)

    return final_subjects