

from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging
from customized_RAG.models import Product 
from customized_RAG.ColivaraRAG import ColivaraRAG
logger = logging.getLogger(__name__)

# queue parameter you can select the worker 
@shared_task(name='Processsing_docs', queue='queue_one')
def process_doc_rag(api_key, full_doc_path, pk):
    logger.info(f"Processing one Doc is started with args: {api_key}, {full_doc_path}, {pk}")
    RAG_obj = ColivaraRAG(collection_name=api_key)
    logger.info
    preprocess = RAG_obj.sync_document(full_doc_path, pk)
    
    if preprocess:
        logger.info("Precessing Doc completed successfully with this details:" + str(preprocess))
        return {'status': 'success'}
    else:
        logger.error("Processing Doc is failed ")
        return {'status': 'error', 'message': 'It has a problem with loading the Doc. Please check the Doc.'}

@shared_task(name='Delete_doc', queue='queue_one')
def delete_doc_rag (api_key,pk):
    RAG_obj = ColivaraRAG(collection_name=api_key)
    preprocess = RAG_obj.delete_document(pk)
    if preprocess:
        return {'status': 'success'}
    else:
        return {'status': 'error', 'message': 'It has a problem with loading the text '}
     

