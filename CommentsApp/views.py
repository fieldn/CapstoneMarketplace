from django.shortcuts import render
from . import models
from . import forms
import json
from django.http import HttpResponse

# Create your views here.

def getCommentByID(s):
    return models.Comment.objects.get(id=s)

def isInt(s):
    try:
        int(s)
        return True
    except:
        return False

def serialize(c):
    return {
        'id' : c.id,
        'time' : str(c.time),
        'comment' : c.comment,
        'subcomments' : [serialize(getCommentByID(s)) for s in c.subcomments.split(',') if isInt(s)]
    }

def getComments(request):
    comments_list = list(models.Comment.objects.filter(parent=True))
    j = json.dumps({'list' : map(serialize, comments_list)})
    context = {'comments' : j}
    return render(request, 'comments.html', context)

def getCommentForm(request):
    return render(request, 'commentForm.html')

def addComment(request):
    if request.method == 'POST':
        try:
            identifier = int(request.POST.get('id', default=-1))
            comment = request.POST['comment']
            comments_list = list(models.Comment.objects.all())
            parent = next((c for c in comments_list if c.id == identifier), None)
            new_comment = models.Comment(comment=comment, parent=parent==None)
            new_comment.save()
            if parent != None:
				parent.subcomments += ',' + str(new_comment.id)
				parent.save();
            response_data = { 'error' : 'success' }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except KeyError:
            pass
