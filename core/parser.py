import logging
from typing import List, Dict, Any, Optional
from pydantic import ValidationError
from core.schemas import ParsedItem

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class DataParser:
    @staticmethod
    def parse_raw_item(raw_data: Dict[str, Any]) -> Optional[ParsedItem]:
        try:
            item = ParsedItem.model_validate(raw_data)
            return item
        except ValidationError as e:
            logging.error(f"structure err: {e}")
            return None

    @classmethod
    def parse_batch(cls, raw_list: List[Dict[str, Any]]) -> List[ParsedItem]:
        parsed_items = []
        for raw in raw_list:
            if isinstance(raw, dict):
                valid_item = cls.parse_raw_item(raw)
                if valid_item:
                    parsed_items.append(valid_item)
        return parsed_items