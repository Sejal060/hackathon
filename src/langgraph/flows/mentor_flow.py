from langgraph.graph import StateGraph
import logging
from src.database import get_db
from typing import Dict, Any
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)

async def validate(ctx: Dict[str,Any]) -> Dict[str,Any]:
    if not ctx.get("question"): raise ValueError("question missing")
    return ctx

async def route_to_mentor(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Route to mentor agent
    db = get_db()
    mentor = db.mentors.find_one({"active": True}) or {"_id":"mentor_auto"}
    ctx["mentor_id"] = str(mentor["_id"])
    return ctx

async def generate_reply(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Generate reply using OpenAI
    question = ctx.get("question", "")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful mentor for hackathon participants."},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content
        ctx["reply"] = reply
    except Exception as e:
        logger.error(f"Error generating mentor reply: {str(e)}")
        ctx["reply"] = "Sorry, I'm having trouble generating a response right now. Please try again later."
    
    return ctx

async def store_interaction(ctx: Dict[str,Any]) -> Dict[str,Any]:
    # Store the interaction in the database
    db = get_db()
    
    interaction_record = {
        "user_id": ctx.get("user_id"),
        "question": ctx.get("question"),
        "reply": ctx.get("reply"),
        "mentor_id": ctx.get("mentor_id"),
        "timestamp": ctx.get("timestamp")
    }
    
    db.mentor_interactions.insert_one(interaction_record)
    return ctx

def build_mentor_flow():
    g = StateGraph(dict)
    g.add_node("validate", validate)
    g.add_node("route", route_to_mentor)
    g.add_node("generate_reply", generate_reply)
    g.add_node("store_interaction", store_interaction)
    g.set_entry_point("validate")
    g.add_edge("validate", "route")
    g.add_edge("route", "generate_reply")
    g.add_edge("generate_reply", "store_interaction")
    g.set_finish_point("store_interaction")
    return g.compile()