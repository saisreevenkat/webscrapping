import PyPDF2
import csv
import py

def extract_text_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    num_pages = len(pdf_reader.pages)
    text = ''
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        text += page_obj.extract_text()
    pdf_file_obj.close()
    return text

def extract_articles(text):
    articles = text.split('\n\n')
    return articles

def write_to_csv(articles, csv_file_path):
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["s_no", "article_title", "article_body"])
        for i, article in enumerate(articles, start=1):
            lines = article.split('\n')
            title = lines[0]
            body = '\n'.join(lines[1:])
            writer.writerow([i, title, body])


def main():
    file_path = 'c:/Users/lenov/Downloads/VisionIAS Monthly Current Affairs January 2024 January 2024.pdf'
    csv_file_path = "c:/Users/lenov/Downloads.csv"

    # Extract text from PDF
    text = extract_text_from_pdf(file_path)

    # Assuming each page contains a separate article
    articles = []
    for i, page_text in enumerate(text):
        # Simple heuristic to split title and body
        lines = page_text.split('\n')
        title = lines[0]
        body = '\n'.join(lines[1:])
        articles.append({'title': title, 'body': body})

    # Save articles to CSV
    write_to_csv(articles, csv_file_path)

print(main)