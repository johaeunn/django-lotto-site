from django import forms


class ManualLottoPurchaseForm(forms.Form):
    numbers = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "id": "selected-numbers-input",
            }
        ),
    )

    def clean_numbers(self):
        numbers_text = self.cleaned_data["numbers"]

        # 숫자판에서 선택된 번호는 "3,11,18,25,33,42" 형태로 전달
        number_parts = [
            part.strip()
            for part in numbers_text.split(",")
            if part.strip()
        ]

        if len(number_parts) != 6:
            raise forms.ValidationError("로또 번호는 정확히 6개 선택해야 합니다.")

        try:
            numbers = [int(part) for part in number_parts]
        except ValueError:
            raise forms.ValidationError("로또 번호는 숫자로만 구성되어야 합니다.")

        if any(number < 1 or number > 45 for number in numbers):
            raise forms.ValidationError("각 번호는 1부터 45 사이여야 합니다.")

        if len(set(numbers)) != 6:
            raise forms.ValidationError("중복된 번호는 선택할 수 없습니다.")

        numbers.sort()
        return numbers