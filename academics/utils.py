def calculate_final_gpa(results):
    main_gp_sum = 0
    main_subject_count = 0
    elective_gp = 0

    for r in results:
        # Convert GP to float for safety
        current_gp = float(r.gpa)
        
        if r.student_subject.role == "MAIN":
            if current_gp == 0:
                return 0.00  # Fail rule: Any F in a MAIN subject = Total GPA 0
            
            main_gp_sum += current_gp
            main_subject_count += 1

        elif r.student_subject.role == "ELECTIVE":
            elective_gp = current_gp

    # 1. Calculate Bonus Points (Points above 2.0)
    bonus_points = max(0, elective_gp - 2)

    # 2. Add bonus to the MAIN sum, then divide by the number of MAIN subjects
    if main_subject_count == 0:
        return 0.00
        
    final_result = (main_gp_sum + bonus_points) / main_subject_count

    # 3. Cap at 5.00 and round
    final_gpa = min(5.00, final_result)
    
    return round(final_gpa, 2)