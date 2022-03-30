from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from datetime import date
from pathlib import Path
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from .forms import NewUserForm
from .forms import UploadFileForm
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, NewUserForm
from .models import Report
from .convert_image import read_nifti_file,normalize,resize_volume,process_scan
from scipy import ndimage
import os
import numpy as np
import nibabel as nib
import tensorflow as tf
import matplotlib.pyplot as plt
from pathlib import Path
plt.switch_backend('Agg')
BASE_DIR = Path(__file__).resolve().parent.parent
model = tf.keras.models.load_model(f"{BASE_DIR}/src/Model")

# Done
def get_predicted_text(prediction):
    if prediction == 0:
        predicted_text = "As per the CT SCAN uploaded, There are a large number of lessions present in your lungs . The amount of lessions are above 75%. It is the highest stage .Please  consult a doctor immediately And stay under medical supervision.Consider being hospitalized immediately. Any late in gaining medical attention would be fatal"
    elif prediction == 1:
        predicted_text = "As per the CT SCAN uploaded, there are no lessions present in your lungs, if you still feel symptoms please contact  your doctor"
    elif prediction == 2:
        predicted_text = "As per the CT SCAN uploaded, There are lessions present in your lungs but the amount of lessions are below 25%. It is the lowest stage and please consult a doctor for further diagnosis."
    elif prediction == 3:
        predicted_text = "As per the CT SCAN uploaded, There are lessions present in your lungs but the amount of lessions are  from 25% to 50%. It is an intermediate stage .Please  consult a doctor immediately."
    else:
        predicted_text = "As per the CT SCAN uploaded, There are a large number of lessions present in your lungs . The amount of lessions are from 50% to 75%. It is a very high stage .Please  consult a doctor immediately."
    return predicted_text  

# Done
@login_required(login_url='/login_gui')
def scan(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        name = request.POST['name'].strip()
        age = request.POST['age']
        gender = request.POST['gender']
        if form.is_valid():
            cleaned_data = form.cleaned_data['file']
            file_name = request.FILES['file'].name
            date_today = date.today()
            filename_splitted = file_name.split('.', 1)
            file_name_without_extension = filename_splitted[0]
            uploaded_image_data = Report(image=cleaned_data, name=name,
                              age=age, filename=f"{file_name_without_extension}.png", date=date_today.strftime("%Y-%m-%d"), user=request.user, gender=gender)
            uploaded_image_data.save()
            print("FIle Data ="+uploaded_image_data.filename)
            print(BASE_DIR)
            file_path = f"{BASE_DIR}/MEDIABIN/media/{file_name}"
            mask_path = f'{BASE_DIR}/src/static/media/masks/study_0255_mask.nii.gz'
            rows = 5
            cols = 6
            img_count = 0
            fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(15, 15))
            ct_scan = nib.load(file_path).get_fdata()
            mask = nib.load(mask_path).get_fdata()
            for i in range(rows):
                for j in range(cols):
                    axes[i, j].imshow(ct_scan[:, :, img_count])
                    axes[i, j].imshow(mask[:, :, img_count], alpha=0.4)
                    img_count += 1
            fig.savefig(f'{BASE_DIR}/src/static/media/png/{file_name_without_extension}.png')
            processed_image = process_scan(file_path)
            processed_image = np.expand_dims(processed_image, axis=0)
            image_to_predict = np.vstack([processed_image])
            predictions = model.predict(image_to_predict)
            prediction = np.where(predictions[0] == max(predictions[0]))
            prediction = prediction[0][0]
            predicted_text = get_predicted_text(prediction)
            os.remove(file_path)
            return render(request, "scan_results.html", {"predicted_text": predicted_text, 'file': file_name_without_extension})
        else:
            return redirect("scan")
    else:
        form = UploadFileForm()
        return render(request, "scan_form.html", {'form': form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
        return redirect("/")

def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username').strip()
            password = request.POST.get('password').strip()

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect("/login_gui?error=username")
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return redirect('/')


def register_login_form(request):
    # form = AuthenticationForm()
    form = NewUserForm()
    try:
        error = request.GET["error"]
        return render(request=request, template_name="register-login-form.html", context={"login_form": form,"error":"username"})
    except:
        return render(request=request, template_name="register-login-form.html", context={"login_form": form})
# Done
@login_required(login_url="/login_url")
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


# Done
def landing(request):
    return render(request, "landing.html")

# Done
@login_required(login_url='/login_gui')
def account_reports(request):
    if(request.method == "GET"):
        return render(request, 'account_reports.html', {'data': Report.objects.filter(user=request.user)})
    else:
        patient_name = request.POST["name"]
        return render(request, 'account_reports.html', {'data': Report.objects.filter(user=request.user,name=patient_name)})


# Done
@login_required(login_url='/login_gui')
def account_info(request):
    return render(request,'account_info.html',{'user_info':request.user})

# Done
def about_us(request):
    return render(request, 'about_us.html')


def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)

