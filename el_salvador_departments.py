import pdfplumber
import csv
import re

# Path to your PDF file
pdf_file = "/Users/vaamx/Documents/Opscale/01_Poblacion_Total_por_Area_Sexo.pdf.pdf"

# Define the output CSV file
output_csv_file = "/Users/vaamx/Documents/Opscale/el_salvador_population_data.csv"

# Regex patterns to capture department and municipality details
department_pattern = re.compile(r"^\d{2}-(\w.+?)\s+\d{1,3}(?:,\d{3})?")
municipality_pattern = re.compile(r"^(\w.+?)\s+(\d{1,3}(?:,\d{3})?)\s+(\d{1,3}(?:,\d{3})?)\s+(\d{1,3}(?:,\d{3})?)\s+(\d{1,3}(?:,\d{3})?)\s+(\d{1,3}(?:,\d{3})?)\s+(\d{1,3}(?:,\d{3})?)")

# Initialize a list to hold the extracted data
extracted_data = []

# Open the PDF and process it
with pdfplumber.open(pdf_file) as pdf:
    current_department = None
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        
        for line in lines:
            # Check if the line is a department header
            department_match = department_pattern.match(line)
            if department_match:
                current_department = department_match.group(1).strip()
                print(f"Found department: {current_department}")
                continue

            # Check if the line matches a municipality
            municipality_match = municipality_pattern.match(line)
            if municipality_match and current_department:
                municipio = municipality_match.group(1).strip()
                total_population = municipality_match.group(2).replace(",", "")
                urbano = municipality_match.group(4).replace(",", "")
                rural = municipality_match.group(7).replace(",", "")

                # Add the extracted data to the list
                extracted_data.append({
                    "DEPARTAMENTO": current_department,
                    "MUNICIPIO": municipio,
                    "TOTAL": int(total_population),
                    "URBANO": int(urbano),
                    "RURAL": int(rural),
                })
                print(f"Added municipality: {municipio} with total population {total_population}")

# Write the extracted data to a CSV file
with open(output_csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["DEPARTAMENTO", "MUNICIPIO", "TOTAL", "URBANO", "RURAL"])
    writer.writeheader()
    for data in extracted_data:
        writer.writerow(data)

print(f"Data extraction complete. Output saved to {output_csv_file}.")
