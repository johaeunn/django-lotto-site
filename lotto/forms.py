from django import forms


class ManualLottoPurchaseForm(forms.Form):
    numbers = forms.CharField(
        label="로또 번호",
        help_text="1~45 사이 숫자 6개를 쉼표로 구분해서 입력하세요. 예: 3,11,18,25,33,42",
        widget=forms.TextInput(
            attrs={
                "placeholder": "예: 3,11,18,25,33,42",
            }
        ),
    )

    def clean_numbers(self):
        numbers_text = self.cleaned_data["numbers"]

        # 공백을 제거하고 쉼표 기준으로 분리
        number_parts = [
            part.strip()
            for part in numbers_text.split(",")
            if part.strip()
        ]

        if len(number_parts) != 6:
            raise forms.ValidationError("로또 번호는 정확히 6개 입력해야 합니다.")

        try:
            numbers = [int(part) for part in number_parts]
        except ValueError:
            raise forms.ValidationError("로또 번호는 숫자로만 입력해야 합니다.")

        if any(number < 1 or number > 45 for number in numbers):
            raise forms.ValidationError("각 번호는 1부터 45 사이여야 합니다.")

        if len(set(numbers)) != 6:
            raise forms.ValidationError("중복된 번호는 입력할 수 없습니다.")

        numbers.sort()
        return numbers