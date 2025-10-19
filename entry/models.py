from django.db import models


class DiaryModel(models.Model):
    note = models.CharField(max_length=100)
    content = models.TextField()
    posted_date = models.DateTimeField()
    productivity = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='Diary Image')
    temp_image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='temp_Image')


    def date_for_chart(self):
        return self.posted_date.strftime('%b %e')

    def __str__(self):
        return self.note

    def summary(self):
        if len(self.content) > 100:
            return self.content[:100] + '  ...'
        return self.content[:100]
