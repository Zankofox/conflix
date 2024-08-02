import random
import locale
from django.shortcuts import render, get_object_or_404
from .models import Conf, Speaker
from django.db.models import Count, Q


def home(request):
    confs_new = Conf.objects.all()

    # Calculate total number of Conf objects
    total_confs = Conf.objects.count()

    # Prepare tags for the new confs
    tags = set()
    for conf in confs_new:
        if conf.tags:
            tags.update(tag.strip() for tag in conf.tags.split(','))

    # Add tag_list attribute to confs_new
    for conf in confs_new:
        conf.tag_list = [tag.strip() for tag in conf.tags.split(',')] if conf.tags else []

    # Get the latest 10 Conf objects
    confs_new = confs_new.order_by('-publishDate')[:10]

    # Prepare tags for the latest confs
    tags = set()
    for conf in confs_new:
        if conf.tags:
            tags.update(tag.strip() for tag in conf.tags.split(','))

    # Add tag_list attribute to confs_new
    for conf in confs_new:
        conf.tag_list = [tag.strip() for tag in conf.tags.split(',')] if conf.tags else []

    # Retrieve banger Conf objects
    confs_banger = Conf.objects.filter(ranking=3).order_by('?')[:10]

    # Prepare tags for banger confs
    tags = set()
    for conf in confs_banger:
        if conf.tags:
            tags.update(tag.strip() for tag in conf.tags.split(','))

    # Add tag_list attribute to confs_banger
    for conf in confs_banger:
        conf.tag_list = [tag.strip() for tag in conf.tags.split(',')] if conf.tags else []

    # Prepare context
    context = {
        "confs_new": confs_new,
        "confs_banger": confs_banger,
        "total_confs": total_confs  # Add total count to context
    }

    return render(request, "home.html", context)

def all_videos(request):
    confs = Conf.objects.all()

    # Filter speakers who are associated with at least one conference
    speaker_ids_with_confs = confs.values_list('speaker_id', flat=True).distinct()
    speakers = Speaker.objects.filter(id__in=speaker_ids_with_confs).order_by('name')

    # Extract unique categories from cat1 and cat2
    categories = set()
    for conf in confs:
        if conf.cat1:
            categories.add(conf.cat1)
        if (str(conf.cat2) != 'None') & (str(conf.cat2) != 'nan'):
            categories.add(conf.cat2)

    # Extract unique tags from the tags attribute
    tags = set()
    for conf in confs:
        if conf.tags:
            tags.update(tag.strip() for tag in conf.tags.split(','))

    for conf in confs:
        conf.tag_list = [tag.strip() for tag in conf.tags.split(',')] if conf.tags else []

    selected_speaker = request.GET.get('speaker')
    selected_category = request.GET.get('category')
    selected_tag = request.GET.get('tag')

    if selected_speaker:
        confs = confs.filter(speaker_id=selected_speaker)
    if selected_category:
        confs = confs.filter(Q(cat1=selected_category) | Q(cat2=selected_category))
    if selected_tag:
        confs = confs.filter(Q(tags__icontains=selected_tag))

    context = {
        'confs': confs,
        'speakers': speakers,
        'categories': sorted(categories),
        'tags': sorted(tags),
        'selected_speaker': selected_speaker,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
    }
    return render(request, 'all_videos.html', context)

def themes(request):
    themes = [
        'Art',
        'Astrophysique',
        'Biologie',
        'Chimie',
        'Ecologie',
        'Economie',
        'Géologie',
        'Informatique',
        'Linguistique',
        'Mathématiques',
        'Musique',
        'Neurosciences',
        'Philosophie',
        'Physique',
        'Politique',
        'Psychologie',
        'Sociologie',
        'Zététique'
    ]

    # Prepare a list to store theme and count tuples
    theme_counts = []

    for theme in themes:
        count = Conf.objects.filter(Q(cat1=theme) | Q(cat2=theme)).count()
        theme_counts.append((theme, count))

    context = {
        'theme_counts': theme_counts
    }

    return render(request, 'themes.html', context)

def theme(request, theme):
    # Filter conferences by category (cat1 or cat2)
    conferences = Conf.objects.filter(Q(cat1=theme) | Q(cat2=theme))

    # Group conferences by speaker
    speakers = Speaker.objects.filter(conf__in=conferences).distinct()

    for conf in conferences:
        conf.split_tags = conf.tags.split(',')
    context = {
        'theme': theme,
        'speakers': speakers,
        'conferences': conferences
    }

    return render(request, 'theme.html', context)

def tags(request):
    confs = Conf.objects.all()

    # Initialize an empty dictionary to store unique tags and their counts
    tag_counts = {}

    # Iterate through all the Conf objects and split the tags attribute
    for conf in confs:
        if conf.tags:  # Ensure that the tags attribute is not empty
            tags_list = conf.tags.split(',')
            for tag in tags_list:
                tag = tag.strip()  # Strip any whitespace
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1

    # Set the locale to French (you can adjust this to your desired locale)
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

    # Sort tags alphabetically regardless of capitalization and accents
    tags = sorted(tag_counts.items(), key=lambda x: locale.strxfrm(x[0].lower()))
    return render(request, 'tags.html', {"tags": tags})

def tag(request, tag):

    tag_input = tag.strip()
    conferences = Conf.objects.filter(tags__icontains=tag_input)

    speakers = Speaker.objects.filter(conf__in=conferences).distinct()

    for conf in conferences:
        conf.split_tags = conf.tags.split(',')

    context = {
        'tag': tag,
        'speakers': speakers,
        'conferences': conferences
    }

    return render(request, 'tag.html', context)


def speaker(request, speaker_id):
    # Filter conferences by speaker
    speaker = get_object_or_404(Speaker, id=speaker_id)

    # Filter conferences by the speaker
    confs = Conf.objects.filter(speaker=speaker)

    for conf in confs:
        conf.split_tags = conf.tags.split(',')

    context = {
        'speaker': speaker,
        'confs': confs
    }

    return render(request, 'speaker.html', context)

def conf(request, conf_id):
    conf = get_object_or_404(Conf, pk=conf_id)
    conf.split_tags = conf.tags.split(',')
    return render(request, 'conf.html', {"conf" : conf})


def rockstar(request):
    speakers = Speaker.objects.order_by('?')

    for speaker in speakers:
        if speaker.quotes:
            quotes_list = speaker.quotes.split('|')
            speaker.random_quote = random.choice(quotes_list)
        else:
            speaker.random_quote = ""

    return render(request, 'rockstar.html', {"speakers": speakers})

def aboutus(request):
    return render(request, 'aboutus.html')
