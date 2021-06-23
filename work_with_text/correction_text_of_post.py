def correction_text_of_post(text: str) -> str:
    types_err = ['х', '×', 'X', 'x', 'Х', '*']
    for element in types_err:
        start_on = 0
        while True:
            finding = text.find(element, start_on)
            if finding == -1:
                break
            try:
                if text[finding - 1] == ' ' and text[finding + 1] == ' ':
                    try:
                        int(text[finding - 2])
                        text = text[:finding - 1] + 'х' + text[finding + 2:]
                        start_on = finding + 1
                        continue
                    except ValueError:
                        try:
                            int(text[finding - 3])
                            text = text[:finding - 2] + 'х' + text[finding + 2:]
                            start_on = finding + 1
                            continue
                        except ValueError:
                            pass
                else:
                    if text[finding - 1] == ' ' and text[finding + 1] != ' ':
                        try:
                            int(text[finding - 2])
                            text = text[:finding - 1] + 'х' + text[finding + 1:]
                            start_on = finding + 1
                        except ValueError:
                            try:
                                int(text[finding - 3])
                                text = text[:finding - 2] + 'х' + text[finding + 1:]
                                start_on = finding + 1
                                continue
                            except ValueError:
                                pass
                    elif text[finding - 1] != ' ' and text[finding + 1] == ' ':
                        try:
                            int(text[finding - 1])
                            text = text[:finding] + 'х' + text[finding + 2:]
                            start_on = finding + 1
                        except ValueError:
                            try:
                                int(text[finding - 3])
                                text = text[:finding - 1] + 'х' + text[finding + 1:]
                                start_on = finding + 1
                                continue
                            except ValueError:
                                pass

            except IndexError:
                pass
            try:
                int(text[finding - 1])
                text = text[:finding] + 'х' + text[finding + 1:]
                start_on = finding + 1
            except ValueError:
                start_on = finding + 1
    return text


if __name__ == '__main__':
    data = '325 х9 - 61000 состояние 325х 8-10 - 54000 325 x 8 х 9 х 10 ц/т - 50000 руб/тн фаска орбита (Объём)'

    print(correction_text_of_post(data))
