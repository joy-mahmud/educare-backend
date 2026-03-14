def calculate_final_gpa(results):
    main_gpas = []
    elective_gpa = None

    for r in results:
        if r.student_subject.role == "MAIN":
            if r.gpa == 0:
                return 0   # fail rule
            main_gpas.append(float(r.gpa))

        elif r.student_subject.role == "ELECTIVE":
            elective_gpa = float(r.gpa)

    base_gpa = sum(main_gpas) / len(main_gpas)

    extra = 0
    if elective_gpa:
        extra = max(0, elective_gpa - 2)

    final_gpa = min(5.0, base_gpa + extra)

    return round(final_gpa, 2)