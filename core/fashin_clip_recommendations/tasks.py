from .FashinClip import FashionImageRecommender
from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging
from fashin_clip_recommendations.models import ImageCollection

logger = logging.getLogger(__name__)

# queue parameter you can select the worker 
@shared_task(name='CreateEmbedding', queue='queue_two')
def fashion_clip_embedding(api_key, full_image_path, pk):
    logger.info(f"Task 'CreateEmbedding' started with args: {api_key}, {full_image_path}, {pk}")
    fashion_obj = FashionImageRecommender(collection_name=api_key)
    logger.info
    preprocess = fashion_obj.load_images(full_image_path, id_img=pk)
    
    if preprocess:
        logger.info("Task 'CreateEmbedding' completed successfully")
        return {'status': 'success'}
    else:
        logger.error("Task 'CreateEmbedding' failed to load the image")
        return {'status': 'error', 'message': 'It has a problem with loading the image. Please check the image.'}

@shared_task(name='DeleteEmbedding', queue='queue_two')
def fashion_clip_delete(api_key,pk):
    fashion_obj = FashionImageRecommender(collection_name=api_key)
    preprocess = fashion_obj.Delete_embeded_images(id_img=pk)

    if preprocess:
        return {'status': 'success'}
    else:
        return {'status': 'error', 'message': 'It has a problem with loading the image. Please check the image.'}
     

@shared_task(name='Retrive_image_ids', queue='queue_two')
def fashion_clip_retrieve(collection_name):
    fashion_obj = FashionImageRecommender(collection_name=collection_name)
    id_imgs = fashion_obj.retrive_image()
   
    if id_imgs:
        return {'id_imgs': id_imgs}
    else:
        return {'status': 'error', 'message': 'this is not retrive any image id from chromadb.'}
     


@shared_task(name='Fashion_clip_recommender', queue='queue_two')
def fashion_clip_recommeneder(collection_name, user_description, number_of_images):
    fashion_obj = FashionImageRecommender(collection_name=collection_name)
    recommendations = fashion_obj.recommend_images(user_description, number_of_images)
    if recommendations:
        
        return {"recommendations": recommendations}
    else:
        return {'status': 'error', 'message': 'this is not retrive any image id from chromadb.'}
     