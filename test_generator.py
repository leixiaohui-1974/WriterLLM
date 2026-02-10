from src.generator import generate_slides
import json

text = "Artificial Intelligence is transforming the world. It is used in healthcare, finance, and transportation. Machine learning is a subset of AI. Deep learning is a subset of machine learning. Neural networks are inspired by the human brain."
slides = generate_slides(text, num_slides=3)
print(json.dumps(slides, indent=2))
assert len(slides) == 3
print("Generator Test Passed")
