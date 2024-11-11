# scripts/insert_demo_data.py
from django.utils import timezone
from myapp.models import Employee, Questionnaire, DailyReport, QuestionnaireThreshold, DailyReportAnswer, QuestionnaireOption
from myapp.models import User
def run():

    # 既存のデータを削除
    Employee.objects.all().delete()
    Questionnaire.objects.all().delete()
    DailyReport.objects.all().delete()
    QuestionnaireThreshold.objects.all().delete()
    DailyReportAnswer.objects.all().delete()
    QuestionnaireOption.objects.all().delete()


# Userデータ
    users = [
        {"username": "田中一郎", "password": "t3stpass1", "email": "johndoe@example.com","employee_type":"admin"},
        {"username": "小山和美", "password": "t3stpass2", "email": "janesmith@example.com"},
        {"username": "山本翔太", "password": "t3stpass3", "email": "michaeljohnson@example.com"},
    ]

# Employeeデータ
    employees = [
        {"name": "田中一郎", "employee_type": "admin"},
        {"name": "小山和美", "employee_type": "general"},
        {"name": "山本翔太", "employee_type": "general"},
    ]

# ユーザーと従業員を組み合わせて処理
    for user_data, emp_data in zip(users, employees):
        # Userの作成（すでに存在する場合はスキップ）
        user, created = User.objects.get_or_create(username=user_data['username'], defaults={k: v for k, v in user_data.items() if k != 'password'})

        # Userが新規作成された場合のみパスワードをセット
        if created:
            user.set_password(user_data['password'])  # パスワードをハッシュ化
            user.save()

        # Employeeの作成（user_id が重複しないように確認）
        emp_data["user"] = user
        
        # Employeeの新規作成（すでに存在する場合はスキップ）
        employee, created = Employee.objects.get_or_create(user=user, defaults=emp_data)
        
        # 新規作成された場合のみログを出力
        if created:
            print(f"Employee created: {employee.name} (ID: {employee.id})")

    # アンケートデータを作成
    questionnaires = [
        {"title": "就寝時間", "type": "morning", "answer_type": "time_select"},
        {"title": "起床時間", "type": "morning", "answer_type": "time_select"},
        {"title": "睡眠の質", "type": "morning", "answer_type": "select"},
        {"title": "今朝の朝食を食べたか", "type": "morning", "answer_type": "select"},
        {"title": "薬を飲んだ時間", "type": "morning", "answer_type": "time_select"},
        {"title": "自分の状態", "type": "morning", "answer_type": "select"},
        {"title": "自分の状態の詳細（自由記述）", "type": "morning", "answer_type": "text"},
        {"title": "不安感のレベル", "type": "morning", "answer_type": "select"},
        {"title": "今の感情", "type": "morning", "answer_type": "select"},
        {"title": "コミュニケーションの意欲", "type": "morning", "answer_type": "select"},
        {"title": "体の調子", "type": "morning", "answer_type": "select"},
        {"title": "集中力の調子", "type": "morning", "answer_type": "select"},
        {"title": "体の不調", "type": "morning", "answer_type": "select"},
        {"title": "自己肯定感", "type": "morning", "answer_type": "select"},
        {"title": "誰かに頼っても良いか", "type": "morning", "answer_type": "select"},
        {"title": "自分が必要とされているか", "type": "morning", "answer_type": "select"},
        {"title": "その他の気になる症状", "type": "morning", "answer_type": "select"},
        {"title": "仕事に対して配慮が必要か", "type": "morning", "answer_type": "select"},
        {"title": "仕事に対して配慮が必要かの詳細", "type": "morning", "answer_type": "text"},
        {"title": "伝えたいこと", "type": "morning", "answer_type": "text"},
        {"title": "回復ルーティン", "type": "morning", "answer_type": "text"},
        {"title": "自身の余裕度", "type": "morning", "answer_type": "select"},
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
        {"daily_report_id": 1, "questionnaire_id": 1, "answer": "22:30"},  # 就寝時間（時間選択）
        {"daily_report_id": 1, "questionnaire_id": 2, "answer": "07:00"},  # 起床時間（時間選択）
        {"daily_report_id": 1, "questionnaire_id": 3, "answer": 1},  # 睡眠の質（選択）
        {"daily_report_id": 1, "questionnaire_id": 4, "answer": 2},  # 今朝の朝食を食べたか（選択）
        {"daily_report_id": 1, "questionnaire_id": 5, "answer": "08:00"},  # 薬を飲んだ時間（時間選択）
        {"daily_report_id": 1, "questionnaire_id": 6, "answer": 4},  # 自分の状態（選択）
        {"daily_report_id": 1, "questionnaire_id": 7, "answer": "体調は安定しているが、少し疲れを感じる。"},  # 自分の状態の詳細（記述）
        {"daily_report_id": 1, "questionnaire_id": 8, "answer": 3},  # 不安感のレベル（選択）
        {"daily_report_id": 1, "questionnaire_id": 9, "answer": 1},  # 今の感情（選択）
        {"daily_report_id": 1, "questionnaire_id": 10, "answer": 4},  # コミュニケーションの意欲（選択）
        {"daily_report_id": 1, "questionnaire_id": 11, "answer": 3},  # 体の調子（選択）
        {"daily_report_id": 1, "questionnaire_id": 12, "answer": 3},  # 集中力の調子（選択）
        {"daily_report_id": 1, "questionnaire_id": 13, "answer": 2},  # 体の不調（選択）
        {"daily_report_id": 1, "questionnaire_id": 14, "answer": 3},  # 自己肯定感（選択）
        {"daily_report_id": 1, "questionnaire_id": 15, "answer": 1},  # 誰かに頼っても良いか（選択）
        {"daily_report_id": 1, "questionnaire_id": 16, "answer": 2},  # 自分が必要とされているか（選択）
        {"daily_report_id": 1, "questionnaire_id": 17, "answer": 3},  # その他の気になる症状（選択）
        {"daily_report_id": 1, "questionnaire_id": 18, "answer": 2},  # 仕事に対して配慮が必要か（選択）
        {"daily_report_id": 1, "questionnaire_id": 19, "answer": "仕事の調整が必要です。"},  # 仕事に対して配慮が必要かの詳細（記述）
        {"daily_report_id": 1, "questionnaire_id": 20, "answer": "特に伝えたいことはありません。"},  # 伝えたいこと（記述）
        {"daily_report_id": 1, "questionnaire_id": 21, "answer": "深呼吸とストレッチを行った。"},  # 回復ルーティン（記述）
        {"daily_report_id": 1, "questionnaire_id": 22, "answer": 3},  # 自身の余裕度（選択）
        
        {"daily_report_id": 2, "questionnaire_id": 1, "answer": "23:00"},  # 就寝時間（時間選択）
        {"daily_report_id": 2, "questionnaire_id": 2, "answer": "07:30"},  # 起床時間（時間選択）
        {"daily_report_id": 2, "questionnaire_id": 3, "answer": 2},  # 睡眠の質（選択）
        {"daily_report_id": 2, "questionnaire_id": 4, "answer": 1},  # 今朝の朝食を食べたか（選択）
        {"daily_report_id": 2, "questionnaire_id": 5, "answer": "07:45"},  # 薬を飲んだ時間（時間選択）
        {"daily_report_id": 2, "questionnaire_id": 6, "answer": 3},  # 自分の状態（選択）
        {"daily_report_id": 2, "questionnaire_id": 7, "answer": "体調はやや良くなったが、少し眠い。"},  # 自分の状態の詳細（記述）
        {"daily_report_id": 2, "questionnaire_id": 8, "answer": 2},  # 不安感のレベル（選択）
        {"daily_report_id": 2, "questionnaire_id": 9, "answer": 3},  # 今の感情（選択）
        {"daily_report_id": 2, "questionnaire_id": 10, "answer": 2},  # コミュニケーションの意欲（選択）
        {"daily_report_id": 2, "questionnaire_id": 11, "answer": 4},  # 体の調子（選択）
        {"daily_report_id": 2, "questionnaire_id": 12, "answer": 4},  # 集中力の調子（選択）
        {"daily_report_id": 2, "questionnaire_id": 13, "answer": 3},  # 体の不調（選択）
        {"daily_report_id": 2, "questionnaire_id": 14, "answer": 2},  # 自己肯定感（選択）
        {"daily_report_id": 2, "questionnaire_id": 15, "answer": 2},  # 誰かに頼っても良いか（選択）
        {"daily_report_id": 2, "questionnaire_id": 16, "answer": 3},  # 自分が必要とされているか（選択）
        {"daily_report_id": 2, "questionnaire_id": 17, "answer": 2},  # その他の気になる症状（選択）
        {"daily_report_id": 2, "questionnaire_id": 18, "answer": 1},  # 仕事に対して配慮が必要か（選択）
        {"daily_report_id": 2, "questionnaire_id": 19, "answer": "もう少し早く仕事を終わらせる必要があります。"},  # 仕事に対して配慮が必要かの詳細（記述）
        {"daily_report_id": 2, "questionnaire_id": 20, "answer": "特に伝えたいことはありません。"},  # 伝えたいこと（記述）
        {"daily_report_id": 2, "questionnaire_id": 21, "answer": "軽い運動をしました。"},  # 回復ルーティン（記述）
        {"daily_report_id": 2, "questionnaire_id": 22, "answer": 2},  # 自身の余裕度（選択）

        {"daily_report_id": 3, "questionnaire_id": 1, "answer": "21:30"},  # 就寝時間（時間選択）
        {"daily_report_id": 3, "questionnaire_id": 2, "answer": "06:45"},  # 起床時間（時間選択）
        {"daily_report_id": 3, "questionnaire_id": 3, "answer": 3},  # 睡眠の質（選択）
        {"daily_report_id": 3, "questionnaire_id": 4, "answer": 1},  # 今朝の朝食を食べたか（選択）
        {"daily_report_id": 3, "questionnaire_id": 5, "answer": "08:00"},  # 薬を飲んだ時間（時間選択）
        {"daily_report_id": 3, "questionnaire_id": 6, "answer": 2},  # 自分の状態（選択）
        {"daily_report_id": 3, "questionnaire_id": 7, "answer": "昨日より少し疲れが残っている。"},  # 自分の状態の詳細（記述）
        {"daily_report_id": 3, "questionnaire_id": 8, "answer": 1},  # 不安感のレベル（選択）
        {"daily_report_id": 3, "questionnaire_id": 9, "answer": 2},  # 今の感情（選択）
        {"daily_report_id": 3, "questionnaire_id": 10, "answer": 3},  # コミュニケーションの意欲（選択）
        {"daily_report_id": 3, "questionnaire_id": 11, "answer": 2},  # 体の調子（選択）
        {"daily_report_id": 3, "questionnaire_id": 12, "answer": 2},  # 集中力の調子（選択）
        {"daily_report_id": 3, "questionnaire_id": 13, "answer": 1},  # 体の不調（選択）
        {"daily_report_id": 3, "questionnaire_id": 14, "answer": 4},  # 自己肯定感（選択）
        {"daily_report_id": 3, "questionnaire_id": 15, "answer": 3},  # 誰かに頼っても良いか（選択）
        {"daily_report_id": 3, "questionnaire_id": 16, "answer": 1},  # 自分が必要とされているか（選択）
        {"daily_report_id": 3, "questionnaire_id": 17, "answer": 4},  # その他の気になる症状（選択）
        {"daily_report_id": 3, "questionnaire_id": 18, "answer": 3},  # 仕事に対して配慮が必要か（選択）
        {"daily_report_id": 3, "questionnaire_id": 19, "answer": "少し時間調整をお願いしたいです。"},  # 仕事に対して配慮が必要かの詳細（記述）
        {"daily_report_id": 3, "questionnaire_id": 20, "answer": "特に伝えたいことはありません。"},  # 伝えたいこと（記述）
        {"daily_report_id": 3, "questionnaire_id": 21, "answer": "リラックスする時間を取りました。"},  # 回復ルーティン（記述）
        {"daily_report_id": 3, "questionnaire_id": 22, "answer": 1}  # 自身の余裕度（選択）
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
