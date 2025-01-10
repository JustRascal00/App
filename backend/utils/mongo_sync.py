from pymongo import MongoClient
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from blog.models import Blog, Comment, Category, Tag, Menu
from users.models import CustomUser

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]

def sync_to_mongo(instance, collection_name, delete=False):
    collection = db[collection_name]
    
    if delete:
        collection.delete_one({'_id': instance.id})
        return
    
    data = {
        '_id': instance.id,
        **{
            field.name: getattr(instance, field.name)
            for field in instance._meta.fields
            if field.name != 'password'
        }
    }
    
    collection.replace_one(
        {'_id': instance.id},
        data,
        upsert=True
    )

@receiver(post_save, sender=Blog)
def sync_blog(sender, instance, **kwargs):
    sync_to_mongo(instance, 'blogs')

@receiver(post_save, sender=Comment)
def sync_comment(sender, instance, **kwargs):
    sync_to_mongo(instance, 'comments')

@receiver(post_save, sender=Category)
def sync_category(sender, instance, **kwargs):
    sync_to_mongo(instance, 'categories')

@receiver(post_save, sender=Tag)
def sync_tag(sender, instance, **kwargs):
    sync_to_mongo(instance, 'tags')

@receiver(post_save, sender=Menu)
def sync_menu(sender, instance, **kwargs):
    sync_to_mongo(instance, 'menus')

@receiver(post_save, sender=CustomUser)
def sync_user(sender, instance, **kwargs):
    sync_to_mongo(instance, 'users')