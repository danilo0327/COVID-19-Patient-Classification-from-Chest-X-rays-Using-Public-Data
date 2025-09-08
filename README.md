# Pulmo-IA — COVID-19 Chest X-ray Classification

##  Project Overview
This project develops a deep learning-based system to classify chest X-rays into **COVID-19**, **Pneumonia**, and **Normal** categories.  
It was carried out for academic purposes as part of a Master's program in Artificial Intelligence.

The workflow integrates **CNN models (Keras & PyTorch)**, **MLflow experiment tracking**, and a prototype **dashboard** for interactive predictions.

---

##  Repository Structure

```bash
.
├── covid_app/           # Web dashboard (Flask + Jinja2)
│   ├── app/             # Backend code, templates, static files
│   ├── requirements.txt # Dashboard dependencies
│   ├── tox.ini          # Testing configuration
│   └── ...
│
├── data/                # Raw data, structured CSVs, DVC tracking
│   ├── raw/             
│   ├── dataframe/
│   └── xray_images.csv.dvc
│
├── models/              # Trained models and class mappings
│   ├── classes_resnet18.json
│   └── covid19-detection-resnet18.zip
│
├── notebooks/           # Training and experiment notebooks
│   ├── Chest_Xray_4Class_Colab.ipynb
│   ├── Chest_Xray_4Class_Colab_MLflow(v2).ipynb
│   ├── EDA.ipynb
│   └── models_test.ipynb
│
└── scripts/             # Utility scripts
    └── create_csv.py


---

##  Models
-  CNN Small (Keras) — Baseline architecture.  
- Simplified CNN (Keras) — Lightweight comparison.  
- ResNet50 and efficientnet_b0. (Transfer Learning, Keras Applications) — Pretrained on ImageNet.  
- ResNet18 (PyTorch) — Best performance, ~80% accuracy.  

Trained weights and artifacts are stored in `models/`.  
Training details are documented in `notebooks/`.  

---

## Dashboard
Implemented with **Flask + Jinja2**:
- Upload an X-ray image.  
- Run the pretrained model.  
- Return the prediction as JSON (current version).  

Future improvements: display class probabilities and overlay results on the uploaded image.

---

##  Experiment Tracking
Experiments were logged with **MLflow** on **AWS EC2**:
- Hyperparameters: learning rate, batch size, weight decay, epochs.  
- Metrics: accuracy, loss, precision, recall, F1-score.  
- Model comparisons across CNN, ResNet50, and ResNet18.  

---

## Teamwork
The project was collaboratively developed using GitHub:
- Data preprocessing and dataset structuring.  
- Model training and evaluation.  
- Experiment tracking with MLflow.  
- Dashboard implementation.  
- Academic documentation and reporting.  

---

## References
- Rahman, T., Chowdhury, M. E. H., Khandakar, A., et al. (2021). *COVID-19 radiography database*. arXiv:2105.10971.  
- He, K., Zhang, X., Ren, S., & Sun, J. (2016). *Deep Residual Learning for Image Recognition*. CVPR.  
- Simonyan, K., & Zisserman, A. (2015). *Very Deep Convolutional Networks for Large-Scale Image Recognition*. ICLR.  
