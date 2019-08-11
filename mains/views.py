from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import Design_Form
from .canny import mainpart

# Create your views here.


def home(request):
    return render(request, 'mains/home.html')


def about(request):
    return render(request, 'mains/about.html', {'title': 'About'})


@login_required
def estimate(request):
    if (request.method == 'POST'):
        form = Design_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # instance = Design_inp(uploadfile=request.FILES['designr_img'])

            myfile = request.FILES["design_input"]
            print(myfile)
            filename = myfile.name
            inurl = "media\\inp_images\\"
            outurl = "media\\out_images\\"
        #     url = os.path.join(PROJECT_ROOT, ur)
            print(inurl)
            print(filename)
        #     image = cv2.imread(
        #         "media\\images\\as.png")
        #     print("ASAAA")
        #     print(image)
            mainpart(filename, inurl, outurl)
        #     return HttpResponseRedirect('estimate')
    else:
        form = Design_Form()
    return render(request, 'mains/estimate.html', {'form': form}, {'title': 'Estimate'})
