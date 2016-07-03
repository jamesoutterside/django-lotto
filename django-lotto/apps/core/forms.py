from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

import logging

logger = logging.getLogger(__name__)

BALL_KEY = 'ball_'

class EntryForm(forms.Form):
    """
        Standard form for entry, model fields handled via view.
    """
    def __init__(self, *args, **kwargs):
        number_of_balls = kwargs.pop('number_of_balls',None)
        min_ball = kwargs.pop('min_ball',None)
        max_ball = kwargs.pop('max_ball',None)

        if not number_of_balls and not min_ball and not max_ball:
            logger.error('Form must contain ball settings')
            raise forms.ValidationError("Form must contain ball settings")

        super(EntryForm, self).__init__(*args, **kwargs)

        # create a field for each ball
        for i in range(number_of_balls):
            ball = i+1

            # create a field for this ball, with relevant validators
            self.fields['%s%s' % (BALL_KEY,ball)] = forms.IntegerField(label='Ball %s' % ball,
                                                               validators=[MaxValueValidator(max_ball),
                                                                           MinValueValidator(min_ball)],
            )

            # set min/max on the widget for front end user
            self.fields['%s%s' % (BALL_KEY,ball)].widget = forms.NumberInput(attrs={'min':min_ball,
                                                                            'max':max_ball})


    def clean(self):
        cleaned_data = super(EntryForm, self).clean()
        balls_and_values = {}
        for i in [f for f in self.fields if f[:5] == BALL_KEY]:
            value = cleaned_data.get(i)
            if value:
                balls_and_values[i] = value

        cleaned_data['validated_balls'] = ','.join([str(i) for i in balls_and_values.values()])

        # check for duplicates
        if len(balls_and_values.values()) != len(set(balls_and_values.values())):
            raise forms.ValidationError("Please don't select duplicate numbers")