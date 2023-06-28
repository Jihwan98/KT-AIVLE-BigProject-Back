from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)
        data = form.cleaned_data
        user.first_name = data.get('first_name')
        user.is_vet = data.get("is_vet")
        user.profile_img = data.get("profile_img")
        user.save()
        return user