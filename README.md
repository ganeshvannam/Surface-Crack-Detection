# Surface Crack Detection

## Overview

This project implements a surface crack detection system using Convolutional Neural Networks (CNNs) and PySpark. The goal is to develop an efficient system for detecting surface cracks in images to prevent structural failures in industries such as manufacturing and construction. The project utilizes CNNs for image classification and PySpark for distributed data processing, allowing for scalable and efficient handling of large image datasets.

## Project Goals

The main objective of this project is to build a system that can accurately detect surface cracks in images. The system should enable early detection of cracks to reduce the risk of structural failures. The project also incorporates PySpark for scalable image data processing, ensuring that the system can handle large datasets efficiently.

## Dataset

The dataset used in this project is sourced from Kaggle and consists of 40,000 images divided into two categories:

- Positive Crack Images: 20,000 images
- Negative Crack Images: 20,000 images

### Data Splitting

The dataset is split into training, validation, and test sets:

- Training Set: 70% (28,000 images)
- Validation Set: 15% (6,000 images)
- Test Set: 15% (6,000 images)

## Models

The following CNN architectures were explored in this project:

- VGG16
- Custom CNN
- ResNet50
- LeNet

## Hyperparameter Tuning

The following hyperparameters were tuned to optimize model performance:

- **Learning Rate**: 0.0001 with scheduling for gradual decrease.
- **Grid Search**: Exploration of combinations of learning rate, dropout rate, and batch size.
- **Batch Size**: 32
- **Optimizer**: Adam
- **Dropout Rate**: 0.5

## Evaluation Metrics

The model performance was evaluated using the following classification metrics:

- Precision
- Recall
- F1-Score
- Accuracy
- Confusion Matrix

## Team Members
- Nandhika Rajmanikandan
- Madhumitha
- Muneendra
