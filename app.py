from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import xml.etree.ElementTree as ET
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import tempfile
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'xml'

def parse_xml_to_dict(xml_file_path):
    """Parse XML file and convert to a structured dictionary"""
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        def element_to_dict(element):
            result = {}
            
            # Add attributes if any
            if element.attrib:
                result['@attributes'] = element.attrib
            
            # Add text content if any (and it's not just whitespace)
            if element.text and element.text.strip():
                if len(list(element)) == 0:  # No child elements
                    return element.text.strip()
                else:
                    result['text'] = element.text.strip()
            
            # Process child elements
            children = {}
            for child in element:
                child_data = element_to_dict(child)
                if child.tag in children:
                    # Handle multiple elements with same tag
                    if not isinstance(children[child.tag], list):
                        children[child.tag] = [children[child.tag]]
                    children[child.tag].append(child_data)
                else:
                    children[child.tag] = child_data
            
            if children:
                result.update(children)
            
            return result if result else None
        
        return {
            'root_element': root.tag,
            'data': element_to_dict(root)
        }
    
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing XML: {str(e)}")

def create_pdf_from_data(data, output_path):
    """Create a PDF from parsed XML data"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkgreen
    )
    
    # Title
    story.append(Paragraph("XML Data Report", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Root element info
    story.append(Paragraph(f"Root Element: {data['root_element']}", heading_style))
    story.append(Spacer(1, 12))
    
    def add_data_to_story(obj, level=0, parent_key=""):
        """Recursively add data to PDF story"""
        indent = "    " * level
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == '@attributes':
                    # Handle attributes
                    story.append(Paragraph(f"{indent}<b>{parent_key} Attributes:</b>", styles['Normal']))
                    for attr_key, attr_value in value.items():
                        story.append(Paragraph(f"{indent}  • {attr_key}: {attr_value}", styles['Normal']))
                elif key == 'text':
                    # Handle text content
                    story.append(Paragraph(f"{indent}<b>Content:</b> {value}", styles['Normal']))
                else:
                    # Handle regular elements
                    if isinstance(value, (list, dict)):
                        story.append(Paragraph(f"{indent}<b>{key}:</b>", styles['Normal']))
                        add_data_to_story(value, level + 1, key)
                    else:
                        story.append(Paragraph(f"{indent}<b>{key}:</b> {value}", styles['Normal']))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                story.append(Paragraph(f"{indent}<b>Item {i + 1}:</b>", styles['Normal']))
                add_data_to_story(item, level + 1, f"{parent_key}[{i}]")
        
        else:
            story.append(Paragraph(f"{indent}{obj}", styles['Normal']))
        
        story.append(Spacer(1, 6))
    
    # Add the main data
    add_data_to_story(data['data'])
    
    # Build PDF
    doc.build(story)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Save uploaded file
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Parse XML
                xml_data = parse_xml_to_dict(filepath)
                
                # Create PDF
                pdf_filename = filename.replace('.xml', '.pdf')
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                create_pdf_from_data(xml_data, pdf_path)
                
                # Clean up XML file
                os.remove(filepath)
                
                flash('File successfully processed!')
                # Store the PDF filename in session for download
                from flask import session
                session['pdf_file'] = pdf_filename
                return redirect(url_for('download_pdf', filename=pdf_filename))
                
            except ValueError as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
            except Exception as e:
                flash(f'Unexpected error: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload an XML file.')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_pdf(filename):
    """Download the generated PDF file"""
    try:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(pdf_path):
            return send_file(pdf_path, as_attachment=True, download_name=filename)
        else:
            flash('File not found or has expired.')
            return redirect(url_for('upload_file'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('upload_file'))

@app.route('/preview/<filename>')
def preview_xml(filename):
    """Preview XML content before generating PDF"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        xml_data = parse_xml_to_dict(filepath)
        return render_template('preview.html', data=xml_data, filename=filename)
    except Exception as e:
        flash(f'Error reading file: {str(e)}')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
