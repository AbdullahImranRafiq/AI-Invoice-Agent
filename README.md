# Personal Finance Dashboard

A Streamlit-based application that uses OCR and AI to extract structured invoice data from images and visualize spending patterns.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google AI](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

## 📸 Screenshots

![Invoice Upload](demo.gif)

> *Upload invoices, extract data automatically, and visualize your spending patterns with AI-powered intelligence.*

## ✨ Features

- 📄 **OCR Processing**: Extract text from invoice images using OCR.space API
- 🤖 **AI-Powered Data Extraction**: Use Google's Gemini AI to structure invoice data
- 📊 **Data Visualization**: Automatic categorization and pie chart visualization of expenses
- 📁 **Multiple Invoice Support**: Process multiple invoices at once

## 📋 Prerequisites

- 🐍 Python 3.8+
- 🔑 OCR.space API Key (free tier available at [ocr.space](https://ocr.space/ocrapi))
- 🔑 Google Gemini API Key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Python_Invoice_Agent.git
cd Python_Invoice_Agent
```

2. Install dependencies:

   Using pip:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using uv (faster):
   ```bash
   uv sync
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys to the `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
API_KEY=your_ocr_space_api_key_here
```

## 💻 Usage

1. Run the Streamlit app:
```bash
streamlit run main.py
```

2. Open your browser (usually at `http://localhost:8501`)

3. Upload invoice images (JPG, PNG, JPEG formats supported)

4. Click "Process Invoices" to extract and visualize the data

## 📦 Data Structure

The app extracts the following fields from invoices:
- Invoice Number
- Invoice Date
- Vendor Name
- Currency
- Subtotal
- Total Amount
- Category (auto-categorized)
- Item-level details (Name, Quantity, Unit Price, Line Total)

## 🛠️ Technologies Used

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Google%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google AI"/>
</p>

- **Streamlit**: Web interface
- **OCR.space API**: Optical character recognition
- **Google Gemini AI**: Structured data extraction
- **Pandas**: Data processing
- **Matplotlib**: Data visualization
- **LangChain**: AI integration framework

## 📄 License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! This project is licensed under GPL v3.0, which means:
- You can freely use, modify, and distribute this software
- Any modifications must also be licensed under GPL v3.0
- You must make source code available when distributing the software

## ⚠️ Disclaimer

This software is provided "as is" without warranty of any kind. See the LICENSE file for full details.

---

<div align="center">
  <p>Made with ❤️ using Streamlit and Google Gemini AI</p>
  <p>
    <a href="https://github.com/yourusername/Python_Invoice_Agent/issues">Report Bug</a>
    ·
    <a href="https://github.com/yourusername/Python_Invoice_Agent/issues">Request Feature</a>
  </p>

</div>
