from django.shortcuts import loader
from django.shortcuts import HttpResponse
from .runner_main import app_main


def getReportAttributes(result, result_temp):
    """
    Return report attributes as a list of (name, value).
    Override this to add custom attributes.
    """
    start_time = str(result_temp['startTime'])[:19]
    duration = str(result_temp['stopTime'] - result_temp['startTime'])
    status = []
    if result.success_count:
        status.append('Pass %s' % result.success_count)
    if result.failure_count:
        status.append('Failure %s' % result.failure_count)
    if result.error_count:
        status.append('Error %s' % result.error_count)
    if status:
        status = ' '.join(status)
    else:
        status = 'none'
    return {
        "Start_Time": start_time,
        'Duration': duration,
        'Status': status,
    }


def generateReport(result, result_temp, context):
    context.update(getReportAttributes(result, result_temp))
    # stylesheet = generate_stylesheet()
    #
    # report = generate_report(result)
    # context.update(generate_report(result, result_temp))
    # ending = generate_ending()
    # output = HTML_TMPL % dict(
    #     title=saxutils.escape(self.title),
    #     generator=generator,
    #     stylesheet=stylesheet,
    #     heading=heading,
    #     report=report,
    #     ending=ending,
    # )


# Create your views here.
def index(req):
    t = loader.get_template('testcase_show.html')    # 导入html文件
    # t = Template("My name is {{name}}.")
    # c = Context({"person_name": "Stephane"})

    context = app_main()
    html = t.render(context)

    return HttpResponse(html)
    # return render_to_response('index.html', {"person_name": "Stephane"})
    # return render(req, 'index.html',)
    # return render(req, t.render(context),)
