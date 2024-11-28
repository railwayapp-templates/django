# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Source the environment variables
export $(grep -v '^#' .env | xargs)

