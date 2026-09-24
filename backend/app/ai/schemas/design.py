from pydantic import BaseModel, Field


class Screen(BaseModel):
    name: str
    description: str = ""


class DesignSpec(BaseModel):
    user_journey: list[str] = Field(default_factory=list)
    screens: list[Screen] = Field(default_factory=list)
    navigation: list[str] = Field(default_factory=list)
    ui_states: list[str] = Field(default_factory=list)
    components: list[str] = Field(default_factory=list)
    apis: list[str] = Field(default_factory=list)
    data_model: list[str] = Field(default_factory=list)
    ai_workflow: list[str] = Field(default_factory=list)
    tech_decisions: list[str] = Field(default_factory=list)


# ---- per-agent (node) response models ----


class UXDesign(BaseModel):
    user_journey: list[str] = Field(default_factory=list)
    screens: list[Screen] = Field(default_factory=list)
    navigation: list[str] = Field(default_factory=list)
    ui_states: list[str] = Field(default_factory=list)


class SolutionDesign(BaseModel):
    components: list[str] = Field(default_factory=list)
    apis: list[str] = Field(default_factory=list)
    data_model: list[str] = Field(default_factory=list)
    ai_workflow: list[str] = Field(default_factory=list)
    tech_decisions: list[str] = Field(default_factory=list)
