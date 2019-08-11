from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import Design_Form
from .canny import mainpart
from login_system.models import Design

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
            # form.save()
            # instance = Design_inp(uploadfile=request.FILES['designr_img'])

            myfile = request.FILES["design_input"]
            design_title = request.POST["design_title"]
            design_desc = request.POST['design_desc']

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
        txt, aaa = mainpart(filename, inurl, outurl)
        print("txt", txt)
        print("aaa", aaa)
        outtext = "out_images\\" + txt
        outimg = "out_images\\" + aaa
        print(outtext)
        print(outimg)
        print(design_title)
        print(design_desc)

        # design_input=myfile,
        lol = Design(design_input=myfile, design_title=design_title, design_desc=design_desc, design_output=outimg,
                     design_output_txt=outtext)
        lol.save()

        messages.success(request, f'File has been uploaded and processed!. Please vist the results tab.')

        return render(request, 'mains/estimate.html', {'form': form, 'title': 'Estimate'})
        #     return HttpResponseRedirect('estimate')
    else:
        form = Design_Form()
    return render(request, 'mains/estimate.html', {'form': form, 'title': 'Estimate'})


@login_required
def results(request):
    data = Design.objects.all()

    stu = {
        "info": data
    }
    return render(request, 'mains/results.html', stu, {'title': 'Results'})
