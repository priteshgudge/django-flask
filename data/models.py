import sys

try:
    from django.db import models
    #from django.utils import timezone
except  Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Sample User model
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    
    class Meta:
    	app_label= 'data'
    	
    def __unicode__(self):
    	return u'%d: %s' %(self.id,self.name)
    def __str__(self):
    	return self.__unicode__();

class Task(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	done = models.BooleanField()
	
	def as_dict(self):
		if not self.uri:
			self.uri = ""
		return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "uri": self.uri 
        	}
	
	def __unicode__(self):
		return u'%d: %s' %(self.id,self.title)
	def __str__(self):
		return self.__unicode__();
