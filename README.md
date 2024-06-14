# Card-OCR-Classifier

A comprehensive machine learning project designed to classify and OCR KTP, KIS, and NPWP cards. The project leverages a fine-tuned ResNet50 model for classification and EasyOCR for optical character recognition.

## Features

- **Image Preprocessing:** Enhances image quality for better OCR accuracy.
- **Data Augmentation:** Applies random transformations to improve model robustness.
- **ResNet50 Classifier:** Fine-tuned on card images to achieve high accuracy.
- **EasyOCR Integration:** Separate OCR models for KTP, KIS, and NPWP cards.
- **RESTful API:** Built with Flask to interface with the models.
- **Dockerized Deployment:** Containerized for easy deployment on Google Cloud Platform.

## Getting Started

### Prerequisites

- Python 3.9
- TensorFlow
- EasyOCR
- Flask
- Docker

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/Card-OCR-Classifier.git
   cd Card-OCR-Classifier
