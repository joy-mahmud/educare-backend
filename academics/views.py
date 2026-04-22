from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClassSubject,StudentResult,ExamRoutine
from .serializers import ClassSubjectSerializer,BulkResultCreateSerializer,ResultViewSerializer,StudentExamResultSerializer,ExamRoutineSerializer
from django.db.models import Max, OuterRef, Subquery,Avg,Sum
from students.models import Student
from .utils import calculate_final_gpa,build_subjects_response,gpa_to_grade
class ClassSubjectAPIView(APIView):

    def get(self, request, class_id):

        subjects = ClassSubject.objects.filter(
            academic_class_id=class_id
        ).select_related(
            "subject",
            "group"
        )

        if not subjects.exists():
            return Response(
                {"message": "No subjects found for this class"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ClassSubjectSerializer(subjects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BulkResultCreateAPIView(APIView):

    def post(self, request):
        serializer = BulkResultCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Results created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ViewResultAPIView(APIView):

    def post(self, request):

        class_id = request.data.get("class_id")
        class_subject_id = request.data.get("subject_id")
        exam = request.data.get("exam")
        classSubject = ClassSubject.objects.get(id=class_subject_id)
        subject_id = classSubject.subject_id

        if not class_id or not subject_id or not exam:
            return Response(
                {"error": "class_id, subject_id and exam are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = StudentResult.objects.filter(
            student_subject__class_subject__academic_class_id=class_id,
            student_subject__class_subject__subject_id=subject_id,
            exam=exam
        ).select_related(
            "student_subject__student",
            "student_subject__class_subject__subject",
            "student_subject__class_subject__academic_class"
        )

        serializer = ResultViewSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentExamResultAPIView(APIView):

    def post(self, request):

        student_id = request.data.get("student_id")
        exam = request.data.get("exam")

        if not student_id or not exam:
            return Response(
                {"error": "student_id and exam are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Highest marks per subject
        highest_marks_subquery = StudentResult.objects.filter(
            student_subject__class_subject__subject=OuterRef(
                "student_subject__class_subject__subject"
            ),
            exam=exam
        ).values(
            "student_subject__class_subject__subject"
        ).annotate(
            highest=Max("marks_obtained")
        ).values("highest")[:1]

        results = StudentResult.objects.filter(
            student_subject__student_id=student_id,
            exam=exam
        ).select_related(
            "student_subject__class_subject__subject"
        ).annotate(
            highest_marks=Subquery(highest_marks_subquery)
        )
        final_gpa = calculate_final_gpa(results)
        final_grade = gpa_to_grade(final_gpa)

        serializer = StudentExamResultSerializer(results, many=True)

        subjects_marks = build_subjects_response(results)

        # # Aggregate calculations
        # totals = results.aggregate(
        #     total_obtained_marks=Sum("marks_obtained"),
        #     total_gpa=Avg("gpa")
        # )

        # # Calculate total full marks
        # total_full_marks = sum(
        #     r.student_subject.class_subject.subject.full_marks
        #     for r in results
        # )
        total_obtained_marks = sum(
            item.get("total_marks", sum(p["total_marks"] for p in item.get("parts", [])))
            for item in subjects_marks
        )

        total_full_marks = sum(
            item.get("full_marks", sum(p["full_marks"] for p in item.get("parts", [])))
            for item in subjects_marks
        )

        return Response({
            "student_id": student_id,
            "exam": exam,
            # "total_obtained_marks": totals["total_obtained_marks"],
            "total_obtained_marks": total_obtained_marks,
            "total_full_marks": total_full_marks,
            "final_gpa": final_gpa,
            "final_grade":final_grade,
            "subjects_marks": subjects_marks
        })

class ExamRoutineListAPIView(APIView):

    def get(self, request):

        class_id = request.query_params.get("class_id")
        exam_id = request.query_params.get("exam_id")

        if not class_id or not exam_id:
            return Response(
                {"error": "class_id and exam_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        routines = ExamRoutine.objects.filter(
            exam_id=exam_id,
            class_subject__academic_class_id=class_id
        ).select_related(
            "class_subject__subject",
            "class_subject__academic_class"
        ).order_by("order", "exam_date")

        if not routines.exists():
            return Response(
                {"message": "No routine found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExamRoutineSerializer(routines, many=True)

        return Response({
            "class_id": class_id,
            "exam_id": exam_id,
            "total_subjects": routines.count(),
            "routine": serializer.data
        })

import io
from django.http import FileResponse
from rest_framework.response import Response
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from django.conf import settings

# Register a Unicode font for Bengali support
# Make sure the .ttf file is in your project directory
# pdfmetrics.registerFont(TTFont('Kalpurush', 'path/to/kalpurush.ttf'))
FONT_PATH = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'kalpurush.ttf')

pdfmetrics.registerFont(TTFont('Kalpurush', FONT_PATH))
class GenerateAllStudentAdmitCard(APIView):
    def get(self, request):
        class_id = request.GET.get("class_id")
        exam_id = request.GET.get("exam_id")

        if not class_id or not exam_id:
            return Response({"error": "class_id and exam_id are required"}, status=400)

        students = Student.objects.filter(studentClass_id=class_id)
        routines = ExamRoutine.objects.filter(
            exam_id=exam_id,
            class_subject__academic_class_id=class_id
        ).select_related("class_subject__subject", "exam").order_by("order")

        if not routines.exists():
            return Response({"error": "No routine found"}, status=404)

        buffer = io.BytesIO()
        # Narrow margins to fit the design
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        styles = getSampleStyleSheet()
        
        # Custom Styles
        header_style = ParagraphStyle('HeaderStyle', parent=styles['Title'], fontSize=18, textColor=colors.white)
        bengali_style = ParagraphStyle(
            'BengaliStyle', 
            parent=styles['Normal'], 
            fontSize=14, 
            textColor=colors.white, 
            alignment=1,
            fontName='Kalpurush' # <--- IMPORTANT
        )
        label_style = ParagraphStyle('LabelStyle', parent=styles['Normal'], fontSize=10, leading=14)

        elements = []

        for i, student in enumerate(students):
            # 1. BLUE HEADER BOX
            # Using a Table to create the blue background effect
            header_content = [
                [Paragraph("<b>Our Educational Institute</b>", header_style)],
                [Paragraph("আমাদের শিক্ষা প্রতিষ্ঠান", bengali_style)]
            ]
            header_table = Table(header_content, colWidths=[doc.width])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a368d')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 15),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 20))

            # 2. EXAM INFO & PHOTO ROW
            # Left: Roll box, Center: Title/Admit Card, Right: Photo Box
            roll_box = Table([["Exam Roll:"]], colWidths=[1*inch], rowHeights=[0.4*inch])
            roll_box.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
            
            mid_content = [
                [Paragraph(f"<b>Exam - {routines.first().exam.name}</b>", styles['Heading2'])],
                [Spacer(1, 5)],
                [Table([["Admit Card"]], colWidths=[1*inch], style=[('BOX', (0,0), (-1,-1), 1, colors.black), ('ALIGN', (0,0), (-1,-1), 'CENTER')])]
            ]
            mid_table = Table(mid_content)

            photo_box = Table([[""]], colWidths=[1.2*inch], rowHeights=[1.4*inch])
            photo_box.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black)]))

            top_row = Table([[roll_box, mid_table, photo_box]], colWidths=[1.5*inch, 3*inch, 1.5*inch])
            top_row.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('ALIGN', (1,0), (1,0), 'CENTER')]))
            elements.append(top_row)
            elements.append(Spacer(1, 20))

            # 3. STUDENT BIODATA
            bio_data = [
                [Paragraph(f"<b>Name:</b> {student.studentName}", label_style)],
                [Paragraph(f"<b>Father:</b> {getattr(student, 'fatherName', 'N/A')}", label_style)],
                [Paragraph(f"<b>Mother:</b> {getattr(student, 'motherName', 'N/A')}", label_style)],
                [Paragraph(f"<b>Class:</b> {student.studentClass.name if student.studentClass else ''}", label_style)],
                [Paragraph(f"<b>Gender:</b> {getattr(student, 'gender', 'Male')}", label_style)],
                [Paragraph(f"<b>Mobile:</b> {student.mobile}", label_style)],
            ]
            bio_table = Table(bio_data, colWidths=[doc.width])
            bio_table.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0)]))
            elements.append(bio_table)
            elements.append(Spacer(1, 15))

            # 4. EXAM ROUTINE
            elements.append(Paragraph("<b>Exam Routine</b>", styles['Heading4']))
            elements.append(Spacer(1, 5))
            
            routine_header = ["Date", "Day", "Start Time", "End Time", "Subject", "Marks"]
            routine_rows = [routine_header]
            for r in routines:
                routine_rows.append([
                    r.exam_date.strftime("%Y-%m-%d"),
                    r.exam_date.strftime("%A"),
                    r.start_time.strftime("%H:%M:%S"),
                    r.end_time.strftime("%H:%M:%S"),
                    r.class_subject.subject.name,
                    r.full_marks
                ])

            rt = Table(routine_rows, colWidths=[1*inch, 0.8*inch, 1*inch, 1*inch, 1.5*inch, 0.7*inch])
            rt.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
            ]))
            elements.append(rt)
            elements.append(Spacer(1, 60)) # Space for signatures

            # 5. SIGNATURE SECTION
            sig_data = [[
                Paragraph("<hr/>Student Signature", label_style),
                "",
                Paragraph("<hr/>Principal Signature", label_style)
            ]]
            sig_table = Table(sig_data, colWidths=[2*inch, 2.5*inch, 2*inch])
            sig_table.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'LEFT'), ('ALIGN', (2,0), (2,0), 'RIGHT')]))
            elements.append(sig_table)

            if i != len(students) - 1:
                elements.append(PageBreak())

        doc.build(elements)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="admit_cards.pdf")
    
class GenerateStudentList(APIView):
    def get(self, request):
        class_id = request.GET.get("class_id")
  
        if not class_id:
            return Response({"error": "class_id is required"}, status=400)

        # Optimization: select_related fetches class/group names in one query
        students = Student.objects.filter(
            studentClass_id=class_id
        ).select_related('studentClass', 'group').order_by('rollNo')

        if not students.exists():
            return Response({"error": "No students found"}, status=404)

        # 1. Setup the PDF Buffer and Document
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50
        )
        elements = []
        styles = getSampleStyleSheet()

        # 2. Define Custom Styles
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Title'],
            fontSize=22,
            textColor=colors.HexColor('#1a368d'),
            spaceAfter=10
        )
        
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=1, # Center
            spaceAfter=30,
            textColor=colors.grey
        )

        # 3. Add Header Content
        elements.append(Paragraph("Our Educational Institute", title_style))
        elements.append(Paragraph(f"Official Student List - Class: {students.first().studentClass.name}", subtitle_style))

        # 4. Define Table Data
        # Header Row
        table_data = [["Roll No", "Student Name", "Class", "Group"]]

        # Data Rows
        for student in students:
            table_data.append([
                str(student.rollNo),
                student.studentName,
                student.studentClass.name if student.studentClass else "N/A",
                student.group.name if student.group else "N/A"
            ])

        # 5. Create and Style the Table
        # Widths: Roll (0.7"), Name (2.8"), Class (1.0"), Group (1.0")
        student_table = Table(table_data, colWidths=[0.7*inch, 2.8*inch, 1.0*inch, 1.0*inch])

        student_table.setStyle(TableStyle([
            # Header Styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a368d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            # Body Styling
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # Center Roll Nos
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Left align Names
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),  # Center Class/Group
            
            # Alternating Row Colors (Zebra Stripes)
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
        ]))

        elements.append(student_table)

        # 6. Build the PDF
        doc.build(elements)
        buffer.seek(0)

        return FileResponse(
            buffer, 
            as_attachment=True, 
            filename=f"Student_List_Class_{class_id}.pdf"
        )

