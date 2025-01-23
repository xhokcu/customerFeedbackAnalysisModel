# Customer Feedback Analysis Model

This project utilizes a pre-trained sentiment analysis model for analyzing customer feedback.

## Overview

The application uses the `finiteautomata/bertweet-base-sentiment-analysis` model from Hugging Face Transformers for sentiment analysis of customer feedback data. It provides a simple API interface to process Excel files containing feedback data.

## Features

- Excel file processing
- Sentiment analysis using BERTweet model
- API endpoint for file uploads
- Sentiment scoring and labeling

## Requirements

- Flask
- Transformers
- Pandas
- PyTorch
