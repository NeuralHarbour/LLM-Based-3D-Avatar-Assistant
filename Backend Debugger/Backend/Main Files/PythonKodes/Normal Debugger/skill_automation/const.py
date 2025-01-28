"""Constants for the Home Assistant Generative Agent."""
from typing import Final

# Configuration keys
CONF_VLM: Final = "vlm"
CONF_VISION_MODEL_TEMPERATURE: Final = "vision_model_temperature"
CONF_VISION_MODEL_TOP_P: Final = "vision_model_top_p"
CONF_SUMMARIZATION_MODEL_TEMPERATURE: Final = "summarization_model_temperature"
CONF_SUMMARIZATION_MODEL_TOP_P: Final = "summarization_model_top_p"

# Default values
DEFAULT_MEMORY_KEY: Final = "initialization"
CONTEXT_MAX_MESSAGES: Final = 100
CONTEXT_SUMMARIZE_THRESHOLD: Final = 10
VLM_NUM_PREDICT: Final = 1024
VISION_MODEL_IMAGE_WIDTH: Final = 640
VISION_MODEL_IMAGE_HEIGHT: Final = 480

# Model configurations
RECOMMENDED_VLM: Final = "openhermes:latest"
RECOMMENDED_VISION_MODEL_TEMPERATURE: Final = 0.7
RECOMMENDED_VISION_MODEL_TOP_P: Final = 0.9
RECOMMENDED_SUMMARIZATION_MODEL_TEMPERATURE: Final = 0.7
RECOMMENDED_SUMMARIZATION_MODEL_TOP_P: Final = 0.9

# Blueprint configuration
BLUEPRINT_NAME: Final = "generative_agent"
EVENT_AUTOMATION_REGISTERED: Final = "automation_registered"

# Prompts
AGENT_SYSTEM_PROMPT: Final = """You are a helpful home assistant agent that can control and monitor various aspects of the home.
You can access cameras, create automations, and maintain memory of important events.
Always think carefully about which tools to use and provide clear, concise responses.
Question: {messages}
"""

VISION_MODEL_SYSTEM_PROMPT: Final = """Analyze the image and provide a clear, detailed description focusing on any notable objects, 
people, or activities. Be specific but concise."""

VISION_MODEL_USER_PROMPT: Final = "What do you see in this image?"

VISION_MODEL_USER_KW_PROMPT: Final = "Look specifically for:"

SUMMARY_SYSTEM_PROMPT: Final = """Summarize the key points of the conversation while maintaining important context and details."""

SUMMARY_INITIAL_PROMPT: Final = "Please provide a summary of our conversation so far."

SUMMARY_PROMPT_TEMPLATE: Final = """Here's what we discussed earlier: {summary}
Please update this summary with our recent conversation."""

EMBEDDING_MODEL_PROMPT_TEMPLATE: Final = """Help me remember anything relevant to: {query}"""

TOOL_CALL_ERROR_TEMPLATE: Final = "Error executing tool: {error}"