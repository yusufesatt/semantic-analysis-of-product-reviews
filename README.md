# Sentiment analysis of reviews of a product on Trendyol.

This project performs sentiment analysis of comments using the OpenAI API by entering the URL of a product on Trendyol and the number of comments the user wants. It pulls the number of comments the user wants and determines whether each comment is positive, negative or neutral. The results are printed to an Excel file.

To use the project, you will first need an OpenAI API key. To get the key, you need to register on the OpenAI website. Afterwards, you can clone the project from GitHub and run it.

[Click here to see the sample output.](https://prnt.sc/15Rh4XA_infS)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yusufesatt/semantic-analysis-of-product-reviews.git
cd semantic-analysis-of-product-reviews
```

2. Create Virtualenv **(Optional)**:

```bash
python -m venv semantic_env

# Ubuntu & MacOS
source semantic_env/bin/activate

# Windows
semantic_env/Scripts/activate
```

3. Install the required dependencies:

```bash 
pip install -r requirements.txt
```

## Usage

The whole process will take place in one line 

```bash
python app.py
```

## Contributing

If you encounter issues or have suggestions for improvements, please report them on the GitHub repository 🚀.

## License

This project is licensed under the [MIT License](https://github.com/yusufesatt/semantic-analysis-of-product-reviews?tab=MIT-1-ov-file).
