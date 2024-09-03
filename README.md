Here is a `README.md` file for your ExpenAI project on GitHub. This file outlines the project details, technologies used, features, installation instructions, and sections for screenshots.

---

# ExpenAI 💸

**ExpenAI** is an intelligent expense tracker application that leverages advanced AI capabilities to process expenses from images, voice, and text inputs. With ExpenAI, users can easily manage their expenses by scanning bills, using voice commands, or typing descriptions of their purchases. The app uses Google Generative AI (Gemini) to categorize and extract amounts from various input formats, providing a seamless and intuitive user experience.


## Technologies Used

ExpenAI utilizes the following technologies:

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
- **Streamlit**: An open-source app framework used for creating data-driven web applications in Python.
- **Google Generative AI (Gemini)**: Google’s generative AI model, used for understanding and processing expense data.
- **Docker**: A platform for developing, shipping, and running applications inside lightweight containers, ensuring consistent environments across deployments.
- **Python**: The primary programming language used for backend logic and frontend scripting.
- **Pandas**: A data manipulation and analysis library used to manage and visualize expense data.
- **Plotly**: A graphing library that makes interactive, publication-quality graphs online to visualize expense categories and trends.

## Features

ExpenAI provides a variety of features to help you manage and track your expenses efficiently:

![Add Expenses](https://i.imgur.com/J6baTvU.png "Add Expenses")

1. **Scan Bill**:
   - Upload an image of your invoice or receipt, and ExpenAI will automatically extract and categorize expenses.
   - Supports multiple image formats: PNG, JPEG, WEBP, HEIC, and HEIF.

     ![Image Input](https://i.imgur.com/m340vrV.png "Image Input")

2. **Voice Input**:
   - Record or upload a `.wav` file with a description of your expenses. ExpenAI will convert the speech to text and categorize the expenses accordingly.

3. **Text Input**:
   - Type in a description of your expenses, and ExpenAI will process the text to extract the category and amount.

4. **Dynamic Dashboard**:
   - A real-time dashboard showing a table of transactions with serial numbers, categories, and amounts.
   - A pie chart that visualizes expense distribution across different categories.
   - A line graph that shows the wallet balance over time, updated with each new expense.

     ![Dashboard](https://i.imgur.com/KKgGGvs.png "Dashboard")

     ![Chart](https://i.imgur.com/8sQbjYp.png "Chart")
     

5. **Easy Deployment**:
   - Docker support for easy setup and deployment across various environments.

## Installation

Follow these steps to set up ExpenAI on your local machine:

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.9 or above (if running without Docker).

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/ExpenAI.git
   cd ExpenAI
   ```

2. **Setup Environment Variables**:

   Create a `.env` file in the root directory and add your API keys:

   ```bash
   GOOGLE_API_KEY=your_google_api_key
   AAI_API_KEY=your_assemblyai_api_key
   ```

3. **Build and Run Using Docker Compose**:

   ```bash
   docker-compose up --build
   ```

   This command will build and start both the FastAPI backend and Streamlit frontend.

4. **Access the Application**:

   - FastAPI backend: [http://localhost](http://localhost)
   - Streamlit frontend: [http://localhost:8501](http://localhost:8501)

## Usage

Once the application is running:

1. Go to the Streamlit frontend at [http://localhost:8501](http://localhost:8501).
2. Enter your initial wallet balance.
3. Choose one of the input methods (Scan Bill, Voice Input, Text Input) to add expenses.
4. View your expenses and remaining wallet balance on the dynamic dashboard.

## Contributing

We welcome contributions to improve ExpenAI! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions, feel free to reach out:

- **Email**: devanshkmishraw@gmail.com
- **GitHub**: [devanshkmishra](https://github.com/devanshkmishra)
