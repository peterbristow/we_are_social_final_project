from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template import Context
from django.template.context_processors import csrf
from django.template.loader import get_template

from pages.forms import ContactForm


def get_index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # contact_name = request.POST.get('contact_name', '')
            # contact_email = request.POST.get('contact_email', '')
            # form_content = request.POST.get('content', '')

            # Save to db
            contact_details = form.save()

            # Send email
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_details.contact_name,
                'contact_email': contact_details.contact_email,
                'form_content': contact_details.message,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "We Are Social" + '',
                ['peterjb73@gmail.com'],
                headers={'Reply-To': contact_details.contact_email}
            )
            email.send()

            messages.success(request, "Your email was send successfully.")

            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    context.update(csrf(request))

    return render(request, 'contact.html', context)
