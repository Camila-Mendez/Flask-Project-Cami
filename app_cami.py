from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'nihongo_app'


users = {
    'Camila': generate_password_hash('password1'),
    'Mani': generate_password_hash('password2')
}

quiz_data = {
    'title': 'JLPT Level Quiz',
    'questions': [
        {
            'id': 1,
            'question_text': 'このかんじのよみかたはなんですか：家族',
            'options': ['かそく', 'かぞうく', 'れいぞうこ', 'かぞく'],
            'correct_answer': 'かぞく'
        },
        {
            'id': 2,
            'question_text': '一番いいオプションを一つ選びなさい。',
            'options': ['昨日本をすべて読んでしまいました。', '昨日本をすべて飲んでしまいました。', '昨日本をすべて忘れてしまいました', '昨日本はすべてが終わってきました'],
            'correct_answer': '昨日本をすべて読んでしまいました。'
        },
        {
            'id': 3,
            'question_text': '日本語が好きですか?',
            'options': ['はい', 'いいえ', 'うん', 'ううん'],
            'correct_answer': 'はい'
        },
        {
            'id': 4,
            'question_text': 'きれいの形容詞のタイプ?',
            'options': ['い形容詞', 'なけようし', 'なにも', '名詞'],
            'correct_answer': 'なけようし'
        },

    ]
}


@app.route('/')
def index():
    return render_template('Index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            print(session)
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = generate_password_hash(password)
            print(users)
            return redirect(url_for('login'))
        else:
            error = 'Username already exists'
            return render_template('register.html', error=error)
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/dashboard/jlpt')
def jlpt():
    if 'username' in session:
        return render_template('jlpt.html')
    return redirect(url_for('login'))


@app.route('/dashboard/jlpt/quiz')
def quiz():
    if 'username' in session:
        return render_template('quiz.html', title=quiz_data['title'], quiz_title=quiz_data['title'],
                               questions=quiz_data['questions'])
    return redirect(url_for('login'))


@app.route('/dashboard/jlpt/quiz/result', methods=['POST'])
def result():
    print("Received POST request")
    user_answers = {key: value for key, value in request.form.items()}
    print("User Answers:", user_answers)
    score, total_questions = calculate_score(user_answers)
    return render_template('result.html', score=score, total_questions=total_questions)


def calculate_score(user_answers):
    score = 0
    total_questions = len(quiz_data['questions'])

    for question in quiz_data['questions']:
        question_id = question['id']
        user_answer = user_answers.get(str(question_id))
        if user_answer and user_answer == question['correct_answer']:
            score += 1

    return score, total_questions


@app.route('/dashboard/haiku')
def haiku():
    if 'username' in session:
        return render_template('haiku.html')
    return redirect(url_for('login'))


@app.route('/dashboard/me')
def me():
    if 'username' in session:
        return render_template('me.html')
    return redirect(url_for('login'))


@app.route('/dashboard/jlpt/courses')
def course():
    if 'username' in session:
        return render_template('courses.html')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
