# Sudolver models
This repository contains the training data and ML models for the sudolver app.

This repository can be viewed as a sort of incubator project for models. As soon as a model is good enough it will be incorporated into sudolver.app and put into production.

## Model Performance (training/validation set)

| Model | Correct (%)  |
| :---:   | :-: |
| YOLO + Contours(clip=2,3,4,6,8,10/tiles=4,5,6,8) + SVM + Opening/Backup YOLO + Laplacian (alpha=10) + AWS Textract | 73.23 |
| YOLO + Contours(clip=3,4,5,6/tiles=8,16) + SVM/Backup YOLO + Laplacian (alpha=10) + AWS Textract | 71.21 |
| YOLO + Contours(clip=2,3,4,6,8,10/tiles=4,5,6,8) + SVM + Opening | 58.08 |
| YOLO + Laplacian (alpha=10) + AWS Textract | 56.64 |
| YOLO + Contours(clip=3,4,5,6/tiles=8,16) + SVM | 56.56 |
| YOLO + Laplacian (alpha=5) + AWS Textract | 55.55 |
| YOLO + Unsharp Masking (k=10) + AWS Textract | 52.60 |
| YOLO + Unsharp Masking (k=5) + AWS Textract | 51.44 |
| AWS Textract | 28.13 |

Tesseract OCR was also used, but didn't give good enough results.

## Model Performance (test set)

| Model | Correct (%)  |
| :---:   | :-: |
| YOLO + Laplacian (alpha=10) + AWS Textract | 65.90 |
| Laplacian (alpha=10) + AWS Textract | 47.72 |
| AWS Textract | 27.27 |
| YOLO + AWS Textract | 15.90 |

The YOLO + Laplacian sharpening + AWS Textract approach yielded the best results with more than 40% better performance than with just AWS Textract alone.
It has to be said that the dataset used was very small (ca. 250 images in total and 45 for the test set).

## Models

The models use a variation of:

* AWS Textract to extract the numbers from the tables
* YOLO for detecting a sudoku grid and cutting the image to just that grid
* Denoising/Highpass filters in the form of a laplacian operator