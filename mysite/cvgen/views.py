from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


def accept(request):
    if request.method == 'POST':
        print("*******************", request.POST)
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        phone = request.POST.get('phone', "")
        summary = request.POST.get('summary', "")
        school = request.POST.get('school', "")
        university = request.POST.get('university', "")
        previous_work = request.POST.get('previous_work', "")
        skills = request.POST.get('skills', "")

        profile = Profile(name=name, email=email, phone=phone,
                          summary=summary, school=school,
                          university=university, previous_work=previous_work,
                          skills=skills)
        profile.save()

    return render(request, 'cvgen/profile_form.html')


def view_cv(request, id):
    user_profile = Profile.objects.get(pk=id)

    return render(request, 'cvgen/cv.html',
                  {'user_profile': user_profile})


def cv(request, id):
    user_profile = Profile.objects.get(pk=id)

    template = loader.get_template('cvgen/cv.html')
    html = template.render({'user_profile': user_profile})

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8'
    }
    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + user_profile.name + '_cv.pdf'

    return response


def list(request):
    profile_objects = Profile.objects.all()
    return render(request, 'cvgen/list.html',
                  {'profile_objects': profile_objects})
