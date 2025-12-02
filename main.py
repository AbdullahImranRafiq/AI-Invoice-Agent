# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import json  # Add this import for parsing JSON
from langchain_google_genai import ChatGoogleGenerativeAI
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import requests
import os
# -------------------------------------
# Environment & App Setup
# -------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OCR_API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="Finance Dashboard", page_icon="💸")
st.title("💵 Personal Finance Dashboard")

uploaded_invoices = st.file_uploader(
    "Upload Invoices",
    accept_multiple_files=True,
    type=["jpg", "png", "jpeg"]
)

# -------------------------------------
# OCR Tool
# -------------------------------------


def ocr_space_file(filename, overlay=False, language="eng"):
    payload = {
        "isOverlayRequired": overlay,
        "apikey": OCR_API_KEY,
        "language": language,
    }

    with open(filename, "rb") as f:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": f},
            data=payload,
        )

    return response.json()

# -------------------------------------
# CSV Conversion Tool
# -------------------------------------


def convert_to_csv(invoice_data: dict):
    """
    Flattens invoice-level + line items into a tabular dataframe
    """
    rows = []

    # Handle cases where Items is None or missing
    items = invoice_data.get("Items")
    if items is None:
        items = [
            {
                "Item_Name": invoice_data.get("Item_Name"),
                "Quantity": invoice_data.get("Quantity"),
                "Unit_Price": invoice_data.get("Unit_Price"),
                "Line_Total": invoice_data.get("Line_Total"),
            }
        ]

    for item in items:
        row = {
            "Invoice_Number": invoice_data.get("Invoice_Number"),
            "Invoice_Date": invoice_data.get("Invoice_Date"),
            "Vendor_Name": invoice_data.get("Vendor_Name"),
            "Currency": invoice_data.get("Currency"),
            "Subtotal": invoice_data.get("Subtotal"),
            "Total_Amount": invoice_data.get("Total_Amount"),
            "Category": invoice_data.get("Category"),
            "Item_Name": item.get("Item_Name"),
            "Quantity": item.get("Quantity"),
            "Unit_Price": item.get("Unit_Price"),
            "Line_Total": item.get("Line_Total"),
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    # Aggregate data by category for the pie chart
    category_data = df.groupby("Category")["Total_Amount"].sum()

    # Plot the pie chart
    st.subheader("Categories")
    pie_chart = plt.figure(dpi=600)
    plt.pie(category_data, labels=category_data.index, autopct="%1.1f%%")
    plt.legend()
    st.pyplot(pie_chart, use_container_width=True)

    return df


root_agent = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", google_api_key=GEMINI_API_KEY)


def process_invoices():
    if not uploaded_invoices:
        st.warning("No invoices uploaded")
        return

    for invoice in uploaded_invoices:
        with open(invoice.name, "wb") as f:
            f.write(invoice.getbuffer())

        ocr_result = ocr_space_file(invoice.name)
        ocr_text = ocr_result.get("ParsedResults", [{}])[
            0].get("ParsedText", "")

        if not ocr_text.strip():
            st.error(f"OCR failed for {invoice.name}")
            continue

        # Pass OCR'd text to the AI model

        structured_data = root_agent.invoke(f"""
You are an Invoice Intelligence Agent operating inside a Personal Finance Dashboard.

TASK
Extract structured invoice data from OCR text.

STRICT RULES
- Use only the following keywords:
- Invoice_Number
- Invoice_Date
- Vendor_Name
- Currency
- Subtotal
- Total_Amount
- Category
- Item_Name
- Quantity
- Unit_Price
- Line_Total
- No tax extraction or inference.
- Do not hallucinate missing values.
- Normalize dates (YYYY-MM-DD).
- Normalize money to numeric only.
- One category per invoice using keyword reasoning.

OUTPUT
Return a structured dict compatible with convert_to_csv. Here is the OCR text: {ocr_text}
""")

        # Extract and parse the JSON content
        if hasattr(structured_data, "content"):
            raw_content = structured_data.content

            # Attempt to clean and parse the content
            cleaned_content = raw_content.strip(
                "`json\n\\`")  # Remove formatting if present
            parsed_data = json.loads(cleaned_content)

            # Ensure parsed_data is a dictionary before passing to convert_to_csv
            if isinstance(parsed_data, dict):
                convert_to_csv(parsed_data)
                st.success(f"Processed {invoice.name}")


# UI Trigger
if st.button("Process Invoices"):
    process_invoices()
