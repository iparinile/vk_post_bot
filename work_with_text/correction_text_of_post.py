data = 'электсроварную 325 х 10 09Г2С - 21 тн. Челябинск. 78000 руб/тн с 325X10 п Хавп 325x10 вапвап 325х10 вапв 325×10 325*10'


def correction_text_of_post(text: str) -> str:
    types_err = ['х', '×', 'X', 'x', 'Х', '*']
    for element in types_err:
        start_on = 0
        while True:
            print(text[60:70])
            finding = text.find(element, start_on)
            print(finding)
            if finding == -1:
                break

            if text[finding-1] == ' ' and text[finding+1] == ' ':
                print('я зашел')
                try:
                    i = int(text[finding-2])
                    text = text[:finding-1] + 'х' + text[finding + 2:]
                    start_on = finding + 1
                    continue
                except ValueError:
                    start_on = finding + 1
                # if text[finding] == 'х':
                #     text = text[:finding - 1] + 'х' + text[finding + 2:]
                #     start_on = finding + 1
                #     continue

            try:
                i = int(text[finding - 1])
                text = text[:finding] + 'х' + text[finding + 1:]
                print(text)
            except ValueError:
                start_on = finding + 1

    return text


print(correction_text_of_post(data))
