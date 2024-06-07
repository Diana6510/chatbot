import pandas as pd

def calculation_levenshtein_distance(a, b):
    # 레벤슈타인 거리 계산하기
    if a == b: return 0  # 두 문자열이 같으면 거리 0 반환
    a_len = len(a)  # 문자열 a의 길이
    b_len = len(b)  # 문자열 b의 길이
    if a == "": return b_len  # a가 빈 문자열이면 b의 길이 반환
    if b == "": return a_len  # b가 빈 문자열이면 a의 길이 반환

    # 2차원 표(matrix) 초기화합니다.
    matrix = [[] for i in range(a_len+1)]
    for i in range(a_len+1):
        matrix[i] = [0 for j in range(b_len+1)]

    # 첫 번째 행과 열을 초기화합니다.
    for i in range(a_len+1):
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j

    # 표를 채워 레벤슈타인 거리를 계산합니다
    for i in range(1, a_len+1):
        ac = a[i-1]  # a의 i번째 문자
        for j in range(1, b_len+1):
            bc = b[j-1]  # b의 j번째 문자
            cost = 0 if (ac == bc) else 1  # 문자가 같으면 cost 0, 다르면 cost 1
            matrix[i][j] = min([
                matrix[i-1][j] + 1,     # 문자 제거
                matrix[i][j-1] + 1,     # 문자 삽입
                matrix[i-1][j-1] + cost # 문자 변경
            ])
    return matrix[a_len][b_len]  # 최종 거리를 반환합니다.

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)  # 질문과 답변 데이터 로드

    def load_data(self, filepath):
        data = pd.read_csv(filepath)  # CSV 파일 읽기
        questions = data['Q'].tolist()  # 질문열을 리스트로 변환
        answers = data['A'].tolist()   # 답변열을 리스트로 변환
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 입력된 질문과 학습 데이터 질문들 간의 레벤슈타인 거리를 계산합니다.
        distances = [calculation_levenshtein_distance(input_sentence, question) for question in self.questions]
        best_match_index = distances.index(min(distances))  # 가장 작은 거리를 가진 질문의 인덱스 찾기
        return self.answers[best_match_index]  # 해당 인덱스의 답변 반환

# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')  # 사용자 입력
    if input_sentence.lower() == '종료':  # '종료' 입력 시 종료합니다.
        break
    response = chatbot.find_best_answer(input_sentence)  # 입력된 질문에 대한 답변 찾기
    print('Chatbot:', response)  # 답변을 출력합니다.
