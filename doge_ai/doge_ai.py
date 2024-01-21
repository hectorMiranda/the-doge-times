import openai
import os


def query_openai(prompt, model="text-davinci-003", max_tokens=100):
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def main():
    prompt = "What is dogecoin?"
    response = query_openai(prompt)
    print("Ð>", response)

if __name__ == "__main__":
    main()
