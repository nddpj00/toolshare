# from django.shortcuts import render, redirect
# from .forms import NewsletterSubscriptionForm
# from .models import Newsletter
# from django.contrib import messages



# def newsletter_form(request):
#     if request.method == 'POST':
#         form = NewsletterSubscriptionForm(request.POST, request.FILES)

#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             print(email)
#             if Newsletter.objects.filter(email=email).exists():
#                 messages.error(request, "The email address is already subscribed to the newsletter.")
#                 print("email exists")
#             else:
#                 if request.user.is_authenticated:
#                     form.instance.is_registered_already = request.user
#                     form.save()
#                     messages.success(request, "Thank you. We'll send you a weekly newsletter, keeping you up-to-date with Share Bear.")
#                 else:
#                     form.save()
#                     messages.success(request, "Thank you. We'll send you a weekly newsletter, keeping you up-to-date with Share Bear."  )
#         else:
#             print("something else")
#             messages.error(request, "Invalid form data. Please try again.")
#     else:
#         newsletter_form = NewsletterSubscriptionForm()
        
#     template = 'newsletter.html'
#     context = {
#     'form': form,
#     }
        

#     return render(request, template, context)

