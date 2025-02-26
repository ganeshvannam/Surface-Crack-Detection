# Surface Crack Detection using CNNs and PySpark

## Overview

This project implements a robust system for detecting surface cracks in images, a critical task in preventing structural failures across various industries like manufacturing and construction.  Leveraging the power of Convolutional Neural Networks (CNNs), the system achieves high accuracy in identifying cracks.  Furthermore, the project utilizes PySpark for distributed data processing, enabling efficient handling of large datasets and ensuring scalability for real-world applications.

## Table of Contents

- [Project Goals](#project-goals)
- [Dataset](#dataset)
- [Data Splitting](#data-splitting)
- [Models](#models)
- [VGG16 Architecture](#vgg16-architecture)
- [Hyperparameter Tuning](#hyperparameter-tuning)
- [Evaluation Metrics](#evaluation-metrics)
- [Performance](#performance)
- [Team](#team)

## Project Goals

The core objective of this project is to develop a highly accurate and efficient system for surface crack detection in images.  This system aims to mitigate the risk of structural failures by enabling early identification of cracks.  A key aspect of the project is the integration of PySpark for scalable data processing, allowing the system to handle large image datasets effectively.

## Dataset

The dataset used in this project was sourced from Kaggle. It consists of 40,000 images, equally divided into two classes:

- Positive Crack Images: 20,000 images
- Negative Crack Images: 20,000 images

## Data Splitting

The dataset was partitioned into training, validation, and test sets to ensure robust model evaluation and prevent overfitting. The splits are as follows:

- Training Set: 70% (28,000 images)
- Validation Set: 15% (6,000 images)
- Test Set: 15% (6,000 images)

## Models

Several CNN architectures were explored in this project, including:

- VGG16
- Custom CNN
- ResNet50
- LeNet

## VGG16 Architecture

The VGG16 model was selected for its strong performance in image classification tasks. The architecture employed in this project includes:

- Input Layer: (224x224x3)
- Pre-trained VGG16 Base
- Flatten Layer
- Dense Layer 1: 128 units, ReLU activation
- Dropout Layer 1: 50%
- Dense Layer 2: 64 units, ReLU activation
- Dropout Layer 2: 50%
- Output Layer: 2 units, Softmax activation

## Hyperparameter Tuning

Careful attention was paid to hyperparameter tuning to optimize model performance. The following strategies were employed:

- Learning Rate: Initialized at 0.0001 with a scheduling mechanism for gradual decrease.
- Grid Search: Exploration of various combinations of learning rate, dropout rate, and batch size.
- Batch Size: 32
- Optimizer: Adam
- Dropout Rate: 0.5

## Evaluation Metrics

Model performance was assessed using standard classification metrics, including:

- Precision
- Recall
- F1-Score
- Accuracy
- Confusion Matrix



## Team

- Madhumitha Mandyam
- Muneendra Magani
- Nandhika Rajmanikandan
