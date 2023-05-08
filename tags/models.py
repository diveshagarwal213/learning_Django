from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Custom Manager
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, Obj_id):
        selectedTable_id = ContentType.objects.get_for_model(obj_type)
        querySet = TaggedItem.objects.select_related("tag").filter(
            content_type=selectedTable_id, object_id=Obj_id
        )
        return querySet


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


# Custom Manager Steps
# 1 => create a class inherited (models.Manager)
# 2 => Define your Custom method (ex. -> get_tags_for)
# 3 => add you class to main class using objects (objects = TaggedItemManager())
# 4 => now you can call like "TaggedItem.objects.get_tags_for(parameters)"
