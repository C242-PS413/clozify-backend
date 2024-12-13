# Bangkit 2024 Capstone Project [C242-PS413] : Clozify

---
## **Clozify - Personalized Fashion Recommendation System**

Welcome to **Clozify**, the Bangkit 2024 Capstone Project for Team **C242-PS413**. Clozify is an innovative mobile application that recommends personalized outfits based on the user's mood and the weather, combining machine learning, cloud computing, and mobile development to create a seamless, data-driven fashion experience.

---

## Team

Here is the list of members of the C242-PS413 team:
|            Name           | Bangkit ID       |   Learning Path    |                        Universitas                        |
|---------------------------|------------------|--------------------|--------------------------------------------------------|
| Raihan Putra Savana       | M279B4KY3655     | Machine Learning   | Universitas Negeri Malang                   |
| Farren Lyrananda Rachman  | M269B4KX1426     | Machine Learning   | Universitas Mulawarman         |
| Andhika Sidiq Firmansyah  | M435B4KY0494     | Machine Learning   | Universitas Islam Bandung          |
| Sela Putri Ismalia        | C269B4KX4097     | Cloud Computing    | Universitas Mulawarman            |
| Wahyu Benartdo Sembiring  | C300B4KY4452     | Cloud Computing    | Universitas Pendidikan Nasional             |
| Siti Nikmatul Ula         | A269B4KX4173     | Mobile Development | Universitas Mulawarman               |
| Nabila Putri Normalita    | A269B4KX3187     | Mobile Development | Universitas Mulawarman               |

---

## Problem Statement

Many individuals struggle with daily outfit decisions, often influenced by factors like mood, weather, and personal style. Current fashion recommendation systems often lack personalization and emotional intelligence.

---

## Project Overview

**Clozify** is a mobile application designed to recommend daily outfits that align with the user's mood and weather conditions. The app uses **machine learning** to detect facial expressions, classifying the user's emotional state, and then suggests outfits based on both their mood and the current weather. This approach provides personalized, practical, and mindful dressing solutions, enhancing user satisfaction while promoting emotional well-being.

---

## Key Features

- **Mood Detection**: Utilizes facial expression analysis to recognize the user's mood through machine learning.
- **Weather Integration**: Incorporates real-time weather data to suggest weather-appropriate clothing.
- **Personalized Recommendations**: Outfits are recommended based on both the user's mood and weather conditions.
- **User-Friendly Interface**: Simple, intuitive mobile interface for submitting mood, weather, and receiving outfit suggestions.
- **Cloud Integration**: Real-time synchronization and storage using cloud services, providing reliable backend support for the app.

---

## Technologies Used

- **Machine Learning**: 
  - **TensorFlow**: For mood recognition model.
  - **Pandas**: Data preprocessing and analysis.
  - **ResNet50**: Embeddings for outfit recommendations.
  - **Cosine Similarity**: For matching outfits based on mood and weather.
  
- **Mobile Development**:
  - **Kotlin**: For building the cross-platform mobile app.
  - **Retrofit**: Handle API requests.
  - **CameraX**: FOr taking picture of user.
  - **MVVM Architecture**: Ensure modularity and clean code.
  
- **Cloud Computing**:
  - **Firebase**: For store data.
  - **FastAPI**: For deploy the model and connect.
  - **Postman**: Testing APIs and analyzing HTTP requests like GET, POST, PUT, DELETE.


---

## Services

| Service                   | Usage                             |
|---------------------------|-----------------------------------|
| Compute Engine            | Backend deployment                |
| Cloud Firestore           | Real-time database                |
| Cloud Storage             | Image storage                     |
| Compute Engine            | Deployment of ML models           |

---

## Dataset

- **Facial Mood Recognition Dataset**: The FER2013 dataset was sourced from the Kaggle website.
- **Outfit Recommendation Dataset**: Fashion Product Images Dataset was sourced from the Kaggle website.

---

Thank you for using Clozify! We hope it makes choosing outfits more fun and effortless.
