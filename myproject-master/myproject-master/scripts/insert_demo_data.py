# scripts/insert_demo_data.py
from django.utils import timezone
from myapp.models import Employee, Questionnaire, DailyReport, QuestionnaireThreshold, DailyReportAnswer, QuestionnaireOption

def run():

    # 既存のデータを削除
    Employee.objects.all().delete()
    Questionnaire.objects.all().delete()
    DailyReport.objects.all().delete()
    QuestionnaireThreshold.objects.all().delete()
    DailyReportAnswer.objects.all().delete()
    QuestionnaireOption.objects.all().delete()

    # 従業員データを作成
    employees = [
        {"name": "John Doe", "employee_type": "admin"},
        {"name": "Jane Smith", "employee_type": "general"},
        {"name": "Michael Johnson", "employee_type": "general"},
    ]
    for emp_data in employees:
        employee, created = Employee.objects.get_or_create(**emp_data)
        print(f'Employee created: {employee.name} (ID: {employee.id})')

    # アンケートデータを作成
    questionnaires = [
        {"title": "就寝時間", "type": "morning", "answer_type": "時間選択"},
        {"title": "起床時間", "type": "morning", "answer_type": "時間選択"},
        {"title": "睡眠の質", "type": "morning", "answer_type": "選択"},
        {"title": "今朝の朝食を食べたか", "type": "morning", "answer_type": "選択"},
        {"title": "薬を飲んだ時間", "type": "morning", "answer_type": "時間選択"},
        {"title": "自分の状態", "type": "morning", "answer_type": "選択"},
        {"title": "自分の状態の詳細（自由記述）", "type": "morning", "answer_type": "記述"},
        {"title": "不安感のレベル", "type": "morning", "answer_type": "選択"},
        {"title": "今の感情", "type": "morning", "answer_type": "選択"},
        {"title": "コミュニケーションの意欲", "type": "morning", "answer_type": "選択"},
        {"title": "体の調子", "type": "morning", "answer_type": "選択"},
        {"title": "集中力の調子", "type": "morning", "answer_type": "選択"},
        {"title": "体の不調", "type": "morning", "answer_type": "選択"},
        {"title": "自己肯定感", "type": "morning", "answer_type": "選択"},
        {"title": "誰かに頼っても良いか", "type": "morning", "answer_type": "選択"},
        {"title": "自分が必要とされているか", "type": "morning", "answer_type": "選択"},
        {"title": "その他の気になる症状", "type": "morning", "answer_type": "選択"},
        {"title": "仕事に対して配慮が必要か", "type": "morning", "answer_type": "選択"},
        {"title": "仕事に対して配慮が必要かの詳細", "type": "morning", "answer_type": "記述"},
        {"title": "伝えたいこと", "type": "morning", "answer_type": "記述"},
        {"title": "回復ルーティン", "type": "morning", "answer_type": "記述"},
        {"title": "自身の余裕度", "type": "morning", "answer_type": "選択"},
    ]
    for q_data in questionnaires:
        questionnaire, created = Questionnaire.objects.get_or_create(**q_data)
        print(f'Questionnaire created: {questionnaire.title} (ID: {questionnaire.id})')

    # デイリーレポートデータを作成
    daily_reports = [
        {"employee_id": 1, "report_datetime": timezone.now(), "report_type": "morning"},
        {"employee_id": 2, "report_datetime": timezone.now(), "report_type": "morning"},
        {"employee_id": 3, "report_datetime": timezone.now(), "report_type": "evening"},
    ]
    for report_data in daily_reports:
        report, created = DailyReport.objects.get_or_create(**report_data)
        print(f'Daily Report created: ID {report.id}')

    # 質問の閾値データを作成
    thresholds = [
        {"employee_id": 1, "questionnaire_id": 3, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 4, "threshold_min": 0, "threshold_max": 1},
        {"employee_id": 1, "questionnaire_id": 6, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 8, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 9, "threshold_min": 0, "threshold_max": 1},
        {"employee_id": 1, "questionnaire_id": 10, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 11, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 12, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 13, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 14, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 15, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 16, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 17, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 18, "threshold_min": 0, "threshold_max": 3},
        {"employee_id": 1, "questionnaire_id": 22, "threshold_min": 0, "threshold_max": 3},

    ]
    for threshold_data in thresholds:
        threshold, created = QuestionnaireThreshold.objects.get_or_create(**threshold_data)
        print(f'Threshold created: ID {threshold.id}')

    # デイリーレポート回答データを作成
    answers = [
        {"daily_report_id": 1, "questionnaire_id": 1, "answer": "22:30", "threshold_value": 3},  # 就寝時間（時間選択）
        {"daily_report_id": 1, "questionnaire_id": 2, "answer": "07:00", "threshold_value": 3},  # 起床時間（時間選択）
        {"daily_report_id": 1, "questionnaire_id": 3, "answer": 1, "threshold_value": 3},  # 睡眠の質（選択）
        {"daily_report_id": 1, "questionnaire_id": 4, "answer": 2, "threshold_value": 3},  # 今朝の朝食を食べたか（選択）
        {"daily_report_id": 1, "questionnaire_id": 5, "answer": "08:00", "threshold_value": 3},  # 薬を飲んだ時間（時間選択）
        {"daily_report_id": 1, "questionnaire_id": 6, "answer": 4, "threshold_value": 3},  # 自分の状態（選択）
        {"daily_report_id": 1, "questionnaire_id": 7, "answer": "体調は安定しているが、少し疲れを感じる。", "threshold_value": 5},  # 自分の状態の詳細（記述）
        {"daily_report_id": 1, "questionnaire_id": 8, "answer": 3, "threshold_value": 3},  # 不安感のレベル（選択）
        {"daily_report_id": 1, "questionnaire_id": 9, "answer": 1, "threshold_value": 3},  # 今の感情（選択）
        {"daily_report_id": 1, "questionnaire_id": 10, "answer": 4, "threshold_value": 3},  # コミュニケーションの意欲（選択）
        {"daily_report_id": 1, "questionnaire_id": 11, "answer": 3, "threshold_value": 3},  # 体の調子（選択）
        {"daily_report_id": 1, "questionnaire_id": 12, "answer": 3, "threshold_value": 3},  # 集中力の調子（選択）
        {"daily_report_id": 1, "questionnaire_id": 13, "answer": 2, "threshold_value": 3},  # 体の不調（選択）
        {"daily_report_id": 1, "questionnaire_id": 14, "answer": 3, "threshold_value": 3},  # 自己肯定感（選択）
        {"daily_report_id": 1, "questionnaire_id": 15, "answer": 1, "threshold_value": 3},  # 誰かに頼っても良いか（選択）
        {"daily_report_id": 1, "questionnaire_id": 16, "answer": 2, "threshold_value": 3},  # 自分が必要とされているか（選択）
        {"daily_report_id": 1, "questionnaire_id": 17, "answer": 3, "threshold_value": 3},  # その他の気になる症状（選択）
        {"daily_report_id": 1, "questionnaire_id": 18, "answer": 2, "threshold_value": 3},  # 仕事に対して配慮が必要か（選択）
        {"daily_report_id": 1, "questionnaire_id": 19, "answer": "仕事の調整が必要です。", "threshold_value": 5},  # 仕事に対して配慮が必要かの詳細（記述）
        {"daily_report_id": 1, "questionnaire_id": 20, "answer": "特に伝えたいことはありません。", "threshold_value": 5},  # 伝えたいこと（記述）
        {"daily_report_id": 1, "questionnaire_id": 21, "answer": "深呼吸とストレッチを行った。", "threshold_value": 5},  # 回復ルーティン（記述）
        {"daily_report_id": 1, "questionnaire_id": 22, "answer": 3, "threshold_value": 3},  # 自身の余裕度（選択）
    ]

    for answer_data in answers:
        answer, created = DailyReportAnswer.objects.get_or_create(**answer_data)
        print(f'Daily Report Answer created: ID {answer.id}')

    # 質問の選択肢データを作成
    options = [
        {"questionnaire_id": 3, "option_text": "良い", "option_value": 1},
        {"questionnaire_id": 3, "option_text": "少し良い", "option_value": 2},
        {"questionnaire_id": 3, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 3, "option_text": "少し悪い", "option_value": 4},
        {"questionnaire_id": 3, "option_text": "悪い", "option_value": 5},
        {"questionnaire_id": 4, "option_text": "食べた", "option_value": 1},
        {"questionnaire_id": 4, "option_text": "まだ食べていない", "option_value": 2},
        {"questionnaire_id": 4, "option_text": "食べていない", "option_value": 3},
        {"questionnaire_id": 6, "option_text": "良い", "option_value": 1},
        {"questionnaire_id": 6, "option_text": "少し良い", "option_value": 2},
        {"questionnaire_id": 6, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 6, "option_text": "少し悪い", "option_value": 4},
        {"questionnaire_id": 6, "option_text": "悪い", "option_value": 5},
        {"questionnaire_id": 8, "option_text": "良い", "option_value": 1},
        {"questionnaire_id": 8, "option_text": "少し良い", "option_value": 2},
        {"questionnaire_id": 8, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 8, "option_text": "少し悪い", "option_value": 4},
        {"questionnaire_id": 8, "option_text": "悪い", "option_value": 5},
        {"questionnaire_id": 9, "option_text": "ポジティブ", "option_value": 1},
        {"questionnaire_id": 9, "option_text": "ニュートラル", "option_value": 2},
        {"questionnaire_id": 9, "option_text": "ネガティブ", "option_value": 3},
        {"questionnaire_id": 10, "option_text": "非常に高い", "option_value": 1},
        {"questionnaire_id": 10, "option_text": "高い", "option_value": 2},
        {"questionnaire_id": 10, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 10, "option_text": "低い", "option_value": 4},
        {"questionnaire_id": 10, "option_text": "非常に低い", "option_value": 5},
        {"questionnaire_id": 11, "option_text": "非常に良い", "option_value": 1},
        {"questionnaire_id": 11, "option_text": "良い", "option_value": 2},
        {"questionnaire_id": 11, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 11, "option_text": "悪い", "option_value": 4},
        {"questionnaire_id": 11, "option_text": "非常に悪い", "option_value": 5},
        {"questionnaire_id": 12, "option_text": "非常に高い", "option_value": 1},
        {"questionnaire_id": 12, "option_text": "高い", "option_value": 2},
        {"questionnaire_id": 12, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 12, "option_text": "低い", "option_value": 4},
        {"questionnaire_id": 12, "option_text": "非常に低い", "option_value": 5},
        {"questionnaire_id": 13, "option_text": "症状なし", "option_value": 1},
        {"questionnaire_id": 13, "option_text": "軽い症状", "option_value": 2},
        {"questionnaire_id": 13, "option_text": "中程度の症状", "option_value": 3},
        {"questionnaire_id": 13, "option_text": "重い症状", "option_value": 4},
        {"questionnaire_id": 13, "option_text": "非常に重い症状", "option_value": 5},
        {"questionnaire_id": 14, "option_text": "非常に高い", "option_value": 1},
        {"questionnaire_id": 14, "option_text": "高い", "option_value": 2},
        {"questionnaire_id": 14, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 14, "option_text": "低い", "option_value": 4},
        {"questionnaire_id": 14, "option_text": "非常に低い", "option_value": 5},
        {"questionnaire_id": 15, "option_text": "はい", "option_value": 1},
        {"questionnaire_id": 15, "option_text": "いいえ", "option_value": 2},
        {"questionnaire_id": 16, "option_text": "はい", "option_value": 1},
        {"questionnaire_id": 16, "option_text": "いいえ", "option_value": 2},
        {"questionnaire_id": 17, "option_text": "なし", "option_value": 1},
        {"questionnaire_id": 17, "option_text": "少しある", "option_value": 2},
        {"questionnaire_id": 17, "option_text": "ある", "option_value": 3},
        {"questionnaire_id": 17, "option_text": "多い", "option_value": 4},
        {"questionnaire_id": 17, "option_text": "非常に多い", "option_value": 5},
        {"questionnaire_id": 18, "option_text": "必要", "option_value": 1},
        {"questionnaire_id": 18, "option_text": "少し必要", "option_value": 2},
        {"questionnaire_id": 18, "option_text": "不要", "option_value": 3},
        {"questionnaire_id": 22, "option_text": "非常に余裕がある", "option_value": 1},
        {"questionnaire_id": 22, "option_text": "少し余裕がある", "option_value": 2},
        {"questionnaire_id": 22, "option_text": "普通", "option_value": 3},
        {"questionnaire_id": 22, "option_text": "少し余裕がない", "option_value": 4},
        {"questionnaire_id": 22, "option_text": "余裕がない", "option_value": 5},
    ]

    for option_data in options:
        option, created = QuestionnaireOption.objects.get_or_create(**option_data)
        print(f'Option created: {option.option_text} for Questionnaire ID {option.questionnaire_id}')

    print("Demo data inserted successfully.")