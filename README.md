.

🍽️ Food Image Classification Using Deep Learning
📌 Project Description

This project was developed to classify food images into their respective categories using deep learning and computer vision techniques. The goal was to understand the complete machine learning workflow—from data collection to model evaluation—using a real-world dataset.

🧠 How I Built This Project
1️⃣ Dataset Selection

I selected the Food Image Classification Dataset from Kaggle because it contains labeled food images suitable for training image classification models. The dataset is organized into folders, where each folder represents a food category.

2️⃣ Data Preprocessing

Loaded the images from the dataset directories

Resized all images to a fixed dimension suitable for CNN input

Normalized pixel values to improve training performance

Split the dataset into training and validation sets

3️⃣ Data Augmentation

To prevent overfitting and improve model generalization, I applied image augmentation techniques such as:

Rotation

Zoom

Horizontal flipping

Width and height shifting

This helped the model learn from varied image patterns.

4️⃣ Model Building

Designed a Convolutional Neural Network (CNN) architecture

Used convolution, pooling, and dense layers

Applied ReLU activation and Softmax for multi-class classification

Compiled the model using an appropriate optimizer and loss function

(Alternatively, transfer learning models like ResNet/MobileNet can be used for better accuracy.)

5️⃣ Model Training

Trained the CNN on the augmented training dataset

Monitored training and validation accuracy

Adjusted hyperparameters such as epochs and batch size to improve performance

6️⃣ Model Evaluation

Evaluated the trained model using validation data

Measured accuracy and loss

Verified predictions on unseen food images

7️⃣ Result Analysis

The model was able to correctly classify different food items with good accuracy. Data augmentation significantly improved the model’s performance and reduced overfitting.

🛠️ Tools & Technologies Used

Python

TensorFlow / Keras

CNN (Convolutional Neural Network)

NumPy, Matplotlib, OpenCV

Kaggle Dataset

🎯 What I Learned

End-to-end implementation of an image classification project

Importance of data preprocessing and augmentation

Building and training CNN models

Evaluating and improving deep learning models

🔮 Future Improvements

Implement transfer learning with pre-trained models

Increase dataset size for higher accuracy

Deploy the model using Flask or Streamlit


**contact details:**
📧 Email ID: bhavanikagitha2@gmail.com

💼 LinkedIn profile URL:
https://www.linkedin.com/in/bhavani-kagitha-17ba74273


🐙 GitHub profile URL :
https://github.com/bhavanikagitha2-123

