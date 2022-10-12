from django import forms

CATEGORIES = [
    ('EL', 'Electronic'),
    ('CA', 'Car'),
    ('FO', 'Food'),
    ('SP', 'Sport'),
    ('SA', 'Smartphones'),
    ('CL', 'Clothes'),
]


class CreateListing(forms.Form):
    title = forms.CharField(label="", required=True,
                            widget=forms.Textarea
                            (attrs={"placeholder": "Title",  "style": "margin-top:20px;height:4rem;"}))

    description = forms.CharField(label="", required=True,max_length=500,
                                  widget=forms.Textarea
                                  (attrs={"placeholder": "Description", "style": "margin-top:2px;height:10rem"}))

    price = forms.DecimalField(label="Starting Price: ", required=True, decimal_places=2, max_value=10000, min_value=0.1,
                               widget=forms.NumberInput
                               (attrs={"placeholder": "0.00", "style": "margin-top:2px;height:2rem"}))

    #image = forms.ImageField(label="Image", required=False)

    img_url = forms.URLField(label="Image Url:", required=False)

    category = forms.ChoiceField(label="Category", required=True, choices=CATEGORIES)


