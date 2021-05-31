def correction_text_of_post(text: str) -> str:
    types_err = ['х', '×', 'X', 'x', 'Х', '*']
    for element in types_err:
        start_on = 0
        while True:
            finding = text.find(element, start_on)
            if finding == -1:
                break

            if text[finding - 1] == ' ' and text[finding + 1] == ' ':
                try:
                    int(text[finding - 2])
                    text = text[:finding - 1] + 'х' + text[finding + 2:]
                    start_on = finding + 1
                    continue
                except ValueError:
                    pass
            try:
                int(text[finding - 1])
                text = text[:finding] + 'х' + text[finding + 1:]
                start_on = finding + 1
            except ValueError:
                start_on = finding + 1

    return text


if __name__ == '__main__':
    data = 'продам трубу 1420*17,5-18,7 отличного качества , цена в безнале 60,000 с ндс. продам трубу 1220*12 '

    print(correction_text_of_post(data))
