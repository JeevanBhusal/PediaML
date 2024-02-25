from http.client import HTTPResponse
from django import forms
from django.shortcuts import render ,redirect, HttpResponse
from requests import post
import pyttsx3
from django.shortcuts import redirect
from .models import Postblog
from django.urls import reverse
import googletrans
from blog.code import SentimentAnalyzer
from .models import BlogComment
from .models import Postblog
from django.contrib import messages
from .summer import generate_summary
# from gtts import gTTS
# from gTTS.templatetags.gTTS import say

from googletrans import Translator
from .code import SentimentAnalyzer
# #An empty array called textForTts
# '''def speech(request):
#     if request.method=="POST":
#         lang=request.POST.get("lang")
#         data=request.POST.get("content")
#         obj = say(language=lang, text=data)
#         return HttpResponse({'obj':obj})
#     #return render(request, 'index.html', {'obj':obj})
#     return redirect(f"/blog/{Postblog.slug}")'''

# Create your views here.
def blogHome(request):
    allPosts=Postblog.objects.all()
    
    context={'allPosts':allPosts}
    return render(request,"blog/blogHome.html",context)

def blogPost(request,slug):
    post = Postblog.objects.filter(slug=slug).first()
    comments=BlogComment.objects.filter(post=post)
    context={"post":post,"comments":comments }
    return render(request,"blog/blogPost.html",context)

def postComment(request):
    if request.method=="POST":

        comments=request.POST.get("comments")
        user=request.user
        postSno=request.POST.get("postSno")
        post=Postblog.objects.get(sno=postSno)
        
        comments=BlogComment(comment=comments,user=user,post=post)
    comments.save()
    messages.success(request,"Your comment has been posted successfully")
    return redirect(f"/blog/{post.slug}")

#reference for summerizing a blog 
# def translate_app(request):
#     if request.method=="POST":
#         lang=request.POST.get("lang")
#         data=request.POST.get("content")
#         translator=Translator()
#         tr=translator.translate(data,dest=lang)
#         # return redirect(f"/blog/{Postblog.slug}",{"result":tr.text})
#         return HttpResponse(tr.text)
#     return redirect(f"/blog/{Postblog.slug}")
def summer(request):
    if request.method=="POST":
        data=request.POST.get("content")
        sr=generate_summary(data)
        # return redirect(f"/blog/{Postblog.slug}",{"result":tr.text})
        print(sr)
        return HttpResponse(sr)
    return redirect(f"/blog/{Postblog.slug}")

    '''def SentimentApp(request):
    context = {}
    if request.method == 'POST':
        if form.is_valid():
            sent = form.cleaned_data.get('Sentence')    # got the sentence
            textAns = SentimentAnalyzer(sent)
            context['text'] = textAns
    
    context['comments'] = comments
    return render(request, '{Postblog.slug}', context=context)'''

def sentiment(request):
    if request.method=="POST":
        # sent_data=request.POST.get("comment")
        postSno=request.POST.get("postSno")
        sent_data=BlogComment.objects.filter(post=postSno)
        #see=BlogComment.objects.filter()
        # print(sent_data)
        score = []   
        for i in sent_data:
            score.append(SentimentAnalyzer(i.post.content))
        
        # print(sent_req)
        if (sum(score)/len(score))>0.7:
            return HttpResponse('Sentiment is:  Positive')
        else:
            return HttpResponse('Sentiment is:  Negative')
    return redirect(f"/blog/{Postblog.slug}")


# checking using pyttx modoule

# def translate_text(request):
#             if request.method == "POST":
#                 lang = request.POST.get("lang")
#                 data = request.POST.get("content")
#                 translator = googletrans.Translator()
#                 translated_text = translator.translate(data, dest=lang)
#             return translated_text.text
def translate_text(text, target_lang):
    translator = googletrans.Translator()
    translated_text = translator.translate(text, dest=target_lang)
    return translated_text.text


def translate_app(request):
    if request.method == "POST":
        lang = request.POST.get("lang")
        data = request.POST.get("content")

        

        # Translate text to the desired language (if needed)
        # You can add translation code here if required
        # translated_text = data
        translated_text = translate_text(data,lang)

        # Initialize the text-to-speech engine within the view function
        engine = pyttsx3.init()
        # set lanaguauge
        engine.setProperty('voice', f'{lang}')

        # Set properties (optional)
        # engine.setProperty('rate', 150)  # Speed of speech
        # engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

        # Set language (if needed)
        # engine.setProperty('language', lang)

        # Say the translated text
        try:
            engine.say(translated_text)

            # Wait for speech to finish
            engine.runAndWait()
        except RuntimeError as e:
            if str(e) == 'run loop already started':
                engine.stop()
                engine.runAndWait()
            else:
                raise e

        # Redirect back to the original page (you may want to modify this)
        # return redirect(reverse('blog', kwargs={'slug': Postblog.slug}))
        # return redirect(f"/blog/{Postblog.slug}")
            print(translated_text)
        return HttpResponse("this is translated data/n" + translated_text)
        # return redirect("./templates/home/home.html")

    # return HttpResponse("This endpoint only supports POST requests.")
    return redirect(f"/blog/{Postblog.slug}")

