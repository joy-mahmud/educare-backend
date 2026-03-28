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
            print("group subject gpa:",current_gp)

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