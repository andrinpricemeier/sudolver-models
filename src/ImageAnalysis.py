import boto3
import os

class ImageAnalysis():
    def analyze(self, image_bytes):
        try:
            client = boto3.client('textract')
            return (True, client.analyze_document(Document={'Bytes': image_bytes}, FeatureTypes=['TABLES']))
        except Exception as ex:
            return (False, ex)