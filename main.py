import argparse
from ast import arg
import os
from argparse import ArgumentParser
import sys
import threading
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT, ITERATION_LIMIT
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    model_has_solution = False

    for _ in range(ITERATION_LIMIT):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0,
                tools=[available_functions],
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        metadata = response.usage_metadata
        assert metadata is not None

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {metadata.prompt_token_count}")
            print(f"Response tokens: {metadata.candidates_token_count}")

        function_responses = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)

                if not function_call_result.parts:
                    raise Exception("Something within the SDK went wrong")

                function_response_part = function_call_result.parts[0]
                if function_response_part.function_response:
                    if function_response_part.function_response.response:
                        function_responses.append(function_response_part)
                        if args.verbose:
                            resulting_printable = str(
                                function_response_part.function_response.response[
                                    "result"
                                ]
                            )
                            print(
                                f"-> {resulting_printable[:100]} ... (Truncated)"
                                if len(resulting_printable) > 100
                                else f"-> {resulting_printable}"
                            )

                        messages.append(
                            types.Content(role="user", parts=function_responses)
                        )
                    else:
                        raise Exception("No response received from LLM")
                else:
                    raise Exception("Something went wrong")
        else:
            print(response.text)
            model_has_solution = True
            break

    if not model_has_solution:
        print(f"The model couldn't find a solution within {ITERATION_LIMIT} loops.")
        sys.exit(1)


if __name__ == "__main__":
    main()
