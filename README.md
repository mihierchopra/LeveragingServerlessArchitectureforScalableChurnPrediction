# LeveragingServerlessArchitectureforScalableChurnPrediction
Leveraging Serverless Architecture for Scalable Churn Prediction

## Introduction
Organizations are increasingly turning to advanced data analytics to efficiently address customer churn in today's extremely competitive business environment, where client retention is crucial for continued profitability. Our project focuses on creating a complex system driven by Artificial Neural Network (ANN) models since we understand how important it is to keep consumers and reduce churn. By utilizing past customer information and behavioral trends, our technology attempts to forecast the likelihood of a certain customer leaving, allowing companies to take preventative measures to keep customers. Our adoption of innovative serverless architecture guarantees software development and deployment at a reasonable cost. Our solution provides enterprises with a cost-effective and comprehensive strategy to monitoring and minimizing client turnover through its seamless connection with Streamlit and other technologies. In an increasingly competitive market scenario, this initiative seeks to provide organizations with actionable information that will improve customer happiness, loyalty, and long-term profitability.

# Objectives
1. Create a data pipeline to ingest and process customer data from an S3 bucket.
2. For training on preprocessed data, use Lambda functions to create an artificial neural network.
3. Deploy the trained model to S3 for quick access and scalability.
4. Integrate the prediction model with Streamlit, which is hosted using Docker, to create a user-friendly interface for input and viewing of churn predictions.
5. Evaluate the prediction model's performance using relevant metrics and make any required.
6. Adjustments to improve accuracy.
7. Demonstrate the solution's efficacy in anticipating customer turnover, as well as its potential.
8. Influence on corporate decisions and retention efforts.
   
# Project Motivation or Significance
The motivation for the project derives from the growing demand for organizations to use data-driven insights to improve client retention. Businesses that leverage the power of ANN models and integrate them into a user-friendly platform like Streamlit may receive significant insights into consumer behavior and take proactive efforts to lower churn rates. This project seeks to provide organizations with an effective and scalable solution for anticipating customer turnover, resulting in increased customer happiness and long-term profitability.

# Ingesting and Storing the Data
Firstly, we upload our dataset to the AWS S3 Bucket. The data is sourced from Kaggle. We decide to utilize AWS Lambda functions for processing and training our model. These functions read the data from the S3 bucket, process it, and then train the model. After training, the model is stored back in S3 for future prediction tasks. We opt for this approach to optimize server costs by leveraging a serverless architecture.

# Data Pipeline Diagram:
1. Data Source: Kaggle
2. AWS S3: Stores the processed data for further analysis and long-term retention.
3. AWS Lambda: Processes and transforms the data.
4. AWS S3: Stores the trained machine learning model and its properties for future prediction tasks.

# Data Transformation
In our data transformation process, with already cleaned data, our focus shifts to optimizing feature engineering and preprocessing for model training. Techniques like LabelEncoder, ColumnTransformer, and StandardScaler are used to make the data suitable for machine learning algorithms. LabelEncoder translates categorical variables into numerical representations compatible with models requiring numeric inputs. ColumnTransformer ensures proper treatment of diverse data types, while StandardScaler maintains consistency across scales, stabilizing model behavior. Furthermore, we stored these objects (LabelEncoder, ColumnTransformer, and StandardScaler) in S3 by pickling each of them to maintain their properties, which are then utilized for prediction in subsequent steps.

In terms of the time taken for transformation, the process is relatively quick. However, to further expedite the process and optimize storage in S3, I streamlined the write operation by consolidating all objects into a single entity. This consolidation ensures efficiency during prediction as it reduces the time required to load packages.

# Dataset Overview
The dataset utilized in this project comprises several key features essential for predicting customer churn and devising effective retention strategies. The dataset includes the following columns:

RowNumber : A unique identifier for each row in the dataset, primarily used for indexing purposes.
CustomerId : A unique identifier assigned to each customer, facilitating individual-level analysis.
Surname : The surname of the customer, providing additional demographic information.
CreditScore : The credit score of the customer, indicating their creditworthiness and financial health.
Geography : The geographical location of the customer, which may influence their behavior and preferences.
Gender : The gender of the customer, providing insights into potential demographic trends.
Age : The age of the customer, a crucial demographic variable affecting purchasing behavior and loyalty.
Tenure : The duration of the customer's relationship with the organization, offering insights into customer loyalty.
Balance : The account balance of the customer, reflecting their financial status and activity.
NumOfProducts : The number of products/services used by the customer, indicating their level of engagement with the organization.
HasCrCard : A binary indicator (1 or 0) representing whether the customer holds a credit card with the organization.
IsActiveMember : A binary indicator (1 or 0) indicating whether the customer is an active member of the organization.
EstimatedSalary : The estimated salary of the customer, providing additional financial context.
Exited : A binary target variable (1 or 0) indicating whether the customer has churned or not.

This dataset offers a comprehensive view of customer attributes and behavior, enabling the development of predictive models to anticipate churn and inform proactive retention strategies. Through thorough analysis and modeling, we aim to leverage this dataset to empower organizations with actionable insights for enhancing customer satisfaction, loyalty, and long-term profitability.

# Project Implementation and Workflow
Step 1: Loading Dataset
The dataset is acquired from Kaggle and securely stored in an Amazon S3 bucket, implementing stringent security measures to safeguard sensitive customer data.

Step 2: Model Training
For model training, the dataset is loaded from the S3 bucket. Data preprocessing involves scaling using Standard Scaling, transformation using Column Transformer, and encoding using Label Encoder. Subsequently, the data is fitted with the ANN algorithm to predict churn.

Step 3: Internal Model Training Code
Post model training, the model is uploaded by pickling it to AWS S3. Additionally, variables representing Standard Scaling, Column Transformation, and Label Encoder are pickled to retain their properties during prediction.

Step 4: Dockerizing the Training Model
Initially, the training code is attempted to be written directly in an AWS Lambda function. However, due to the 50 MB limit for adding layers to the Lambda function and the size of the keras package exceeding 400MB, the approach is shifted towards containerization. Lambda function deployment is done using containers to overcome this limitation.

Step 5: Elastic Container Registry
In our workflow, we utilize Elastic Container Registry (ECR) as the container repository. We begin by building the Docker image on our local system and then proceed to upload it to Docker Hub. Subsequently, we utilize EC2 as an intermediary to push the Docker image from Docker Hub to ECR. Due to the limitations of assigned lab roles, EC2 serves as a medium for communication between AWS tools without requiring additional authentication credentials.

Step 6: Deploying Lambda Function for Dataset Training
Following the upload of the Docker image to ECR, we create a Lambda function using this image. While ideally, the Lambda function could be triggered automatically upon dataset upload to the S3 bucket, for simplicity, we manually trigger the function. As a result, the model and related properties are stored on the S3 bucket for future use.

Step 7: Predicting Using the Deployed Model
For prediction purposes, we retrieve the pickled model from the S3 bucket. Additionally, we load the scaler and transformation variables from the S3 bucket to scale and transform incoming data from user input.

Step 8: Dockerizing the Prediction Code
Due to the 50 MB limit for adding layers to the Lambda function, we opt to deploy the prediction code using containers. We begin by building the Docker image on our local system and then proceed to upload it to Elastic Container Registry (ECR) via Docker Hub and EC2.

Step 9: API Gateway
To facilitate user interaction with our prediction function, we establish an endpoint as our API Gateway. This gateway enables the transmission of user input to the prediction Lambda function. We configure this API Gateway as a trigger for the prediction Lambda function to initiate predictions based on user input.

Step 10: User Interface
The final step involves creating a user-friendly interface where users can input relevant data and receive predictions regarding the likelihood of a customer leaving or staying. For this purpose, we employ Streamlit as our platform of choice.

Step 11: Internals of Streamlit Application
Within the Streamlit application, we develop an interactive interface to capture user input. Leveraging the API Gateway, we transmit this data to the Lambda function for prediction. Subsequently, the predicted results are displayed as output to the user in real-time.

Step 12: Hosting the Frontend Application
Given the constraints of our lab role and limited AWS security credentials, we deploy the application on an EC2 instance. Using Docker, we containerize the application and push it to Docker Hub. We then pull the Docker image to the EC2 instance and run it. To maintain a static IP address, we assign an elastic IP address to the EC2 instance, ensuring consistent accessibility for users.

# Conclusion
In conclusion, our project successfully addresses the critical challenge of predicting and mitigating customer churn through the implementation of advanced data analytics techniques and innovative technologies. By leveraging Artificial Neural Network (ANN) models and integrating them with user-friendly interfaces like Streamlit, we have developed a comprehensive solution to anticipate customer turnover and empower organizations with actionable insights for proactive retention strategies.

Throughout the project, we meticulously executed each step, from loading the dataset and training the model to deploying it using Docker containers and establishing endpoints via API Gateway. Despite the constraints of lab roles and AWS security credentials, we navigated challenges effectively, ensuring the seamless functioning of the system.

Our user interface provides a straightforward platform for users to input relevant data and receive churn predictions promptly. Hosting the frontend application on EC2, coupled with Dockerization, ensures scalability and accessibility.

Overall, this project demonstrates the effectiveness of leveraging data-driven insights and modern technologies to enhance customer retention efforts. Moving forward, the insights gained from this project can inform strategic decision-making and contribute to long-term business success by fostering customer satisfaction, loyalty, and profitability.
