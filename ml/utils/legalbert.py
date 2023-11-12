from transformers import AutoTokenizer, AutoModel
from dataclasses import dataclass


@dataclass
class LegalBert:
    tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
    model = AutoModel.from_pretrained("nlpaueb/legal-bert-base-uncased")

    def advice(self, text):
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        return output
    

if __name__ == "__main__":
    print(LegalBert().advice("Establishing a system for the identification and registration of [MASK] animals and regarding the labelling of beef and beef products"))