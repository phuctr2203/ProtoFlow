"""Authored 'expected' lightweight design for the document-Q&A MVP (Idea.MD §24-26).
Used by the MockLLMProvider so the design pipeline runs offline. Kept small."""

from app.ai.schemas.design import DesignSpec, Screen


def build_design() -> DesignSpec:
    return DesignSpec(
        user_journey=["Dashboard", "Upload", "Processing", "Chat", "Answer + Sources"],
        screens=[
            Screen(name="Documents", description="List and upload documents"),
            Screen(name="Upload", description="Drag & drop a PDF"),
            Screen(name="Chat", description="Ask questions in natural language"),
            Screen(name="Answer + Sources", description="Answer with citation chips"),
        ],
        navigation=["Sidebar: Documents, Chat"],
        ui_states=["Empty", "Uploading", "Indexing", "Answered", "Error"],
        components=["UploadDropzone", "ChatInput", "AnswerCard", "CitationChip"],
        apis=["POST /documents", "GET /documents", "POST /ask"],
        data_model=["Document", "Chunk", "Embedding", "Conversation"],
        ai_workflow=["Extract text → chunk → embed → store → retrieve → answer with citations"],
        tech_decisions=[
            "React + Vite frontend",
            "FastAPI backend",
            "Qdrant for vector retrieval",
            "OpenAI-compatible LLM via provider layer",
        ],
    )
