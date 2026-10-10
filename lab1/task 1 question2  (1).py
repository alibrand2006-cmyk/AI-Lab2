def scholarship_decision(score, documents_complete, attendance, interview_score):
    if (
        score >= 70
        and documents_complete
        and attendance >= 75
        and interview_score >= 60
    ):
        return "Review"
    else:
        return "Hold"


cases = [
    ("pass", 80, True, 85, 75, "All four conditions are satisfied."),
    ("attendance_failure", 80, True, 70, 75,
     "Attendance is below the required 75% threshold."),
    ("interview_failure", 80, True, 85, 55,
     "Interview score is below the required 60 threshold."),
    ("threshold_boundary", 70, True, 75, 60,
     "All values are exactly at the minimum thresholds.")
]


for name, score, documents_complete, attendance, interview_score, reason in cases:

    actual = scholarship_decision(
        score,
        documents_complete,
        attendance,
        interview_score
    )

    expected = "Review" if name in ["pass", "threshold_boundary"] else "Hold"

    print(f"Case: {name}")
    print(
        f"Input: score={score}, "
        f"documents_complete={documents_complete}, "
        f"attendance={attendance}, "
        f"interview_score={interview_score}"
    )
    print(f"Expected: {expected}")
    print(f"Actual: {actual}")
    print(f"Reason: {reason}")
    print("-" * 60)