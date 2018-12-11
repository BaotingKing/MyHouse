from django.shortcuts import loader
from django.shortcuts import HttpResponse
from .runner_main import app_main


# Create your views here.
def index(req):
    t = loader.get_template('testcase_show.html')    # load html file
    # t = Template("My name is {{name}}.")
    # c = Context({"person_name": "Stephane"})

    context = app_main()
    html = t.render(context)

    return HttpResponse(html)
    # return render_to_response('index.html', {"person_name": "Stephane"})
    # return render(req, 'index.html',)
    # return render(req, t.render(context),)
