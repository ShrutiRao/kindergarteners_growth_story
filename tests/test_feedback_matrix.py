import pandas as pd

from src.analytics import mood_feedback_matrix, teacher_feedback_sentiment


def test_teacher_feedback_sentiment_groups_common_feedback_phrases():
    assert teacher_feedback_sentiment("Improved reading") == "positive"
    assert teacher_feedback_sentiment("Strong effort in math") == "positive"
    assert teacher_feedback_sentiment("Great classroom behavior") == "positive"
    assert teacher_feedback_sentiment("Needs support with handwriting") == "needs_support"
    assert teacher_feedback_sentiment("") == "neutral"


def test_mood_feedback_matrix_counts_mood_and_sentiment():
    frame = pd.DataFrame(
        [
            {"mood": "Happy", "teacher_feedback": "Improved reading"},
            {"mood": "Happy", "teacher_feedback": "Needs support with handwriting"},
            {"mood": "Excited", "teacher_feedback": "Great classroom behavior"},
            {"mood": "Focused", "teacher_feedback": ""},
        ]
    )
    matrix = mood_feedback_matrix(frame)
    assert matrix.loc["Happy", "positive"] == 1
    assert matrix.loc["Happy", "needs_support"] == 1
    assert matrix.loc["Excited", "positive"] == 1
    assert matrix.loc["Focused", "neutral"] == 1
