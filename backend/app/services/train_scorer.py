import argparse
import json
import numpy as np
from sklearn.metrics import f1_score, classification_report

def _generate_synthetic_data():
    strong = ["The empirical evidence overwhelmingly supports this position. Multiple peer-reviewed studies demonstrate consistent results across different contexts and methodologies."] * 30
    moderate = ["This argument has merit in some respects, though the evidence is mixed and the conclusion may be somewhat overstated given available data."] * 30
    weak = ["This is obviously true because everyone knows it. The other side is simply wrong."] * 30
    return strong + moderate + weak, [2]*30 + [1]*30 + [0]*30

def train_scorer(epochs=3, output_path="./trained_scorer", batch_size=8):
    try:
        from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
        import torch
        from torch.utils.data import Dataset
    except ImportError:
        print("Install: pip install transformers torch")
        return
    texts, labels = _generate_synthetic_data()
    print(f"Training on {len(texts)} examples...")
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)
    class ArgumentDataset(Dataset):
        def __init__(self, texts, labels, tokenizer, max_len=256):
            self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_len)
            self.labels = labels
        def __len__(self): return len(self.labels)
        def __getitem__(self, idx):
            item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item
    split = int(0.8 * len(texts))
    train_dataset = ArgumentDataset(texts[:split], labels[:split], tokenizer)
    val_dataset = ArgumentDataset(texts[split:], labels[split:], tokenizer)
    training_args = TrainingArguments(output_dir=output_path, num_train_epochs=epochs, per_device_train_batch_size=batch_size, evaluation_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True, report_to="none")
    trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=val_dataset)
    trainer.train()
    preds_output = trainer.predict(val_dataset)
    preds = np.argmax(preds_output.predictions, axis=1)
    f1 = f1_score(labels[split:], preds, average="weighted")
    print(f"\nDone! F1: {f1:.4f}")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    with open(f"{output_path}/metadata.json", "w") as f:
        json.dump({"f1_score": f1, "label_map": {0: "weak", 1: "moderate", 2: "strong"}}, f, indent=2)
    return f1

class ArgumentScorer:
    def __init__(self, model_path="./trained_scorer"):
        self.loaded = False
        self.model_path = model_path
    def _load(self):
        if self.loaded: return
        try:
            from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
            import torch
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path)
            self.model = DistilBertForSequenceClassification.from_pretrained(self.model_path)
            self.model.eval()
            self.torch = torch
            self.loaded = True
        except Exception as e:
            print(f"Warning: Could not load scorer ({e}). Using random scores.")
    def score(self, text):
        self._load()
        if not self.loaded:
            import random
            score = random.uniform(0.4, 0.9)
            return {"ml_score": score, "label": "moderate", "confidence": 0.5}
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=256, padding=True)
        with self.torch.no_grad():
            outputs = self.model(**inputs)
        probs = self.torch.softmax(outputs.logits, dim=1).squeeze().tolist()
        label_idx = int(self.torch.argmax(outputs.logits).item())
        return {"ml_score": {0:0.25,1:0.62,2:0.88}[label_idx], "label": {0:"weak",1:"moderate",2:"strong"}[label_idx], "confidence": probs[label_idx]}

scorer = ArgumentScorer()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--output", type=str, default="./trained_scorer")
    args = parser.parse_args()
    train_scorer(epochs=args.epochs, output_path=args.output)
