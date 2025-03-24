# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os

from semantic_kernel.agents import BedrockAgent, BedrockAgentThread
from semantic_kernel.contents.binary_content import BinaryContent

"""
This sample shows how to interact with a Bedrock agent that is capable of writing and executing code.
This sample uses the following main component(s):
- a Bedrock agent
You will learn how to create a new Bedrock agent and ask it a question that requires coding to answer.
After running this sample, a bar chart will be generated and saved to a file in the same directory
as this script.
"""

AGENT_NAME = "semantic-kernel-bedrock-agent"
INSTRUCTION = "You are a friendly assistant. You help people find information."


ASK = """
Create a bar chart for the following data:
Panda   5
Tiger   8
Lion    3
Monkey  6
Dolphin  2
"""


async def main():
    bedrock_agent = await BedrockAgent.create_and_prepare_agent(AGENT_NAME, instructions=INSTRUCTION)
    await bedrock_agent.create_code_interpreter_action_group()

    thread: BedrockAgentThread = None

    # Placeholder for the file generated by the code interpreter
    binary_item: BinaryContent | None = None

    try:
        # Invoke the agent
        async for response in bedrock_agent.invoke(
            input_text=ASK,
            thread=thread,
        ):
            print(f"Response:\n{response}")
            thread = response.thread
            if not binary_item:
                binary_item = next((item for item in response.items if isinstance(item, BinaryContent)), None)
    finally:
        # Delete the agent
        await bedrock_agent.delete_agent()
        await thread.delete() if thread else None

    # Save the chart to a file
    if not binary_item:
        raise RuntimeError("No chart generated")

    file_path = os.path.join(os.path.dirname(__file__), binary_item.metadata["name"])
    binary_item.write_to_file(os.path.join(os.path.dirname(__file__), binary_item.metadata["name"]))
    print(f"Chart saved to {file_path}")

    # Sample output (using anthropic.claude-3-haiku-20240307-v1:0):
    # Response:
    # Here is the bar chart for the given data:
    # [A bar chart showing the following data:
    # Panda   5
    # Tiger   8
    # Lion    3
    # Monkey  6
    # Dolpin  2]
    # Chart saved to ...


if __name__ == "__main__":
    asyncio.run(main())
