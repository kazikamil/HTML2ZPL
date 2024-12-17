from flask import Flask, request
from lxml import etree
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

# Charger le fichier XSLT
xslt_doc_str = '''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text"/>

    <!-- Template to match the root element -->
    <xsl:template match="/">
        ^XA
        
        <xsl:apply-templates/>
        
        ^XZ
    </xsl:template>
    
    <!-- Template to match the div with title 'barcode' -->
    <xsl:template match="div[@title='barcode']">
        <xsl:text>^FO</xsl:text><xsl:value-of select="@data-x"/>
        <xsl:text>,</xsl:text><xsl:value-of select="@data-y"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>^BY</xsl:text><xsl:value-of select="@data-width"/><xsl:text>,2</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:value-of select="@data-command"/><xsl:value-of select="@data-height"/><xsl:text>,Y,N</xsl:text>
        <xsl:text>^FD</xsl:text>
        <xsl:value-of select="@data-content"/>
        <xsl:text>^FS</xsl:text>
        <xsl:text>&#10;</xsl:text>
    </xsl:template>

    <!-- Template to match the div with title 'qrcode' -->
    <xsl:template match="div[@title='qrcode']">
        <xsl:text>^FO</xsl:text><xsl:value-of select="@data-x"/>
        <xsl:text>,</xsl:text><xsl:value-of select="@data-y"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>^BQN,</xsl:text><xsl:value-of select="@data-width"/><xsl:text>,</xsl:text><xsl:value-of select="@data-height"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>^FDQA,</xsl:text>
        <xsl:value-of select="@data-content"/>
        <xsl:text>^FS</xsl:text>
        <xsl:text>&#10;</xsl:text>
    </xsl:template>
    <xsl:template match="div[@title='dataMatrix']">
        <xsl:text>^FO</xsl:text><xsl:value-of select="@data-x"/>
        <xsl:text>,</xsl:text><xsl:value-of select="@data-y"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>^BXN,</xsl:text><xsl:value-of select="@data-height"/><xsl:text>,200</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>^FD</xsl:text>
        <xsl:value-of select="@data-content"/>
        <xsl:text>^FS</xsl:text>
        <xsl:text>&#10;</xsl:text>
    </xsl:template>
    <xsl:template match="div[@title='img']">
        <xsl:text>^FO</xsl:text><xsl:value-of select="@data-x"/>
        <xsl:text>,</xsl:text><xsl:value-of select="@data-y"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:value-of select="@data-content"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>^FS</xsl:text>
        <xsl:text>&#10;</xsl:text>
    </xsl:template>
     <xsl:template match="div[@title='text']">
        <xsl:text>^FO</xsl:text><xsl:value-of select="@data-x"/>
        <xsl:text>,</xsl:text><xsl:value-of select="@data-y"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:value-of select="@data-font"/><xsl:value-of select="@data-height"/><xsl:text>,</xsl:text><xsl:value-of select="@data-width"/>
        <xsl:text>^FD</xsl:text><xsl:value-of select="@data-content"/><xsl:text>^FS</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>^FS</xsl:text>
        <xsl:text>&#10;</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>
'''

# Convertir la chaîne XSLT en bytes
xslt_doc_bytes = xslt_doc_str.encode('utf-8')
xslt_doc = etree.fromstring(xslt_doc_bytes)
print(xslt_doc)
transform = etree.XSLT(xslt_doc)

@app.route('/transform', methods=['POST'])
def transform_xml():
    try:
        # Récupérer le document XML envoyé en POST
        xml_doc_str = request.data.decode('utf-8')
        
        # Convertir la chaîne XML en objet XML
        xml_doc = etree.fromstring(xml_doc_str)
        
        # Appliquer la transformation
        result_doc = transform(xml_doc)
        
        # Retourner le résultat en réponse
        return str(result_doc), 200
    except Exception as e:
        print(e)
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
