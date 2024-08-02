from django.db import models

class Speaker(models.Model):
    name = models.CharField(max_length=200)
    cat1 = models.CharField(max_length=200)
    cat2 = models.CharField(max_length=200, blank=True, null=True)
    wikiLink = models.URLField(max_length=500, blank=True, null=True)
    rockStar = models.BooleanField(default=False)
    insert_date = models.DateTimeField(auto_now_add=True)
    quotes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Conf(models.Model):
    name = models.CharField(max_length=200)
    youtubeLink = models.URLField(max_length=500)
    youtubeEmbedLink = models.URLField(max_length=500)
    ranking = models.IntegerField(default=3)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, default='Conférence')
    cat1 = models.CharField(max_length=200)
    cat2 = models.CharField(max_length=200, blank=True, null=True)
    tags = models.CharField(max_length=200)
    startTimeCode = models.CharField(max_length=8, default='00:00:00')
    questionsTimeCode = models.CharField(max_length=8, default='00:00:00', blank=True, null=True)
    length = models.CharField(max_length=8, default='00:00:00', blank=True, null=True)
    audioQuality = models.CharField(max_length=50, default='High')
    videoQuality = models.CharField(max_length=50, default='High')
    tnLink = models.URLField(max_length=500, blank=True, null=True, default='https://i.ibb.co/5r6cVCW/confrencesfr-high-resolution-logo.png')
    publishDate = models.DateField()
    insertDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

