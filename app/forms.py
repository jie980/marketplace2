from django import forms

class loginForm(forms.Form):
    username = forms.CharField(min_length=3,
                               error_messages={"min_length": "length of username should >=3",
                                               "required": "Username cannot be empty"}
                               )
    password = forms.CharField(min_length=6,
                               error_messages={"min_length": "length of password should >=6",
                                               "required": "password cannot be empty"}
                               )


class registerForm(forms.Form):
    username = forms.CharField(min_length=3,
                               error_messages={"min_length": "length of username should >=3",
                                               "required": "Username cannot be empty"}
                               )

    email = forms.EmailField(required=True,
                             error_messages={'required': "email cannot be empty",
                                             'invalid': 'emailform invalid '}
                             )

    password = forms.CharField(min_length=6,
                               error_messages={"min_length": "length of password should >=6",
                                               "required": "password cannot be empty"}
                               )
    password_repeat = forms.CharField(min_length=6,
                                      error_messages={"min_length": "length of password should >=6",
                                                      "required": "password cannot be empty"}
                                      )

    def clean(self):
        cleaned_data = super(registerForm, self).clean()
        passwd = cleaned_data.get('password')
        passwd_repeat = cleaned_data.get('password_repeat')

        if passwd != passwd_repeat:
            self.add_error('password_repeat', 'Passwords do not match')
        return cleaned_data


class sellForm(forms.Form):
    pName = forms.CharField(error_messages={"required": "Product name cannot be empty"})
    pDescription = forms.CharField(required=False)
    pPicture = forms.FileField(required=False)
    pPrice = forms.DecimalField(max_digits=7, decimal_places=2, min_value=0,
                                error_messages={'required': "price cannot be empty"})
    pInventory = forms.IntegerField(min_value=0, error_messages={'required': "#inventory cannot be empty"})

    def clean(self):
        cleaned_data = super(sellForm, self).clean()
        return cleaned_data


class checkoutForm(forms.Form):
    firstname = forms.CharField(error_messages={"required": "First name cannot be empty"})
    lastname = forms.CharField(error_messages={"required": "Last name cannot be empty"})
    companyname = forms.CharField(required=False)
    country = forms.CharField(error_messages={"required": "Country cannot be empty"})
    address = forms.CharField(error_messages={"required": "Address cannot be empty"})
    city = forms.CharField(error_messages={"required": "City cannot be empty"})
    zipcode = forms.CharField(error_messages={"required": "Zipcode cannot be empty"})
    phone = forms.CharField(error_messages={"required": "phone number cannot be empty"})
    comment = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(checkoutForm, self).clean()
        return cleaned_data
