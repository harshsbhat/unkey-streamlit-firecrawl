# Content Readability score with Unkey X Firecrawl X Streamlit

The app analyzes the readability of content from a provided URL, using various metrics to assess its complexity and clarity. It generates a comprehensive report, including scores like Flesch Reading Ease and SMOG Index, alongside visualizations for better understanding.

This app is rate limited using Unkey. So you can only make 3 requests per 3 minutes.

## Prerequisites

- Python 3.x
- Streamlit
- Requests library
- An account with Unkey with Root Key
- Firecrawl with valid API Key

## Setup Unkey 

1. Go to unkey [ratelimits](https://app.unkey.com/ratelimits)

2. Create a new namespace with name `firecrawl.streamlit`

3. Go to settings/root-keys and create a root key with Ratelimit permissions

4. Add it in the .env file `UNKEY_ROOT_KEY`


## Quickstart

1. Clone this repository:
   
   ```
   git clone https://github.com/harshsbhat/unkey-streamlit-firecrawl.git
   cd unkey-streamlit-firecrawl


3. Set up a virtual environment (optional but recommended): :
   ```
   python3 -m venv venv   # For Linux/macOS
   source venv/bin/activate  # For Linux/macOS

   python -m venv venv   # For Windows
   venv\Scripts\activate  # For Windows

4. Set up your environment variables: Create a .env file in the project root and add the following variables.
Get the Unkey rootkey from [unkey dashboard](http://app.unkey.com/). You can also get the Firecrawl API key from [Firecrawl](https://www.firecrawl.dev/)


   ```
    FIRECRAWL_API_KEY=""
    UNKEY_ROOT_KEY=""
   ```

5. Install the required dependencies


   ```
   pip install -r requirements.txt
   ```

6. Run the app

   ```
   streamlit run app.py
   ```

## Usage

https://www.loom.com/share/dab87938ac9f453fadab5673881e59d5?sid=7266731d-8c90-4184-a04f-d0f10708a562