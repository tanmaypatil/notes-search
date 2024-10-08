from concurrent.futures import ThreadPoolExecutor, as_completed
import fitz  # PyMuPDF for PDF handling
import gradio as gr
from PIL import Image
import io
from file_search import search

# pdf upload task
def pdf_to_image_task(pdf_file):
    # check if pdf file is provided
    if not pdf_file:
         raise ValueError("No pdf file provided , please upload the same")
    # Open the PDF from the uploaded file
    doc = fitz.open(pdf_file.name)
    images = []
    
    # Iterate through all the pages and convert them to images
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        # Append the image to the list
        images.append(img)
    return images 

def search_vector_task(prompt):
    # Query vector store 
    store_id = 'vs_Rxi64D4Z3ntBfcJDqrPPhgpP'
    assistant_output = search([store_id],prompt)
    assistant_message = "\n".join(assistant_output)
    
    return assistant_message
    
# Function to convert a page of the PDF into an image
def pdf_to_images(pdf_file,prompt):
    with ThreadPoolExecutor() as executor:
        future_to_task = {
        executor.submit(pdf_to_image_task,pdf_file): "pdf_to_image_task",
        executor.submit(search_vector_task,prompt): "search_vector_task",
        }
        # Wait for both tasks to complete before returning the results
        for future in as_completed(future_to_task):
            task_name = future_to_task[future] 
            result = future.result()  # Retrieve the result of each task
            if ( task_name == 'pdf_to_image_task'):
                images = result
            else :
                assistant_message = result
 
    # Return the images (Gradio will display them)
    return images,assistant_message

# Create the Gradio interface
pdf_input = gr.File(file_types=['.pdf'], label="Upload PDF")
prompt = gr.Textbox(
            label="prompt",
            info="Enter search query",
            lines=3,
            value="what was the work in api governance.",
        )
output_gallery = gr.Gallery(type="pil", label="PDF Pages")
output = gr.Textbox(
            label="result",
            info="output of search",
            lines=3,
            value="output will appear here ",
        )

interface = gr.Interface(
    fn=pdf_to_images,  # Function to process and display the PDF
    inputs=[pdf_input,prompt],  # Input widget to upload the PDF
    outputs=[output_gallery,output],  # Output as images
    title="Resume intelligence",
    description="Upload a PDF file and view its pages as images."
)

# Launch the interface
interface.launch()
