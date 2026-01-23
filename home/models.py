from django.db import models
import uuid
# Create your models here.
def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    return f"board/{uuid.uuid4()}.{ext}"



class Board(models.Model):
    name = models.CharField(max_length=40, blank=False ,null=False, verbose_name="Name")
    badge = models.CharField(max_length=50, blank=True ,null=True, verbose_name="Badge")  #شارة 
    position = models.CharField(blank=False ,null=False, verbose_name="Position") # position
    image = models.ImageField(upload_to=image_upload, blank=True ,null=True, verbose_name="Image") # image
    description = models.TextField(blank=True ,null=True, verbose_name="Description") # الوصف
    expertise = models.CharField(blank=True ,null=True, verbose_name="Expertise") # الخبرات
    #################
    facebook = models.CharField(blank=True ,null=True, verbose_name="Facebook")
    linkedin = models.CharField(blank=True ,null=True, verbose_name="Linked In")
    x = models.CharField(blank=True ,null=True, verbose_name="X")


    def __str__(self):
        return self.name
    

    def list_expertise(self):
        ls_items = []
        if '|' in self.expertise:
            for i in self.expertise.split("|"):
                ls_items.append(i.strip())
            return ls_items
        return self.expertise
    
    
    def short_description(self, length=200):
        if len(self.description) > length:
            return self.description[:length] + "..."
        return self.description





class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=150, blank=True, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




