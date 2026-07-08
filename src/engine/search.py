import json
import re

class SearchEngine:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = []
        self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.data = []

    def _normalize(self, text: str) -> str:
        """Normalizes text for easier comparison."""
        if not text:
            return ""
        return re.sub(r'[^\w\s]', '', text.lower()).strip()

    def search_by_symptom(self, query: str) -> list[dict]:
        """Search by the canonical symptom name."""
        q = self._normalize(query)
        results = []
        for item in self.data:
            if q in self._normalize(item["sintoma_canonico"]):
                results.append(item)
        return results

    def search_by_zone(self, zone: str) -> list[dict]:
        """Search by the detected physical zones."""
        q = self._normalize(zone)
        results = []
        for item in self.data:
            # Check if the query is in any of the detected zones
            if any(q in self._normalize(z) for z in item["zonas_detectadas"]):
                results.append(item)
        return results

    def search_by_description(self, query: str) -> list[dict]:
        """Search for keywords within the emotional conflict/descriptions."""
        q = self._normalize(query)
        if not q:
            return []
            
        results = []
        for item in self.data:
            # Search in all interpretations
            found = False
            for interp in item["interpretaciones"]:
                conflicto = interp.get("conflicto_emocional", "")
                modelo = interp.get("modelo_mental", "")
                if q in self._normalize(conflicto) or q in self._normalize(modelo):
                    found = True
                    break
            if found:
                results.append(item)
        return results

    def multi_vector_search(self, symptom: str = None, zone: str = None, description: str = None) -> list[dict]:
        """
        Performs an intersectional search across multiple vectors.
        """
        sets = []

        if symptom:
            res = self.search_by_symptom(symptom)
            if res: sets.append(set(map(id, res)))
            else: return [] # If one vector fails, intersection is empty

        if zone:
            res = self.search_by_zone(zone)
            if res: sets.append(set(map(id, res)))
            else: return []

        if description:
            res = self.search_by_description(description)
            if res: sets.append(set(map(id, res)))
            else: return []

        if not sets:
            return []

        # Perform intersection
        intersection_ids = set.intersection(*sets)
        
        # Reconstruct result list
        # We use a dict for faster lookup of the actual objects
        data_dict = {id(item): item for item in self.data}
        return [data_dict[item_id] for item_id in intersection_ids]

if __name__ == "__main__":
    # Quick Test
    engine = SearchEngine("data/processed/processed_data.json")
    print(f"Loaded {len(engine.data)} items.")
    
    print("\n--- Test: Search by Symptom (ACNÉ) ---")
    print(engine.search_by_symptom("acné"))

    print("\n--- Test: Search by Zone (piel) ---")
    print(engine.search_by_zone("piel"))

    print("\n--- Test: Multi-vector (Symptom: ACNÉ AND Zone: cara) ---")
    print(engine.multi_vector_search(symptom="acné", zone="cara"))
