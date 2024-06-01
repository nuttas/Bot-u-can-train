import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    print("พิมพ์ 'ออก' เพื่อออก")

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'ออก':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: ฉันไม่รู้คำตอบ สอนฉันที')
            new_answer: str = input('พิมพ์คำตอบ หรือ ข้ามโดยการพิมพ์ว่า "ข้าม": ')

            if new_answer.lower() != 'ข้าม':
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: ขอบคุณ, ฉันเรียนรู้การตอบกลับใหม่แล้ว!')

if __name__ == '__main__':
    chat_bot()
