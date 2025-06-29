# XML to PDF Converter

Una aplicación web Flask que convierte archivos XML en documentos PDF con formato profesional.

## 🚀 Características

- **Conversión XML a PDF**: Convierte cualquier archivo XML en un documento PDF estructurado
- **Interfaz web intuitiva**: Subida de archivos mediante drag & drop
- **Procesamiento inteligente**: Parsea automáticamente la estructura XML y la convierte en contenido legible
- **Formato profesional**: PDFs con estilos personalizados, colores y estructura organizada
- **Gestión de archivos**: Limpieza automática de archivos temporales
- **Vista previa**: Opción para previsualizar el contenido XML antes de generar el PDF
- **Descarga directa**: Descarga inmediata del archivo PDF generado

## 📋 Requisitos

- Python 3.7+
- Flask
- ReportLab
- Werkzeug

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/lorenzo-perez/xml-to-pdf.git
cd xml-to-pdf
```

2. **Crear un entorno virtual** (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
python app.py
```

5. **Abrir en el navegador**
```
http://localhost:5000
```

## 📁 Estructura del proyecto

```
xml-to-pdf/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias de Python
├── templates/          # Templates HTML
│   ├── upload.html     # Página de subida de archivos
│   └── preview.html    # Página de vista previa
├── uploads/            # Directorio temporal para archivos
└── README.md          # Este archivo
```

## 🎯 Uso

1. **Acceder a la aplicación** en tu navegador
2. **Seleccionar un archivo XML** usando el botón de carga o arrastrando el archivo
3. **Hacer clic en "Convertir"** para procesar el archivo
4. **Descargar el PDF** generado automáticamente

### Formatos XML compatibles

La aplicación puede procesar cualquier archivo XML válido, incluyendo:
- Documentos XML simples
- XML con atributos
- XML con estructura anidada
- XML con elementos repetidos

## 📊 Características del PDF generado

- **Encabezado**: Título del reporte y fecha de generación
- **Información del elemento raíz**: Nombre del elemento principal
- **Estructura jerárquica**: Contenido organizado respetando la jerarquía XML
- **Atributos destacados**: Los atributos XML se muestran de forma diferenciada
- **Formato profesional**: Colores, fuentes y espaciado optimizados

## ⚙️ Configuración

### Variables de entorno

```bash
PORT=5000                    # Puerto de la aplicación (opcional)
FLASK_ENV=development        # Entorno de Flask
```

### Configuración en app.py

```python
app.secret_key = 'your-secret-key-here'  # Cambiar en producción
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Tamaño máximo: 16MB
```

## 🐳 Docker (Opcional)

Para ejecutar con Docker:

```bash
# Construir la imagen
docker build -t xml-to-pdf .

# Ejecutar el contenedor
docker run -p 5000:5000 xml-to-pdf
```

## 🔧 Desarrollo

### Estructura del código

- **`parse_xml_to_dict()`**: Convierte XML a diccionario Python
- **`create_pdf_from_data()`**: Genera PDF desde datos estructurados
- **`allowed_file()`**: Valida tipos de archivo permitidos
- **Rutas Flask**: Manejo de subida, procesamiento y descarga

### Agregar nuevas características

1. **Nuevos formatos de salida**: Modificar `create_pdf_from_data()`
2. **Estilos personalizados**: Editar los estilos en ReportLab
3. **Validaciones adicionales**: Extender `allowed_file()`

## 🚨 Limitaciones

- Tamaño máximo de archivo: 16MB
- Solo acepta archivos XML válidos
- Los archivos se procesan de forma síncrona

## 🐛 Solución de problemas

### Error: "Invalid XML format"
- Verificar que el archivo XML esté bien formado
- Comprobar que no falten etiquetas de cierre

### Error: "File not found"
- Los archivos se eliminan después del procesamiento
- Descargar el PDF inmediatamente después de la conversión

### Error de memoria
- Reducir el tamaño del archivo XML
- Verificar disponibilidad de memoria en el servidor

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Lorenzo Pérez**
- GitHub: [@lorenzo-perez](https://github.com/lorenzo-perez)

## 🙏 Agradecimientos

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [ReportLab](https://www.reportlab.com/) - Generación de PDFs
- [Python](https://python.org/) - Lenguaje de programación

---

⭐ ¡Dale una estrella al proyecto si te resultó útil!
