from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, inference, room_io, TurnHandlingOptions, ChatContext
from livekit.plugins import noise_cancellation
from prompts import SESSION_INSTRUCTION, AGENT_INSTRUCTION, CRITICAL_INSTRUCTION
from tools import (
    call_contact,
    create_event,
    get_current_datetime,
    get_weather,
    list_events,
    place_phone_call,
    search_web,
    send_email,
)
from mem0 import AsyncMemoryClient
import asyncio
import os
import logging
import json

load_dotenv()


def build_stt():
    provider = (os.getenv("STT_PROVIDER") or "").strip().lower()
    speechmatics_key = os.getenv("SPEECHMATICS_API_KEY") or os.getenv("SPEECHMATICS_KEY")
    language = os.getenv("SPEECHMATICS_LANGUAGE") or os.getenv("STT_LANGUAGE") or "en"

    if provider in {"speechmatics", "speechmatics/enhanced"} or (provider not in {"deepgram"} and speechmatics_key):
        return inference.STT(model="speechmatics/enhanced", language=language)

    return inference.STT(model="deepgram/nova-3", language="multi")


def build_tools():
    tools = [
        get_current_datetime,
        get_weather,
        search_web,
        send_email,
        list_events,
        create_event,
        place_phone_call,
        call_contact,
    ]
    mcp_url = os.getenv("N8N_MCP_SERVER_URL") or os.getenv("MCP_SERVER_URL")

    if mcp_url:
        from livekit.agents.llm.mcp import MCPServerHTTP, MCPToolset

        tools.append(
            MCPToolset(
                id="mcp",
                mcp_server=MCPServerHTTP(
                    url=mcp_url,
                    transport_type=os.getenv("MCP_TRANSPORT", "streamable_http"),
                ),
            )
        )

    return tools

class Assistant(Agent):
    def __init__(self, chat_ctx=None) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            stt=build_stt(),
            llm=inference.LLM(model="google/gemma-4-31b-it"),
            tts=inference.TTS(
                model="inworld/inworld-tts-2",
                voice="Ashley",
            ),
            tools=build_tools(),

            chat_ctx=chat_ctx
        )

async def shutdown_hook(chat_ctx: ChatContext, mem0: AsyncMemoryClient, memories_str: str):
    logging.info("Shutting down agent session...")

    messages_formatting = [

    ]

    logging.info(f"Chat context messages: {chat_ctx.items}")

    for item in chat_ctx.items:
        content_str = (
            ''.join(item.content)
            if isinstance(item.content, list)
            else str(item.content)
        )

        if memories_str and memories_str in content_str:
            continue

        if item.role in ["user", "assistant"]:
            messages_formatting.append(
                {
                    "role": item.role,
                    "content": content_str.strip(),
                }
            )

    logging.info(f"Formatted messages: {messages_formatting}")
    await mem0.add(messages_formatting, user_id="Vishal")
    logging.info("Memories saved to mem0.")

async def save_conversation_item(event, mem0: AsyncMemoryClient, memories_str: str):
    try:
        item = event.item
        if item.role not in ["user", "assistant"]:
            return

        content_str = (
            ''.join(item.content)
            if isinstance(item.content, list)
            else str(item.content)
        ).strip()

        if not content_str or (memories_str and memories_str in content_str):
            return

        await mem0.add(
            [{"role": item.role, "content": content_str}],
            user_id="Vishal",
        )
        logging.info("Conversation item saved to mem0.")
    except Exception:
        logging.exception("Failed to save conversation item to mem0.")

def schedule_memory_save(event, mem0: AsyncMemoryClient, memories_str: str):
    asyncio.create_task(save_conversation_item(event, mem0, memories_str))

server = AgentServer(

)

@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
        turn_handling=TurnHandlingOptions(
            turn_detection=inference.TurnDetector(),
            temperature=0.8,
        ),
    )

    await ctx.connect()

    mem0 = AsyncMemoryClient()
    user_name = 'Vishal'

    response = await mem0.get_all(filters={"user_id": user_name})
    results = response.get("results", [])
    initial_ctx = ChatContext()
    memories = ''
    memories_str = ''

    if results:
        memories = [
            {
                "memory": result["memory"],
                "updated_at": result["updated_at"]
            }
            for result in results
        ]
        memories_str = json.dumps(memories)
        initial_ctx.add_message(
            role="assistant",
            content=f"Memories: {memories_str}"
        )

    agent = Assistant(chat_ctx=initial_ctx)

    await session.start(
        room=ctx.room,
        agent=agent,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=noise_cancellation.NC(),
            ),
        ),
    )

    session.on(
        "conversation_item_added",
        lambda event: schedule_memory_save(event, mem0, memories_str),
    )

    await ctx.connect()


    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )

    ctx.add_shutdown_callback(lambda: shutdown_hook(session._agent.chat_ctx, mem0, memories_str))

if __name__ == "__main__":
    agents.cli.run_app(server)