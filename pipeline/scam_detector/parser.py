from typing import Dict, Any
from utils import get_logger, extract_json_from_text

logger = get_logger(__name__)

class OutputParser:
    """Parses LLM output into structured format."""
   
    def parse_llm_output(self, llm_output: str) -> Dict[str, Any]:
        logger.info(f"Parsing LLM output of length: {len(llm_output)}")

        # Case 1: None
        if llm_output is None:
            logger.error("LLM output is None.")
            return {
                "label": "Uncertain",
                "reasoning": "No response received from LLM",
                "intent": "Could not determine",
                "risk_factors": ["empty_response"]
            }

        # Case 2: Structured Gemini response object
        if hasattr(llm_output, "candidates"):
            try:
                parts = llm_output.candidates[0].content.parts
                text_parts = [p.text for p in parts if hasattr(p, "text") and p.text]
                llm_text = "\n".join(text_parts) if text_parts else ""
                logger.info(f"Parsing structured LLM output, text length: {len(llm_text)}")
            except Exception as e:
                logger.error(f"Failed to extract text from Gemini response: {e}")
                llm_text = ""
        else:
            # Case 3: Plain string
            llm_text = str(llm_output)
            logger.info(f"Parsing plain LLM output of length: {len(llm_text)}")

        
        # Try to extract JSON using utils function
        parsed_json = extract_json_from_text(llm_output)
       
        if parsed_json:
            logger.info("Successfully parsed LLM output to JSON.")
            return parsed_json
        else:
            logger.warning("No JSON found in LLM output.")
            # Return fallback result
            fallback_result = {
                "label": "Uncertain",
                "reasoning": "Failed to parse response: No JSON found",
                "intent": "Could not determine",
                "risk_factors": []
            }
            return fallback_result
